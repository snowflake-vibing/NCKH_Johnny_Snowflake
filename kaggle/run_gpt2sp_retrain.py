"""Strategy 2: Retrain GPT2SP from scratch across settings/seeds and push to HF Hub."""

import argparse
import os
import random
import sys
import time
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BENCHMARK_PROJECTS,
    DEFAULT_CHECKPOINTS_REPO_NAME,
    DEFAULT_RESULTS_REPO_NAME,
    format_issue_texts,
    load_gpt2sp_splits,
    resolve_output_dir,
)
from hf_utils import HFExperimentLogger
from metrics import compute_mae_mdae, compute_sa, safe_wilcoxon, vargha_delaney_a12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrain GPT2SP from GPT-2 base and compare against Median Effort Baseline."
    )
    parser.add_argument("--project", type=str, default="springxd", choices=list(BENCHMARK_PROJECTS.keys()))
    parser.add_argument(
        "--setting",
        type=str,
        default="title_20",
        choices=["title_20", "full_128", "planning_clean"],
        help="Input representation / leakage setting.",
    )
    parser.add_argument(
        "--clean-csv",
        type=str,
        default=None,
        help="Path to clean planning-time CSV (used when --setting planning_clean).",
    )
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument(
        "--batch-size",
        type=int,
        default=0,
        help="Effective batch size. 0 uses author's dynamic 30%% of train size via grad accumulation.",
    )
    parser.add_argument("--max-length", type=int, default=0, help="Override max_length (0 = setting default).")
    parser.add_argument("--seeds", type=str, default="42", help="Comma-separated random seeds.")
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--checkpoints-repo", type=str, default=DEFAULT_CHECKPOINTS_REPO_NAME)
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_clean_csv(explicit_path: str) -> str:
    """Locate leakage-free planning-time CSV across repo paths."""
    candidates = [
        explicit_path,
        os.path.join("data", "clean", "springxd_cleaned_dataset.csv"),
        os.path.join("docs", "draft", "springxd_cleaned_dataset.csv"),
    ]
    for cand in candidates:
        if cand and os.path.exists(cand):
            return cand
    raise FileNotFoundError(
        "Clean planning-time CSV not found in --clean-csv, data/clean/, or docs/draft/."
    )


def prepare_setting_data(
    args: argparse.Namespace,
    cache_dir: str,
) -> Tuple[List[str], np.ndarray, List[str], np.ndarray, List[str], np.ndarray, List, int]:
    """Load (train, val, test) texts and labels cleanly according to selected setting."""
    if args.setting == "planning_clean":
        clean_path = resolve_clean_csv(args.clean_csv)
        df = pd.read_csv(clean_path)
        if "Is_GPT2SP_3526_Subset" in df.columns:
            df = df[df["Is_GPT2SP_3526_Subset"] == 1].reset_index(drop=True)
        splits_col = df["Chronological_Split"].astype(str).str.lower()
        tr_df = df[splits_col == "train"].reset_index(drop=True)
        va_df = df[splits_col.isin(["val", "valid", "validation"])].reset_index(drop=True)
        te_df = df[splits_col == "test"].reset_index(drop=True)

        def get_clean_text(sub_df: pd.DataFrame) -> List[str]:
            if "Clean_Text" in sub_df.columns:
                return sub_df["Clean_Text"].fillna("").astype(str).tolist()
            return (
                sub_df["Clean_Title"].fillna("").astype(str)
                + " "
                + sub_df["Clean_Description"].fillna("").astype(str)
            ).str.strip().tolist()

        seq_len = args.max_length or 128
        return (
            get_clean_text(tr_df),
            tr_df["Initial_Story_Point"].astype(float).values,
            get_clean_text(va_df),
            va_df["Initial_Story_Point"].astype(float).values,
            get_clean_text(te_df),
            te_df["Initial_Story_Point"].astype(float).values,
            te_df["Issue_Key"].tolist() if "Issue_Key" in te_df.columns else list(range(len(te_df))),
            seq_len,
        )

    splits = load_gpt2sp_splits(args.project, cache_dir)
    include_desc = args.setting == "full_128"
    seq_len = args.max_length or (128 if include_desc else 20)
    tr_df, va_df, te_df = splits["train"], splits["val"], splits["test"]
    keys = te_df["issuekey"].tolist() if "issuekey" in te_df.columns else list(range(len(te_df)))
    return (
        format_issue_texts(tr_df, include_description=include_desc),
        pd.to_numeric(tr_df["storypoint"], errors="coerce").fillna(0.0).values,
        format_issue_texts(va_df, include_description=include_desc),
        pd.to_numeric(va_df["storypoint"], errors="coerce").fillna(0.0).values,
        format_issue_texts(te_df, include_description=include_desc),
        pd.to_numeric(te_df["storypoint"], errors="coerce").fillna(0.0).values,
        keys,
        seq_len,
    )


