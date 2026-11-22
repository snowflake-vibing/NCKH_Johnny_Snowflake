"""Pure PyTorch GPT2SP architecture and Hugging Face checkpoint loaders."""

import os
from typing import Optional, Tuple
import torch
import torch.nn as nn
from huggingface_hub import hf_hub_download
from transformers import GPT2Config, GPT2Model, GPT2Tokenizer


class GPT2SP(nn.Module):
    """Pure PyTorch implementation of Fu & Tantithamthavorn (IEEE TSE 2023) GPT2SP.

    Avoids GPT2PreTrainedModel metaclass tied-weight issues on newer transformers
    versions while preserving 100% of the author's 2-layer MLP head (dense1, dense2, score).
    """

    def __init__(self, config: GPT2Config):
        super().__init__()
        self.config = config
        self.transformer = GPT2Model(config)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)
        self.score = nn.Linear(config.n_embd, 1, bias=False)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        transformer_outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        hidden_states = transformer_outputs[0]
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        logits = self.score(hidden_states)

        batch_size = input_ids.shape[0]
        if self.config.pad_token_id is not None:
            non_pad = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
            sequence_lengths = torch.clamp(non_pad, min=0)
        else:
            sequence_lengths = torch.full(
                (batch_size,),
                input_ids.shape[1] - 1,
                device=logits.device,
                dtype=torch.long,
            )

        batch_idx = torch.arange(batch_size, device=logits.device)
        return logits[batch_idx, sequence_lengths].view(-1)


def build_tokenizer_and_config(base_model: str = "gpt2") -> Tuple[GPT2Tokenizer, GPT2Config]:
    """Load GPT-2 tokenizer and regression config with pad_token mapped to eos_token."""
    tokenizer = GPT2Tokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token
    config = GPT2Config.from_pretrained(
        base_model,
        num_labels=1,
        pad_token_id=tokenizer.pad_token_id,
    )
    return tokenizer, config


def safe_torch_load(weights_path: str) -> dict:
    """Load state dict with weights_only=True when supported by installed PyTorch."""
    try:
        return torch.load(weights_path, map_location="cpu", weights_only=True)
    except TypeError:
        return torch.load(weights_path, map_location="cpu")


def load_official_gpt2sp_checkpoint(
    repo_id: str,
    config: GPT2Config,
    device: torch.device,
    hf_token: Optional[str] = None,
) -> Tuple[GPT2SP, str]:
    """Download official author checkpoint and load all transformer + MLP weights."""
    weights_path = hf_hub_download(
        repo_id=repo_id,
        filename="pytorch_model.bin",
        token=hf_token,
    )
    state_dict = safe_torch_load(weights_path)

    required_head_keys = ("dense1.weight", "dense2.weight", "score.weight")
    missing_head = [k for k in required_head_keys if k not in state_dict]
    if missing_head:
        raise KeyError(
            f"Checkpoint {repo_id} missing expected MLP weights: {missing_head}"
        )

    model = GPT2SP(config)
    missing, _ = model.load_state_dict(state_dict, strict=False)
    missing_head_after = [k for k in missing if any(h in k for h in ("dense1", "dense2", "score"))]
    if missing_head_after:
        raise RuntimeError(f"Failed to bind head weights from {repo_id}: {missing_head_after}")

    model.to(device)
    model.eval()
    return model, weights_path


def init_gpt2sp_for_training(
    config: GPT2Config,
    device: torch.device,
    base_model: str = "gpt2",
) -> GPT2SP:
    """Initialize a fresh GPT2SP model with pretrained GPT-2 backbone for fine-tuning."""
    model = GPT2SP(config)
    model.transformer = GPT2Model.from_pretrained(base_model, config=config)
    model.to(device)
    return model


def cleanup_downloaded_file(filepath: str) -> None:
    """Delete downloaded weights file (and symlink target in HF blob cache) to save disk."""
    if not filepath:
        return
    targets = []
    if os.path.islink(filepath):
        targets.append(os.path.realpath(filepath))
    targets.append(filepath)
    for target in targets:
        try:
            if os.path.exists(target):
                os.remove(target)
        except OSError:
            pass
