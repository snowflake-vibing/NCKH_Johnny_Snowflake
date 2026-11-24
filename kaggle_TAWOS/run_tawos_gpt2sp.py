"""TAWOS 13-project x 3-setting GPT2SP Experiment Runner (GitHub -> Kaggle GPU -> HF Artifact).

Ported directly from JohnnyPhan1712/SR-G3_planning-time-sp (`src/gpt2sp/train_tawos.py`):
- 2-model optimization per project: Model Final (final + cross) and Model Planning (planning).
- Chronological 60/20/20 split by `Planning_Date` (`SP <= 100`).
- Pinned defaults from `gpt2sp_plan.md`: epochs=20, lr=5e-4, batch_size=32, max_len=128, seed=42.
- Mandatory Median Effort Baseline + paired Wilcoxon Signed-Rank Test + Vargha-Delaney A12 + Holm.
- Per-project Auto-Resume and 1-commit final batch push to Hugging Face (`NCKH3-StoryPoint-Artifact`).
"""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import sys
from contextlib import nullcontext
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from kaggle_TAWOS.compare import run_compare
    from kaggle_TAWOS.config import (
        DEFAULT_CHECKPOINTS_REPO_NAME,
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        PREDICTION_COLS,
        PROJECTS,
        SEED,
        parse_projects_arg,
        resolve_data_dir,
        resolve_output_dir,
    )
    from kaggle_TAWOS.dataset import StoryPointDataset, load_tawos_snapshot
    from kaggle_TAWOS.hf_utils import HFExperimentLogger, ensure_tawos_snapshots
    from kaggle_TAWOS.metrics import (
        compute_metrics,
        sa_vs_median,
        safe_wilcoxon,
        vargha_delaney_a12,
    )
    from kaggle_TAWOS.model import GPT2SP, clear_hf_cache
except ImportError:
    from compare import run_compare  # type: ignore
    from config import (  # type: ignore
        DEFAULT_CHECKPOINTS_REPO_NAME,
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        PREDICTION_COLS,
        PROJECTS,
        SEED,
        parse_projects_arg,
        resolve_data_dir,
        resolve_output_dir,
    )
    from dataset import StoryPointDataset, load_tawos_snapshot  # type: ignore
    from hf_utils import HFExperimentLogger, ensure_tawos_snapshots  # type: ignore
    from metrics import (  # type: ignore
        compute_metrics,
        sa_vs_median,
        safe_wilcoxon,
        vargha_delaney_a12,
    )
    from model import GPT2SP, clear_hf_cache  # type: ignore


