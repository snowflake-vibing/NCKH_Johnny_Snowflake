"""Pure PyTorch faithful port of Choetkiertikul et al. (IEEE TSE 2019) Deep-SE architecture."""

import json
import math
import os
import random
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from config import DEEPSE_PRETRAIN_BASE_URL, download_file_with_retry
from metrics import compute_mae_mdae


class HighwayLayer(nn.Module):
    """Gated Highway layer matching Keras 1.0.6 Highway(activation='relu', transform_bias=-1)."""

    def __init__(self, dim: int, transform_bias: float = -1.0):
        super().__init__()
        self.h_proj = nn.Linear(dim, dim)
        self.t_proj = nn.Linear(dim, dim)
        nn.init.xavier_normal_(self.h_proj.weight)
        nn.init.zeros_(self.h_proj.bias)
        nn.init.xavier_normal_(self.t_proj.weight)
        nn.init.constant_(self.t_proj.bias, transform_bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.h_proj(x))
        t = torch.sigmoid(self.t_proj(x))
        return t * h + (1.0 - t) * x


class PoolingSeq(nn.Module):
    """Sequence pooling layer supporting mean, masked max, and last-valid-token modes."""

    def __init__(self, mode: str = "mean"):
        super().__init__()
        if mode not in ("mean", "max", "last"):
            raise ValueError(f"Unsupported pool_mode '{mode}'. Choose from: mean, max, last.")
        self.mode = mode

    def forward(self, seqs: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        if self.mode == "mean":
            masked_sum = (seqs * mask.unsqueeze(-1)).sum(dim=1)
            denom = torch.clamp(mask.sum(dim=1, keepdim=True), min=1.0)
            return masked_sum / denom
        if self.mode == "max":
            masked = seqs.masked_fill(mask.unsqueeze(-1) == 0, -1e9)
            return masked.max(dim=1).values
        lengths = torch.clamp(mask.sum(dim=1).long() - 1, min=0)
        batch_idx = torch.arange(seqs.size(0), device=seqs.device)
        return seqs[batch_idx, lengths]


class DeepSEModel(nn.Module):
    """Pure PyTorch implementation of Deep-SE (LSTM + Mean/Max/Last Pool + Shared Highway).

    Mirrors `Deep-SE/classification/create_model.py`:
    - Shared Embedding (index 0 reserved for PAD; index 1..vocab_size hold word embeddings)
    - Shared LSTM across Title and Description streams with Keras-style orthogonal/forget-1 init
    - Sequence Pooling + Average Merge (`0.5 * (pooled_title + pooled_descr)`)
    - Weight-tied Highway layer iterated `hidden_layers` times + Linear scalar regressor
    """

    def __init__(
        self,
        vocab_size: int = 500,
        emb_dim: int = 50,
        hidden_layers: int = 10,
        pool_mode: str = "mean",
        dropout_inp: bool = True,
        dropout_hid: bool = True,
        pretrained_embedding: Optional[np.ndarray] = None,
        freeze_embedding: bool = True,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.emb_dim = emb_dim
        self.hidden_layers = hidden_layers
        self.pool_mode = pool_mode
        self.freeze_embedding = freeze_embedding

        if pretrained_embedding is not None:
            if pretrained_embedding.ndim != 2 or pretrained_embedding.shape[1] != emb_dim:
                raise ValueError(
                    f"Pretrained embedding shape {pretrained_embedding.shape} incompatible with emb_dim={emb_dim}"
                )
            n_rows = pretrained_embedding.shape[0] + 1
            weight_init = np.zeros((n_rows, emb_dim), dtype=np.float32)
            weight_init[1:] = pretrained_embedding.astype(np.float32)
            self.embedding = nn.Embedding(n_rows, emb_dim, padding_idx=0)
            with torch.no_grad():
                self.embedding.weight.copy_(torch.from_numpy(weight_init))
            self.embedding.weight.requires_grad = not freeze_embedding
        else:
            n_rows = vocab_size + 1
            self.embedding = nn.Embedding(n_rows, emb_dim, padding_idx=0)

        self.n_embedding_rows = n_rows
        self.inp_dropout = nn.Dropout(0.2 if dropout_inp else 0.0)
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=emb_dim, batch_first=True)
        self._init_lstm_keras_style()

        self.pooling = PoolingSeq(mode=pool_mode)
        self.hid_dropout1 = nn.Dropout(0.5 if dropout_hid else 0.0)
        # create_highway() in Deep-SE instantiates one shared Highway layer and applies it hdl times.
        self.highway = HighwayLayer(emb_dim, transform_bias=-1.0)
        self.hid_dropout2 = nn.Dropout(0.5 if dropout_hid else 0.0)
        self.regressor = nn.Linear(emb_dim, 1)

    def _init_lstm_keras_style(self) -> None:
        nn.init.xavier_uniform_(self.lstm.weight_ih_l0)
        nn.init.orthogonal_(self.lstm.weight_hh_l0)
        nn.init.zeros_(self.lstm.bias_ih_l0)
        nn.init.zeros_(self.lstm.bias_hh_l0)
        with torch.no_grad():
            self.lstm.bias_ih_l0[self.emb_dim : 2 * self.emb_dim].fill_(1.0)

    def forward(
        self,
        title_ids: torch.Tensor,
        title_mask: torch.Tensor,
        descr_ids: torch.Tensor,
        descr_mask: torch.Tensor,
    ) -> torch.Tensor:
        title_emb = self.inp_dropout(self.embedding(title_ids))
        descr_emb = self.inp_dropout(self.embedding(descr_ids))

        title_hid, _ = self.lstm(title_emb)
        descr_hid, _ = self.lstm(descr_emb)

        pooled_title = self.pooling(title_hid, title_mask)
        pooled_descr = self.pooling(descr_hid, descr_mask)

        hidd = 0.5 * (pooled_title + pooled_descr)
        hidd = self.hid_dropout1(hidd)
        for _ in range(self.hidden_layers):
            hidd = self.highway(hidd)
        hidd = self.hid_dropout2(hidd)
        return self.regressor(hidd).view(-1)


def load_pretrained_lm_embedding(repo_name: str, emb_dim: int, cache_dir: str) -> np.ndarray:
    """Download Deep-SE NCE LSTM language-model HDF5 and extract the embedding weight matrix."""
    try:
        import h5py
    except ImportError as exc:
        raise ImportError(
            "Loading Deep-SE NCE pretrained HDF5 weights requires `h5py`. "
            "Install it (`pip install h5py`) or pass `--pretrain scratch`."
        ) from exc

    fname = f"lstm2v_{repo_name}_dim{emb_dim}.hdf5"
    local_path = os.path.join(cache_dir, fname)
    download_file_with_retry(f"{DEEPSE_PRETRAIN_BASE_URL}{fname}", local_path)

    primary_matches: List[Tuple[str, np.ndarray]] = []
    fallback_matches: List[Tuple[str, np.ndarray]] = []

    with h5py.File(local_path, "r") as hf:
        def visitor(name: str, obj) -> None:
            if isinstance(obj, h5py.Dataset) and len(obj.shape) == 2 and obj.shape[1] == emb_dim:
                if "embedding" in name.lower():
                    primary_matches.append((name, np.asarray(obj[...], dtype=np.float32)))
                elif obj.shape[0] >= 500:
                    fallback_matches.append((name, np.asarray(obj[...], dtype=np.float32)))

        hf.visititems(visitor)

    if primary_matches:
        return primary_matches[0][1]
    if fallback_matches:
        return fallback_matches[0][1]
    raise RuntimeError(
        f"No 2D embedding weight matrix with width {emb_dim} found inside {local_path}"
    )


def set_seed(seed: int) -> None:
    """Set deterministic RNG seeds across Python, NumPy, and PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def safe_torch_load(weights_path: str) -> dict:
    """Load state dict with weights_only=True when supported by installed PyTorch."""
    try:
        return torch.load(weights_path, map_location="cpu", weights_only=True)
    except TypeError:
        return torch.load(weights_path, map_location="cpu")


def cleanup_downloaded_file(filepath: str) -> None:
    """Delete a cached file safely to keep Kaggle disk usage compact."""
    if not filepath:
        return
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except OSError:
        pass


def make_deepse_loader(
    tensors: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    labels: np.ndarray,
    batch_size: int,
    shuffle: bool,
) -> DataLoader:
    """Build a DataLoader yielding (title_ids, title_mask, descr_ids, descr_mask, y)."""
    title_x, title_mask, descr_x, descr_mask = tensors
    ds = TensorDataset(
        torch.tensor(title_x, dtype=torch.long),
        torch.tensor(title_mask, dtype=torch.float32),
        torch.tensor(descr_x, dtype=torch.long),
        torch.tensor(descr_mask, dtype=torch.float32),
        torch.tensor(labels, dtype=torch.float32),
    )
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)


def evaluate_deepse_loader(
    model: nn.Module, loader: DataLoader, device: torch.device
) -> Tuple[float, float, np.ndarray]:
    """Run evaluation without gradients and return (MAE, MdAE, predictions)."""
    model.eval()
    preds: List[float] = []
    targets: List[float] = []
    with torch.no_grad():
        for t_ids, t_mask, d_ids, d_mask, y in loader:
            out = model(
                t_ids.to(device),
                t_mask.to(device),
                d_ids.to(device),
                d_mask.to(device),
            )
            preds.extend(out.cpu().numpy().tolist())
            targets.extend(y.numpy().tolist())
    mae, mdae, _ = compute_mae_mdae(targets, preds)
    return mae, mdae, np.asarray(preds, dtype=np.float64)


def train_deepse_session(
    train_tensors: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    train_y: np.ndarray,
    val_tensors: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    val_y: np.ndarray,
    test_tensors: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    test_y: np.ndarray,
    vocab_size: int,
    emb_dim: int,
    hidden_layers: int,
    pool_mode: str,
    pretrained_embedding: Optional[np.ndarray],
    freeze_embedding: bool,
    loss_name: str,
    lr: float,
    batch_size: int,
    epochs: int,
    seed: int,
    device: torch.device,
    ckpt_dir: str,
    min_patience: int = 5,
    max_patience: int = 30,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Train DeepSEModel with author-faithful RMSprop, adaptive LR halving, and early stopping."""
    set_seed(seed)
    os.makedirs(ckpt_dir, exist_ok=True)
    best_weights_path = os.path.join(ckpt_dir, "pytorch_model.bin")
    config_path = os.path.join(ckpt_dir, "model_config.json")

    train_loader = make_deepse_loader(train_tensors, train_y, batch_size=batch_size, shuffle=True)
    val_loader = make_deepse_loader(val_tensors, val_y, batch_size=max(batch_size, 128), shuffle=False)
    test_loader = make_deepse_loader(test_tensors, test_y, batch_size=max(batch_size, 128), shuffle=False)

    model = DeepSEModel(
        vocab_size=vocab_size,
        emb_dim=emb_dim,
        hidden_layers=hidden_layers,
        pool_mode=pool_mode,
        dropout_inp=True,
        dropout_hid=True,
        pretrained_embedding=pretrained_embedding,
        freeze_embedding=freeze_embedding,
    ).to(device)

    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.RMSprop(trainable_params, lr=lr)
    loss_fn = nn.MSELoss() if loss_name == "mse" else nn.L1Loss()

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "vocab_size": vocab_size,
                "emb_dim": emb_dim,
                "hidden_layers": hidden_layers,
                "pool_mode": pool_mode,
                "freeze_embedding": freeze_embedding,
                "n_embedding_rows": model.n_embedding_rows,
                "loss": loss_name,
                "lr": lr,
                "batch_size": batch_size,
                "seed": seed,
            },
            f,
            indent=2,
        )

    # Save initial weights as a defensive fallback in case NaN triggers on epoch 1.
    torch.save(model.state_dict(), best_weights_path)

    best_val_mae = float("inf")
    best_epoch = 0
    patience = min_patience
    wait = 0
    current_lr = lr
    history: List[Dict[str, Any]] = []

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        n_batches = max(1, len(train_loader))
        for t_ids, t_mask, d_ids, d_mask, by in train_loader:
            optimizer.zero_grad()
            preds = model(
                t_ids.to(device),
                t_mask.to(device),
                d_ids.to(device),
                d_mask.to(device),
            )
            loss = loss_fn(preds, by.to(device))
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item())

        avg_train_loss = total_loss / n_batches
        val_mae, val_mdae, _ = evaluate_deepse_loader(model, val_loader, device)

        if math.isnan(avg_train_loss) or math.isnan(val_mae):
            if verbose:
                print(f"  ⚠️ Epoch {epoch:03d}: NaN detected; stopping early cleanly.")
            break

        marker = ""
        if val_mae < best_val_mae:
            best_val_mae = val_mae
            best_epoch = epoch
            torch.save(model.state_dict(), best_weights_path)
            wait = 0
            marker = " ⭐ [BEST]"
        else:
            wait += 1
            if wait >= patience:
                wait = 0
                patience += 5
                current_lr /= 2.0
                for pg in optimizer.param_groups:
                    pg["lr"] = current_lr
                if patience > max_patience:
                    marker = " ⏹️ [EARLY_STOP]"

        history.append(
            {
                "epoch": epoch,
                "train_loss": round(avg_train_loss, 6),
                "val_mae": round(val_mae, 4),
                "val_mdae": round(val_mdae, 4),
                "lr": current_lr,
            }
        )

        if verbose and (marker or epoch == 1 or epoch % 25 == 0 or epoch == epochs):
            print(
                f"  Epoch {epoch:03d}/{epochs} | train_{loss_name}={avg_train_loss:.4f} | "
                f"val_mae={val_mae:.4f} | lr={current_lr:.6g}{marker}"
            )

        if patience > max_patience:
            break

    best_sd = safe_torch_load(best_weights_path)
    model.load_state_dict(best_sd)
    test_mae, test_mdae, test_preds = evaluate_deepse_loader(model, test_loader, device)

    return {
        "best_epoch": best_epoch,
        "best_val_mae": best_val_mae,
        "test_mae": test_mae,
        "test_mdae": test_mdae,
        "test_preds": test_preds,
        "history": history,
        "ckpt_dir": ckpt_dir,
        "best_weights_path": best_weights_path,
    }
