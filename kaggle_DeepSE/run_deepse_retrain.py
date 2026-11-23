"""Strategy 2: Controlled retraining of Deep-SE across official_pkl, final_raw, and planning_clean."""

import argparse
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BENCHMARK_PROJECTS,
    DEFAULT_CHECKPOINTS_REPO_NAME,
    DEFAULT_RESULTS_REPO_NAME,
    build_vocab_from_texts,
    load_deepse_dict,
    load_deepse_pkl_splits,
    load_deepse_splits,
    prepare_sequence_tensors,
    resolve_output_dir,
    texts_to_word_ids,
)
from hf_utils import HFExperimentLogger
from metrics import compute_mae_mdae, compute_sa, safe_wilcoxon, vargha_delaney_a12
from model import load_pretrained_lm_embedding, train_deepse_session


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrain Deep-SE under controlled settings and compare against Median Effort Baseline."
    )
    parser.add_argument("--project", type=str, default="springxd", choices=list(BENCHMARK_PROJECTS.keys()))
    parser.add_argument(
        "--setting",
        type=str,
        default="official_pkl",
        choices=["official_pkl", "final_raw", "planning_clean"],
        help="Dataset representation / temporal leakage control setting.",
    )
    parser.add_argument(
        "--vocab-source",
        type=str,
        default="auto",
        choices=["auto", "repo_dict", "train_only"],
        help="Vocabulary source for raw/clean text modes ('auto' uses repo_dict for LM pretrain, train_only for scratch).",
    )
    parser.add_argument(
        "--clean-csv",
        type=str,
        default=None,
        help="Explicit path to clean planning-time CSV (used when --setting planning_clean).",
    )
    parser.add_argument("--dim", type=int, default=50, choices=[10, 50, 100, 200])
    parser.add_argument("--vocab-size", type=int, default=500)
    parser.add_argument("--max-length", type=int, default=100)
    parser.add_argument("--hidden-layers", type=int, default=10)
    parser.add_argument("--pool", type=str, default="mean", choices=["mean", "max", "last"])
    parser.add_argument(
        "--pretrain",
        type=str,
        default="fixed_lm",
        choices=["fixed_lm", "finetune_lm", "scratch"],
    )
    parser.add_argument("--loss", type=str, default="mse", choices=["mse", "mae"])
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--seeds", type=str, default="1234", help="Comma-separated random seeds.")
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--checkpoints-repo", type=str, default=DEFAULT_CHECKPOINTS_REPO_NAME)
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def resolve_clean_csv(explicit_path: Optional[str], project_name: str) -> str:
    """Locate leakage-free planning-time CSV across repo paths."""
    candidates = [
        explicit_path,
        os.path.join("data", "clean", f"{project_name}_cleaned_dataset.csv"),
        os.path.join("docs", "draft", f"{project_name}_cleaned_dataset.csv"),
    ]
    for cand in candidates:
        if cand and os.path.exists(cand):
            return cand
    raise FileNotFoundError(
        f"Clean planning-time CSV for '{project_name}' not found in --clean-csv, data/clean/, or docs/draft/."
    )