def set_seed(seed: int = SEED) -> None:
    """Fix PyTorch and NumPy random seeds for reproducibility."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def _autocast_ctx(device: torch.device, args: argparse.Namespace):
    if device.type != "cuda":
        return nullcontext()
    if getattr(args, "bf16", False):
        return torch.amp.autocast("cuda", dtype=torch.bfloat16)
    if getattr(args, "fp16", False):
        return torch.amp.autocast("cuda", dtype=torch.float16)
    return nullcontext()


def train_epoch(
    model: torch.nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    device: torch.device,
    args: argparse.Namespace,
    scaler: Any = None,
    clip_grad: float = 1.0,
) -> float:
    """Train GPT2SP for one epoch using L1Loss."""
    model.train()
    total_loss = 0.0
    for batch in loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        optimizer.zero_grad()
        with _autocast_ctx(device, args):
            _, loss = model(input_ids, attention_mask=attention_mask, labels=labels)

        if loss is not None:
            if scaler is not None and scaler.is_enabled():
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip_grad)
                scaler.step(optimizer)
                scaler.update()
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip_grad)
                optimizer.step()
            scheduler.step()
            total_loss += float(loss.item()) * len(labels)

    return total_loss / max(1, len(loader.dataset))


@torch.no_grad()
def evaluate_loss(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    args: argparse.Namespace,
) -> float:
    """Evaluate L1 loss on validation set."""
    model.eval()
    total_loss = 0.0
    for batch in loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)
        with _autocast_ctx(device, args):
            _, loss = model(input_ids, attention_mask=attention_mask, labels=labels)
        if loss is not None:
            total_loss += float(loss.item()) * len(labels)
    return total_loss / max(1, len(loader.dataset))


@torch.no_grad()
def predict_dataloader(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    args: argparse.Namespace,
) -> np.ndarray:
    """Predict story points clipped to >= 0."""
    model.eval()
    preds: List[float] = []
    for batch in loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        with _autocast_ctx(device, args):
            logits, _ = model(input_ids, attention_mask=attention_mask)
        preds.extend(logits.squeeze(-1).float().cpu().numpy().tolist())
    return np.clip(np.array(preds, dtype=np.float64), 0.0, None)


def train_single_model(
    train_texts: List[str],
    train_labels: np.ndarray,
    val_texts: List[str],
    val_labels: np.ndarray,
    tokenizer: Any,
    args: argparse.Namespace,
    device: torch.device,
    ckpt_save_dir: Optional[str] = None,
) -> GPT2SP:
    """Train 1 GPT2SP model, track best val checkpoint on CPU RAM, and restore it."""
    from transformers import get_linear_schedule_with_warmup

    train_ds = StoryPointDataset(train_texts, train_labels, tokenizer, max_length=args.max_len)
    val_ds = StoryPointDataset(val_texts, val_labels, tokenizer, max_length=args.max_len)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    model = GPT2SP(pretrained_model_name="gpt2").to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    total_steps = len(train_loader) * args.epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=max(1, total_steps)
    )

    use_scaler = device.type == "cuda" and bool(getattr(args, "fp16", False)) and not bool(getattr(args, "bf16", False))
    scaler = torch.amp.GradScaler("cuda", enabled=use_scaler) if device.type == "cuda" else None

    best_val_loss = float("inf")
    best_state: Optional[Dict[str, torch.Tensor]] = None

    for epoch in range(1, args.epochs + 1):
        tr_loss = train_epoch(model, train_loader, optimizer, scheduler, device, args, scaler=scaler)
        val_loss = evaluate_loss(model, val_loader, device, args)
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        print(f"    Epoch {epoch:02d}/{args.epochs:02d} - Train L1: {tr_loss:.4f} - Val L1: {val_loss:.4f}")

    if best_state is not None:
        model.load_state_dict({k: v.to(device) for k, v in best_state.items()})

    if ckpt_save_dir:
        os.makedirs(ckpt_save_dir, exist_ok=True)
        model.transformer.save_pretrained(ckpt_save_dir)
        tokenizer.save_pretrained(ckpt_save_dir)
        torch.save(
            {
                "dense1": model.dense1.state_dict(),
                "dense2": model.dense2.state_dict(),
                "score": model.score.state_dict(),
                "best_val_loss": best_val_loss,
            },
            os.path.join(ckpt_save_dir, "regression_head.pt"),
        )

    return model


def _build_prediction_df(base_test: pd.DataFrame, project: str, y_true_col: str, y_pred: np.ndarray) -> pd.DataFrame:
    df = base_test.assign(
        project=project,
        y_true=base_test[y_true_col].astype(float),
        y_pred=y_pred.astype(float),
    )[PREDICTION_COLS].copy()
    df["ID"] = df["ID"].astype(np.int64)
    df["changed"] = df["changed"].astype(bool)
    df["y_true"] = df["y_true"].astype(np.float64)
    df["y_pred"] = df["y_pred"].astype(np.float64)
    return df


def run_tawos_project(
    project: str,
    parquet_path: str,
    needed_settings: List[str],
    args: argparse.Namespace,
    tokenizer: Any,
    device: torch.device,
    ckpt_root_dir: str,
    logger: HFExperimentLogger,
) -> Dict[str, pd.DataFrame]:
    """Train requested setting models for 1 TAWOS project (2-model optimization)."""
    print(f"\n{'=' * 25} TAWOS Project: {project} {'=' * 25}")
    train_df, val_df, test_df = load_tawos_snapshot(
        project, parquet_path=parquet_path, setting=None, input_mode=args.input_mode, max_sp=MAX_SP
    )
    base_test = test_df.assign(project=project)
    results: Dict[str, pd.DataFrame] = {}

    need_final_model = any(s in ("final", "cross") for s in needed_settings)
    need_planning_model = "planning" in needed_settings

    if need_final_model:
        print(f"  -> [Model FINAL] Training for {project} (train={len(train_df)}, val={len(val_df)})...")
        ckpt_dir = os.path.join(ckpt_root_dir, project, "final") if args.save_checkpoints else None
        model_final = train_single_model(
            train_df["Final_Text"].tolist(),
            train_df["Final_Story_Point"].to_numpy(),
            val_df["Final_Text"].tolist(),
            val_df["Final_Story_Point"].to_numpy(),
            tokenizer,
            args,
            device,
            ckpt_save_dir=ckpt_dir,
        )

        if "final" in needed_settings:
            ds_f = StoryPointDataset(
                test_df["Final_Text"].tolist(), test_df["Final_Story_Point"].to_numpy(), tokenizer, max_length=args.max_len
            )
            loader_f = DataLoader(ds_f, batch_size=args.batch_size, shuffle=False)
            pred_f = predict_dataloader(model_final, loader_f, device, args)
            results["final"] = _build_prediction_df(base_test, project, "Final_Story_Point", pred_f)

        if "cross" in needed_settings:
            ds_c = StoryPointDataset(
                test_df["Text"].tolist(), test_df["Story_Point"].to_numpy(), tokenizer, max_length=args.max_len
            )
            loader_c = DataLoader(ds_c, batch_size=args.batch_size, shuffle=False)
            pred_c = predict_dataloader(model_final, loader_c, device, args)
            results["cross"] = _build_prediction_df(base_test, project, "Story_Point", pred_c)

        if ckpt_dir and logger.enabled and logger.checkpoints_repo_id:
            logger.upload_checkpoint_dir(ckpt_dir, f"tawos_gpt2sp/{project}/final", f"Upload checkpoint {project}/final")
            shutil.rmtree(ckpt_dir, ignore_errors=True)

        del model_final
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    if need_planning_model:
        print(f"  -> [Model PLANNING] Training for {project} (train={len(train_df)}, val={len(val_df)})...")
        ckpt_dir = os.path.join(ckpt_root_dir, project, "planning") if args.save_checkpoints else None
        model_plan = train_single_model(
            train_df["Text"].tolist(),
            train_df["Story_Point"].to_numpy(),
            val_df["Text"].tolist(),
            val_df["Story_Point"].to_numpy(),
            tokenizer,
            args,
            device,
            ckpt_save_dir=ckpt_dir,
        )
        ds_p = StoryPointDataset(
            test_df["Text"].tolist(), test_df["Story_Point"].to_numpy(), tokenizer, max_length=args.max_len
        )
        loader_p = DataLoader(ds_p, batch_size=args.batch_size, shuffle=False)
        pred_p = predict_dataloader(model_plan, loader_p, device, args)
        results["planning"] = _build_prediction_df(base_test, project, "Story_Point", pred_p)

        if ckpt_dir and logger.enabled and logger.checkpoints_repo_id:
            logger.upload_checkpoint_dir(ckpt_dir, f"tawos_gpt2sp/{project}/planning", f"Upload checkpoint {project}/planning")
            shutil.rmtree(ckpt_dir, ignore_errors=True)

        del model_plan
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return results


def _try_load_resumed_project(
    project: str,
    target_settings: List[str],
    per_proj_dir: str,
    resume_dl_cache: str,
    logger: HFExperimentLogger,
) -> Optional[Dict[str, pd.DataFrame]]:
    loaded: Dict[str, pd.DataFrame] = {}
    for setting in target_settings:
        local_file = os.path.join(per_proj_dir, f"{project}_{setting}.parquet")
        if os.path.isfile(local_file) and os.path.getsize(local_file) > 0:
            loaded[setting] = pd.read_parquet(local_file)
            continue
        rel_hf = f"predictions/per_project/{project}_{setting}.parquet"
        if logger.enabled:
            dl = logger.download_remote_file(rel_hf, resume_dl_cache)
            if dl and os.path.isfile(dl):
                os.makedirs(per_proj_dir, exist_ok=True)
                shutil.copy2(dl, local_file)
                loaded[setting] = pd.read_parquet(local_file)
                continue
        return None
    return loaded


def run_smoke_test(
    args: argparse.Namespace,
    snapshot_paths: Dict[str, str],
    tokenizer: Any,
    device: torch.device,
    out_dir: str,
) -> None:
    """Mini-batch 1-epoch smoke verification on first available project."""
    sample_proj = "JSWSERVER" if "JSWSERVER" in snapshot_paths else sorted(snapshot_paths.keys())[0]
    print(f"\n🧪 [SMOKE TEST] Running 1-epoch mini-batch sanity check on {sample_proj}...")
    train_df, val_df, test_df = load_tawos_snapshot(
        sample_proj, parquet_path=snapshot_paths[sample_proj], setting=None, input_mode=args.input_mode
    )
    mini_args = copy.deepcopy(args)
    mini_args.epochs = 1
    mini_args.batch_size = min(4, len(train_df))

    model = train_single_model(
        train_df["Final_Text"].iloc[:8].tolist(),
        train_df["Final_Story_Point"].iloc[:8].to_numpy(),
        val_df["Final_Text"].iloc[:4].tolist(),
        val_df["Final_Story_Point"].iloc[:4].to_numpy(),
        tokenizer,
        mini_args,
        device,
    )
    ds = StoryPointDataset(
        test_df["Final_Text"].iloc[:4].tolist(),
        test_df["Final_Story_Point"].iloc[:4].to_numpy(),
        tokenizer,
        max_length=args.max_len,
    )
    preds = predict_dataloader(model, DataLoader(ds, batch_size=4), device, mini_args)
    assert len(preds) == len(ds), "Smoke test prediction length mismatch!"
    print(f"  ✅ Smoke test passed! Sample predictions on {sample_proj}: {np.round(preds, 4).tolist()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train & evaluate GPT2SP on 13 TAWOS snapshots across final/cross/planning settings."
    )
    parser.add_argument("--projects", type=str, default="all", help="'all' or comma-separated TAWOS project keys")
    parser.add_argument(
        "--settings",
        type=str,
        default="all",
        choices=["all", "final", "cross", "planning"],
        help="Experimental settings to run",
    )
    parser.add_argument(
        "--input-mode",
        type=str,
        default="title_description",
        choices=["title_description", "title_only"],
    )
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-len", type=int, default=128)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--fp16", action="store_true", help="Use FP16 autocast on CUDA")
    parser.add_argument("--bf16", action="store_true", help="Use BF16 autocast on CUDA")
    parser.add_argument("--save-checkpoints", action="store_true", help="Upload trained checkpoints to HF Model repo")
    parser.add_argument("--smoke-test", action="store_true", help="Run fast mini-batch smoke test only")
    parser.add_argument("--no-resume", action="store_true", help="Do not reuse completed per-project parquets")
    parser.add_argument("--no-hf-push", action="store_true")
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--data-dir", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--checkpoints-repo", type=str, default=DEFAULT_CHECKPOINTS_REPO_NAME)
    parser.add_argument("--snapshots-subdir", type=str, default=DEFAULT_SNAPSHOTS_SUBDIR)
    parser.add_argument(
        "--run-name",
        type=str,
        default="experiments/tawos/gpt2sp/13proj_3settings_seed42",
        help="HF dataset subdirectory prefix",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    projects = parse_projects_arg(args.projects)
    target_settings = ["final", "cross", "planning"] if args.settings == "all" else [args.settings]

    out_dir = resolve_output_dir(args.output_dir, args.run_name)
    pred_dir = os.path.join(out_dir, "predictions")
    per_proj_dir = os.path.join(pred_dir, "per_project")
    resume_cache_dir = os.path.join(out_dir, "_hf_resume_cache")
    ckpt_root_dir = os.path.join(out_dir, "_ckpts")
    os.makedirs(per_proj_dir, exist_ok=True)

    data_cache_dir = resolve_data_dir(args.data_dir)
    extra_dirs = [args.data_dir] if args.data_dir else []
    snapshot_paths = ensure_tawos_snapshots(
        projects=projects,
        local_dir=data_cache_dir,
        results_repo=args.results_repo,
        remote_subdir=args.snapshots_subdir,
        extra_search_dirs=extra_dirs,
    )

    from transformers import GPT2Tokenizer

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    if args.smoke_test:
        run_smoke_test(args, snapshot_paths, tokenizer, device, out_dir)
        return

    logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=args.checkpoints_repo if args.save_checkpoints else None,
        run_prefix=args.run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    print("=" * 85)
    print(f"🚀 TAWOS GPT2SP | device={device} | projects={len(projects)} | settings={target_settings}")
    print("=" * 85)

    all_preds_by_setting: Dict[str, List[pd.DataFrame]] = {s: [] for s in target_settings}
    summary_rows: List[Dict[str, Any]] = []

    for proj in projects:
        resumed = (
            None
            if args.no_resume
            else _try_load_resumed_project(proj, target_settings, per_proj_dir, resume_cache_dir, logger)
        )
        if resumed is not None:
            print(f"⏭️ Resumed completed predictions for {proj} ({', '.join(target_settings)})")
            proj_preds = resumed
        else:
            proj_preds = run_tawos_project(
                project=proj,
                parquet_path=snapshot_paths[proj],
                needed_settings=target_settings,
                args=args,
                tokenizer=tokenizer,
                device=device,
                ckpt_root_dir=ckpt_root_dir,
                logger=logger,
            )
            per_proj_batch: List[Tuple[str, str]] = []
            for s_name, df_s in proj_preds.items():
                p_local = os.path.join(per_proj_dir, f"{proj}_{s_name}.parquet")
                df_s.to_parquet(p_local, index=False)
                per_proj_batch.append((p_local, f"predictions/per_project/{proj}_{s_name}.parquet"))
            if logger.enabled:
                logger.upload_results_batch(
                    per_proj_batch, f"Checkpoint per-project GPT2SP TAWOS predictions for {proj}"
                )

        # Compute per-project metrics + mandatory Median Effort Baseline comparison (AGENTS.md)
        train_df, val_df, _ = load_tawos_snapshot(
            proj, parquet_path=snapshot_paths[proj], setting=None, input_mode=args.input_mode, max_sp=MAX_SP
        )
        pool_df = pd.concat([train_df, val_df], ignore_index=True)

        for s_name in target_settings:
            df_s = proj_preds[s_name]
            all_preds_by_setting[s_name].append(df_s)
            pool_col = "Story_Point" if s_name == "planning" else "Final_Story_Point"
            pool_vals = pool_df[pool_col].astype(np.float64).to_numpy()
            med_val = float(np.median(pool_vals))

            y_t = df_s["y_true"].astype(np.float64).to_numpy()
            y_p = df_s["y_pred"].astype(np.float64).to_numpy()
            y_med = np.full_like(y_t, med_val, dtype=np.float64)

            gpt_m = compute_metrics(y_t, y_p, pool=pool_vals, seed=args.seed, rg_runs=1000)
            med_m = compute_metrics(y_t, y_med, pool=pool_vals, seed=args.seed, rg_runs=1000)
            w_stat, p_val = safe_wilcoxon(np.abs(y_t - y_p), np.abs(y_t - y_med))
            a12_val = vargha_delaney_a12(np.abs(y_t - y_p), np.abs(y_t - y_med))
            sa_med = sa_vs_median(gpt_m["MAE"], med_m["MAE"])

            summary_rows.append(
                {
                    "project": proj,
                    "setting": s_name,
                    "n_train": len(pool_df),
                    "n_test": len(df_s),
                    "TrainVal_Median": med_val,
                    "Median_MAE": med_m["MAE"],
                    "Median_MdAE": med_m["MdAE"],
                    "GPT2SP_MAE": gpt_m["MAE"],
                    "GPT2SP_MdAE": gpt_m["MdAE"],
                    "GPT2SP_SA_RG (%)": gpt_m["SA"],
                    "SA_vs_Median (%)": sa_med,
                    "Wilcoxon_W_vs_Med": w_stat,
                    "p_value_vs_Med": p_val,
                    "A12_vs_Med": a12_val,
                    "Verdict": "BEATS_MEDIAN" if gpt_m["MAE"] < med_m["MAE"] else "LOSES_TO_MEDIAN",
                }
            )
            print(
                f"  📊 {proj:10s} [{s_name:8s}] GPT2SP_MAE={gpt_m['MAE']:.4f} | "
                f"Median_MAE={med_m['MAE']:.4f} | SA_vs_Med={sa_med:+.2f}% | A12={a12_val:.3f}"
            )

    batch_items: List[Tuple[str, str]] = []
    for s_name, dfs in all_preds_by_setting.items():
        combined_df = pd.concat(dfs, ignore_index=True)
        out_pq = os.path.join(pred_dir, f"gpt2sp_gpt2sp_{s_name}.parquet")
        combined_df.to_parquet(out_pq, index=False)
        batch_items.append((out_pq, f"predictions/gpt2sp_gpt2sp_{s_name}.parquet"))

    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(out_dir, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    batch_items.append((summary_path, "summary.csv"))

    # Global project-level Wilcoxon Signed-Rank Test vs. Median Effort Baseline per setting
    stat_rows: List[Dict[str, Any]] = []
    for s_name in target_settings:
        sub = summary_df[summary_df["setting"] == s_name]
        w_glob, p_glob = safe_wilcoxon(sub["GPT2SP_MAE"], sub["Median_MAE"])
        a12_glob = vargha_delaney_a12(sub["GPT2SP_MAE"], sub["Median_MAE"])
        stat_rows.append(
            {
                "setting": s_name,
                "Comparison": "GPT2SP_MAE vs Median_MAE",
                "N_Projects": len(sub),
                "Mean_Diff": float((sub["GPT2SP_MAE"] - sub["Median_MAE"]).mean()),
                "Wilcoxon_W": w_glob,
                "p_value": p_glob,
                "A12_vs_Med": a12_glob,
                "Wins_vs_Median": int((sub["Verdict"] == "BEATS_MEDIAN").sum()),
                "Losses_vs_Median": int((sub["Verdict"] == "LOSES_TO_MEDIAN").sum()),
                "Mean_SA_vs_Median (%)": float(sub["SA_vs_Median (%)"].mean()),
            }
        )
    stat_df = pd.DataFrame(stat_rows)
    stat_path = os.path.join(out_dir, "stat_tests_vs_median.csv")
    stat_df.to_csv(stat_path, index=False)
    batch_items.append((stat_path, "stat_tests_vs_median.csv"))

    comp_outputs = run_compare(
        pred_dir=pred_dir,
        prefix="gpt2sp",
        out_dir=out_dir,
        title_prefix="TAWOS GPT2SP",
    )
    for rel_key, local_file in comp_outputs.items():
        batch_items.append((local_file, rel_key))

    meta_path = logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "projects": projects,
            "settings": target_settings,
            "n_summary_rows": len(summary_df),
        },
        upload=False,
    )
    batch_items.append((meta_path, "metadata.json"))

    if logger.enabled:
        ok = logger.upload_results_batch(
            batch_items,
            f"Finalize {args.run_name} predictions, summary, Wilcoxon/A12 tables, figure & metadata",
        )
        if ok:
            print(f"\n✅ Finalized {len(batch_items)} files in {logger.results_repo_id}/{args.run_name}!")

    if args.save_checkpoints:
        clear_hf_cache()


if __name__ == "__main__":
    main()