def make_loader(
    tokenizer, texts: List[str], labels: np.ndarray, max_len: int, batch_size: int, shuffle: bool
) -> DataLoader:
    enc = tokenizer.batch_encode_plus(
        texts,
        truncation=True,
        max_length=max_len,
        padding="max_length",
        return_tensors="pt",
    )
    ds = TensorDataset(enc["input_ids"], enc["attention_mask"], torch.tensor(labels, dtype=torch.float32))
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)


def evaluate_loader(
    model: nn.Module, loader: DataLoader, device: torch.device
) -> Tuple[float, float, np.ndarray]:
    model.eval()
    preds, targets = [], []
    with torch.no_grad():
        for b_ids, b_mask, b_y in loader:
            out = model(b_ids.to(device), attention_mask=b_mask.to(device))
            preds.extend(out.cpu().numpy().tolist())
            targets.extend(b_y.numpy().tolist())
    mae, mdae, _ = compute_mae_mdae(targets, preds)
    return mae, mdae, np.asarray(preds, dtype=np.float64)


def save_loss_curve(df_hist: pd.DataFrame, out_path: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_hist["epoch"], df_hist["train_mae_loss"], label="Train MAE Loss", marker="o", markersize=3)
    ax.plot(df_hist["epoch"], df_hist["val_mae"], label="Validation MAE", marker="s", markersize=3)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MAE (Story Points)")
    ax.set_title(title)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close(fig)


def train_one_seed(
    seed: int,
    args: argparse.Namespace,
    tokenizer,
    config,
    data_tuple: Tuple,
    device: torch.device,
    out_dir: str,
    hf_logger: HFExperimentLogger,
) -> Dict:
    tr_txt, tr_y, va_txt, va_y, te_txt, te_y, te_keys, seq_len = data_tuple
    set_seed(seed)

    # Physical micro-batch capped for T4 15GB VRAM safety; accumulate gradients for large target batch.
    effective_bs = args.batch_size if args.batch_size > 0 else max(8, int(len(tr_txt) * 0.3))
    micro_bs = 32 if seq_len > 32 else 64
    micro_bs = min(micro_bs, effective_bs)
    accum_steps = max(1, int(np.ceil(effective_bs / micro_bs)))

    train_loader = make_loader(tokenizer, tr_txt, tr_y, seq_len, micro_bs, shuffle=True)
    val_loader = make_loader(tokenizer, va_txt, va_y, seq_len, micro_bs, shuffle=False)
    test_loader = make_loader(tokenizer, te_txt, te_y, seq_len, micro_bs, shuffle=False)

    from transformers import get_linear_schedule_with_warmup
    from model import init_gpt2sp_for_training, safe_torch_load

    model = init_gpt2sp_for_training(config, device, base_model="gpt2")
    loss_fn = nn.L1Loss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    updates_per_epoch = max(1, int(np.ceil(len(train_loader) / accum_steps)))
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=updates_per_epoch * args.epochs
    )

    seed_dir = os.path.join(out_dir, f"seed_{seed}")
    ckpt_dir = os.path.join(seed_dir, "best_checkpoint")
    os.makedirs(ckpt_dir, exist_ok=True)

    best_val_mae = float("inf")
    best_epoch = 0
    history = []

    print(
        f"\n🏋️ Seed {seed} | effective_bs={effective_bs} (micro_bs={micro_bs}, accum={accum_steps}) | "
        f"seq_len={seq_len} | epochs={args.epochs}"
    )

    for epoch in range(1, args.epochs + 1):
        model.train()
        optimizer.zero_grad()
        total_loss = 0.0
        for step, (b_ids, b_mask, b_y) in enumerate(train_loader):
            preds = model(b_ids.to(device), attention_mask=b_mask.to(device))
            loss = loss_fn(preds, b_y.to(device))
            total_loss += float(loss.item())
            (loss / accum_steps).backward()

            if (step + 1) % accum_steps == 0 or (step + 1) == len(train_loader):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

        avg_train_loss = total_loss / max(1, len(train_loader))
        val_mae, val_mdae, _ = evaluate_loader(model, val_loader, device)
        history.append(
            {
                "epoch": epoch,
                "train_mae_loss": round(avg_train_loss, 4),
                "val_mae": round(val_mae, 4),
                "val_mdae": round(val_mdae, 4),
            }
        )

        marker = ""
        if val_mae <= best_val_mae:
            best_val_mae = val_mae
            best_epoch = epoch
            torch.save(model.state_dict(), os.path.join(ckpt_dir, "pytorch_model.bin"))
            config.save_pretrained(ckpt_dir)
            marker = " ⭐ [BEST]"

        print(f"  Epoch {epoch:02d}/{args.epochs} | train_loss={avg_train_loss:.4f} | val_mae={val_mae:.4f}{marker}")

    df_hist = pd.DataFrame(history)
    hist_path = os.path.join(seed_dir, "training_history.csv")
    df_hist.to_csv(hist_path, index=False)
    hf_logger.upload_result(hist_path, f"seed_{seed}/training_history.csv")

    curve_path = os.path.join(seed_dir, "loss_curve.png")
    save_loss_curve(df_hist, curve_path, f"GPT2SP Retrain ({args.project} | {args.setting} | seed={seed})")
    hf_logger.upload_result(curve_path, f"seed_{seed}/loss_curve.png")

    # Reload best checkpoint cleanly for honest test evaluation
    best_sd = safe_torch_load(os.path.join(ckpt_dir, "pytorch_model.bin"))
    model.load_state_dict(best_sd)
    test_mae, test_mdae, test_preds = evaluate_loader(model, test_loader, device)

    train_median = float(np.median(tr_y))
    med_pred_arr = np.full(len(te_y), train_median, dtype=np.float64)
    med_mae, med_mdae, err_med = compute_mae_mdae(te_y, med_pred_arr)
    err_model = np.abs(te_y - test_preds)

    sa_med = compute_sa(test_mae, med_mae)
    w_stat, p_val = safe_wilcoxon(err_model, err_med)
    a12 = vargha_delaney_a12(err_model, err_med)

    pred_df = pd.DataFrame(
        {
            "issuekey": te_keys,
            "Ground_Truth_SP": te_y,
            "Pred_GPT2SP_Retrain": np.round(test_preds, 6),
            "Pred_Median_Baseline": med_pred_arr,
            "Error_GPT2SP": np.round(err_model, 6),
            "Error_Median": np.round(err_med, 6),
        }
    )
    pred_path = os.path.join(seed_dir, "test_predictions.csv")
    pred_df.to_csv(pred_path, index=False)
    hf_logger.upload_result(pred_path, f"seed_{seed}/test_predictions.csv")
    hf_logger.upload_checkpoint_dir(
        ckpt_dir, f"seed_{seed}", commit_message=f"Upload best GPT2SP ckpt (epoch {best_epoch})"
    )

    print(
        f"  🎯 Test Result (seed={seed}, best_ep={best_epoch}): "
        f"GPT2SP MAE={test_mae:.4f} vs Median MAE={med_mae:.4f} | SA={sa_med:+.2f}% | p={p_val:.4e}"
    )

    return {
        "project": args.project,
        "setting": args.setting,
        "seed": seed,
        "best_epoch": best_epoch,
        "best_val_mae": round(best_val_mae, 4),
        "test_mae": round(test_mae, 4),
        "test_mdae": round(test_mdae, 4),
        "median_baseline_mae": round(med_mae, 4),
        "median_baseline_mdae": round(med_mdae, 4),
        "SA_vs_Median (%)": round(sa_med, 2),
        "Wilcoxon_W": round(w_stat, 2),
        "Wilcoxon_p": p_val,
        "A12_vs_Median": round(a12, 4),
    }