def prepare_setting_data(
    args: argparse.Namespace,
    cache_dir: str,
) -> Dict[str, Any]:
    """Prepare tokenized sequence tensors, labels, and embedding weights for the selected setting."""
    meta = BENCHMARK_PROJECTS[args.project]

    emb_slice = None
    effective_vocab = args.vocab_size
    freeze_emb = args.pretrain == "fixed_lm"
    if args.pretrain in ("fixed_lm", "finetune_lm"):
        full_emb = load_pretrained_lm_embedding(meta["repo"], args.dim, cache_dir)
        effective_vocab = min(args.vocab_size, full_emb.shape[0])
        emb_slice = full_emb[:effective_vocab]

    if args.setting == "official_pkl":
        pkl = load_deepse_pkl_splits(args.project, cache_dir)
        tr_t, tr_d, tr_y = pkl["train_t"], pkl["train_d"], pkl["train_y"]
        va_t, va_d, va_y = pkl["val_t"], pkl["val_d"], pkl["val_y"]
        te_t, te_d, te_y = pkl["test_t"], pkl["test_d"], pkl["test_y"]
        te_keys = list(range(len(te_y)))
        resolved_vocab_source = "official_pkl"
    else:
        vocab_source = args.vocab_source
        if vocab_source == "auto":
            vocab_source = "train_only" if args.pretrain == "scratch" else "repo_dict"

        if vocab_source == "train_only" and args.pretrain in ("fixed_lm", "finetune_lm"):
            raise ValueError(
                "--vocab-source train_only cannot be paired with NCE pretrained weights "
                "(lstm2v embeddings require --vocab-source repo_dict). Pass --pretrain scratch instead."
            )

        if args.setting == "planning_clean":
            clean_path = resolve_clean_csv(args.clean_csv, args.project)
            df = pd.read_csv(clean_path)
            if "Is_GPT2SP_3526_Subset" in df.columns:
                df = df[df["Is_GPT2SP_3526_Subset"] == 1].reset_index(drop=True)
            splits_col = df["Chronological_Split"].astype(str).str.lower()
            tr_df = df[splits_col == "train"].reset_index(drop=True)
            va_df = df[splits_col.isin(["val", "valid", "validation"])].reset_index(drop=True)
            te_df = df[splits_col == "test"].reset_index(drop=True)

            tr_titles = tr_df["Clean_Title"].fillna("").astype(str).tolist()
            tr_descs = tr_df["Clean_Description"].fillna("").astype(str).tolist()
            va_titles = va_df["Clean_Title"].fillna("").astype(str).tolist()
            va_descs = va_df["Clean_Description"].fillna("").astype(str).tolist()
            te_titles = te_df["Clean_Title"].fillna("").astype(str).tolist()
            te_descs = te_df["Clean_Description"].fillna("").astype(str).tolist()

            tr_y = pd.to_numeric(tr_df["Initial_Story_Point"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            va_y = pd.to_numeric(va_df["Initial_Story_Point"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            te_y = pd.to_numeric(te_df["Initial_Story_Point"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            te_keys = te_df["Issue_Key"].tolist() if "Issue_Key" in te_df.columns else list(range(len(te_df)))
        else:
            splits = load_deepse_splits(args.project, cache_dir)
            tr_df, va_df, te_df = splits["train"], splits["val"], splits["test"]

            title_col = "title" if "title" in tr_df.columns else "Title"
            desc_col = "description" if "description" in tr_df.columns else "Description"
            tr_titles = tr_df[title_col].fillna("").astype(str).tolist()
            tr_descs = tr_df[desc_col].fillna("").astype(str).tolist()
            va_titles = va_df[title_col].fillna("").astype(str).tolist()
            va_descs = va_df[desc_col].fillna("").astype(str).tolist()
            te_titles = te_df[title_col].fillna("").astype(str).tolist()
            te_descs = te_df[desc_col].fillna("").astype(str).tolist()

            tr_y = pd.to_numeric(tr_df["storypoint"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            va_y = pd.to_numeric(va_df["storypoint"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            te_y = pd.to_numeric(te_df["storypoint"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float32)
            te_keys = te_df["issuekey"].tolist() if "issuekey" in te_df.columns else list(range(len(te_df)))

        if vocab_source == "repo_dict":
            word_dict = load_deepse_dict(meta["repo"], cache_dir)
        else:
            word_dict = build_vocab_from_texts(tr_titles + tr_descs)

        tr_t = texts_to_word_ids(tr_titles, word_dict)
        tr_d = texts_to_word_ids(tr_descs, word_dict)
        va_t = texts_to_word_ids(va_titles, word_dict)
        va_d = texts_to_word_ids(va_descs, word_dict)
        te_t = texts_to_word_ids(te_titles, word_dict)
        te_d = texts_to_word_ids(te_descs, word_dict)
        resolved_vocab_source = vocab_source

    train_tensors = prepare_sequence_tensors(
        tr_t, tr_d, vocab_size=effective_vocab, max_len=args.max_length
    )
    val_tensors = prepare_sequence_tensors(
        va_t, va_d, vocab_size=effective_vocab, max_len=args.max_length
    )
    test_tensors = prepare_sequence_tensors(
        te_t, te_d, vocab_size=effective_vocab, max_len=args.max_length
    )

    return {
        "train_tensors": train_tensors,
        "train_y": tr_y,
        "val_tensors": val_tensors,
        "val_y": va_y,
        "test_tensors": test_tensors,
        "test_y": te_y,
        "test_keys": te_keys,
        "emb_slice": emb_slice,
        "effective_vocab": effective_vocab,
        "freeze_emb": freeze_emb,
        "resolved_vocab_source": resolved_vocab_source,
    }


def save_loss_curve(df_hist: pd.DataFrame, out_path: str, title: str, loss_name: str) -> None:
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(
        df_hist["epoch"],
        df_hist["train_loss"],
        label=f"Train {loss_name.upper()} Loss",
        color="#3498db",
        marker="o",
        markersize=2.5,
    )
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel(f"Train {loss_name.upper()} Loss", color="#3498db")
    ax1.tick_params(axis="y", labelcolor="#3498db")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(
        df_hist["epoch"],
        df_hist["val_mae"],
        label="Validation MAE",
        color="#e74c3c",
        marker="s",
        markersize=2.5,
    )
    ax2.set_ylabel("Validation MAE (Story Points)", color="#e74c3c")
    ax2.tick_params(axis="y", labelcolor="#e74c3c")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right", frameon=True)
    ax1.set_title(title)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close(fig)


def run_one_seed(
    seed: int,
    args: argparse.Namespace,
    bundle: Dict[str, Any],
    device: torch.device,
    out_dir: str,
    hf_logger: HFExperimentLogger,
) -> Dict[str, Any]:
    seed_dir = os.path.join(out_dir, f"seed_{seed}")
    ckpt_dir = os.path.join(seed_dir, "best_checkpoint")
    fig_dir = os.path.join(out_dir, "figures")
    os.makedirs(ckpt_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    train_y = bundle["train_y"]
    val_y = bundle["val_y"]
    test_y = bundle["test_y"]

    print(
        f"\n🏋️ Seed {seed} | train={len(train_y)} val={len(val_y)} test={len(test_y)} | "
        f"vocab_src={bundle['resolved_vocab_source']} (V={bundle['effective_vocab']}) | "
        f"pretrain={args.pretrain} dim={args.dim} epochs={args.epochs}"
    )

    train_out = train_deepse_session(
        train_tensors=bundle["train_tensors"],
        train_y=train_y,
        val_tensors=bundle["val_tensors"],
        val_y=val_y,
        test_tensors=bundle["test_tensors"],
        test_y=test_y,
        vocab_size=bundle["effective_vocab"],
        emb_dim=args.dim,
        hidden_layers=args.hidden_layers,
        pool_mode=args.pool,
        pretrained_embedding=bundle["emb_slice"],
        freeze_embedding=bundle["freeze_emb"],
        loss_name=args.loss,
        lr=args.lr,
        batch_size=args.batch_size,
        epochs=args.epochs,
        seed=seed,
        device=device,
        ckpt_dir=ckpt_dir,
        verbose=True,
    )

    df_hist = pd.DataFrame(train_out["history"])
    hist_path = os.path.join(seed_dir, "history.csv")
    df_hist.to_csv(hist_path, index=False)

    fig_dir = os.path.join(out_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    curve_path = os.path.join(fig_dir, f"loss_curve_seed_{seed}.png")
    if len(df_hist) > 0:
        save_loss_curve(
            df_hist,
            curve_path,
            f"Deep-SE Retrain ({args.project} | {args.setting} | {args.pretrain} | seed={seed})",
            args.loss,
        )

    test_mae = train_out["test_mae"]
    test_mdae = train_out["test_mdae"]
    test_preds = train_out["test_preds"]
    te_y_f64 = np.asarray(test_y, dtype=np.float64)

    train_median = float(np.median(train_y))
    train_mean = float(np.mean(train_y))
    med_pred_arr = np.full(len(te_y_f64), train_median, dtype=np.float64)
    mean_pred_arr = np.full(len(te_y_f64), train_mean, dtype=np.float64)

    med_mae, med_mdae, err_med = compute_mae_mdae(te_y_f64, med_pred_arr)
    mean_mae, _, _ = compute_mae_mdae(te_y_f64, mean_pred_arr)
    err_model = np.abs(te_y_f64 - test_preds)

    sa_med = compute_sa(test_mae, med_mae)
    w_stat, p_val = safe_wilcoxon(err_model, err_med)
    a12 = vargha_delaney_a12(err_model, err_med)

    pred_df = pd.DataFrame(
        {
            "issuekey": bundle["test_keys"],
            "Ground_Truth_SP": te_y_f64,
            "Pred_DeepSE_Retrain": np.round(test_preds, 6),
            "Pred_Median_Baseline": med_pred_arr,
            "Pred_Mean_Baseline": np.round(mean_pred_arr, 6),
            "Error_DeepSE": np.round(err_model, 6),
            "Error_Median": np.round(err_med, 6),
        }
    )
    pred_path = os.path.join(seed_dir, "predictions.csv")
    pred_df.to_csv(pred_path, index=False)

    batch_items = [
        (hist_path, f"seed_{seed}/history.csv"),
        (pred_path, f"seed_{seed}/predictions.csv"),
    ]
    if len(df_hist) > 0:
        batch_items.append((curve_path, f"figures/loss_curve_seed_{seed}.png"))
    hf_logger.upload_results_batch(
        batch_items,
        commit_message=f"Upload Deep-SE retrain artifacts for seed {seed}",
    )
    hf_logger.upload_checkpoint_dir(
        ckpt_dir,
        f"seed_{seed}",
        commit_message=f"Upload best Deep-SE ckpt (epoch {train_out['best_epoch']})",
    )

    print(
        f"  🎯 Test Result (seed={seed}, best_ep={train_out['best_epoch']}): "
        f"Deep-SE MAE={test_mae:.4f} vs Median MAE={med_mae:.4f} | "
        f"SA={sa_med:+.2f}% | A12={a12:.3f} | p={p_val:.4e}"
    )

    return {
        "project": args.project,
        "setting": args.setting,
        "pretrain": args.pretrain,
        "vocab_source": bundle["resolved_vocab_source"],
        "dim": args.dim,
        "seed": seed,
        "best_epoch": train_out["best_epoch"],
        "best_val_mae": round(train_out["best_val_mae"], 4),
        "test_mae": round(test_mae, 4),
        "test_mdae": round(test_mdae, 4),
        "median_baseline_mae": round(med_mae, 4),
        "median_baseline_mdae": round(med_mdae, 4),
        "mean_baseline_mae": round(mean_mae, 4),
        "SA_vs_Median (%)": round(sa_med, 2),
        "Wilcoxon_W": round(w_stat, 2),
        "Wilcoxon_p": p_val,
        "A12_vs_Median": round(a12, 4),
    }


def main() -> None:
    args = parse_args()
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    run_name = (
        args.run_name
        or f"experiments/deepse/retrain/{args.project}_{args.setting}_{args.pretrain}_dim{args.dim}"
    )

    out_dir = resolve_output_dir(args.output_dir, run_name)
    cache_dir = os.path.join(out_dir, "deepse_cache")
    os.makedirs(cache_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 85)
    print(
        f"🚀 DEEP-SE RETRAINING | project={args.project} | setting={args.setting} | "
        f"pretrain={args.pretrain} | seeds={seeds}"
    )
    print(f"💻 Device: {device}")
    print("=" * 85)

    hf_logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=args.checkpoints_repo,
        run_prefix=run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    bundle = prepare_setting_data(args, cache_dir)
    start_ts = time.time()

    summary_rows = [
        run_one_seed(seed, args, bundle, device, out_dir, hf_logger) for seed in seeds
    ]

    df_summary = pd.DataFrame(summary_rows)
    summary_path = os.path.join(out_dir, "summary.csv")
    df_summary.to_csv(summary_path, index=False)
    meta_path = hf_logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "elapsed_sec": round(time.time() - start_ts, 2),
            "vocab_source_resolved": bundle["resolved_vocab_source"],
            "effective_vocab_size": bundle["effective_vocab"],
            "mean_test_mae": round(float(df_summary["test_mae"].mean()), 4),
            "std_test_mae": round(float(df_summary["test_mae"].std(ddof=0)), 4),
        },
        upload=False,
    )
    hf_logger.upload_results_batch(
        [(summary_path, "summary.csv"), (meta_path, "metadata.json")],
        commit_message=f"Finalize {run_name} summary & metadata",
    )

    print("\n✅ Deep-SE Retraining complete! Summary:")
    print(df_summary.to_string(index=False))


if __name__ == "__main__":
    main()