def main() -> None:
    args = parse_args()
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    run_name = args.run_name or f"gpt2sp_retrain_{args.project}_{args.setting}"

    out_dir = resolve_output_dir(args.output_dir, run_name)
    cache_dir = os.path.join(out_dir, "csv_cache")
    os.makedirs(cache_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 85)
    print(f"🚀 GPT2SP RETRAINING | project={args.project} | setting={args.setting} | seeds={seeds}")
    print(f"💻 Device: {device}")
    print("=" * 85)

    hf_logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=args.checkpoints_repo,
        run_prefix=run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    from model import build_tokenizer_and_config

    tokenizer, config = build_tokenizer_and_config("gpt2")
    data_tuple = prepare_setting_data(args, cache_dir)
    start_ts = time.time()

    summary_rows = []
    for seed in seeds:
        row = train_one_seed(seed, args, tokenizer, config, data_tuple, device, out_dir, hf_logger)
        summary_rows.append(row)

    df_summary = pd.DataFrame(summary_rows)
    summary_path = os.path.join(out_dir, "retrain_summary.csv")
    df_summary.to_csv(summary_path, index=False)
    hf_logger.upload_result(summary_path, "retrain_summary.csv", "Upload retrain summary")
    hf_logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "elapsed_sec": round(time.time() - start_ts, 2),
            "mean_test_mae": round(float(df_summary["test_mae"].mean()), 4),
            "std_test_mae": round(float(df_summary["test_mae"].std(ddof=0)), 4),
        },
    )

    print("\n✅ Retraining complete! Summary:")
    print(df_summary.to_string(index=False))


if __name__ == "__main__":
    main()
