"""Strategy 1: 16-project Deep-SE (Choetkiertikul et al., IEEE TSE 2019) PyTorch replication & audit."""

import argparse
import gc
import os
import sys
import time
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

# Allow running either from repo root (`python kaggle_DeepSE/run_deepse_16projects.py`)
# or inside kaggle_DeepSE/ (`python run_deepse_16projects.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BENCHMARK_PROJECTS,
    DEFAULT_CHECKPOINTS_REPO_NAME,
    DEFAULT_RESULTS_REPO_NAME,
    load_deepse_pkl_splits,
    parse_projects_arg,
    prepare_sequence_tensors,
    resolve_output_dir,
)
from hf_utils import HFExperimentLogger
from metrics import (
    compute_mae_mdae,
    compute_sa,
    holm_bonferroni,
    safe_wilcoxon,
    vargha_delaney_a12,
)
from model import load_pretrained_lm_embedding, train_deepse_session


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replicate Deep-SE (IEEE TSE 2019) across 16 benchmark projects in PyTorch."
    )
    parser.add_argument(
        "--projects",
        type=str,
        default="all",
        help="Comma-separated project keys or 'all' (default: all).",
    )
    parser.add_argument(
        "--dim",
        type=int,
        default=50,
        choices=[10, 50, 100, 200],
        help="Embedding / LSTM / Highway hidden dimension (default: 50).",
    )
    parser.add_argument(
        "--vocab-size",
        type=int,
        default=500,
        help="Vocabulary cutoff matching Deep-SE prepare_data.py (default: 500).",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=100,
        help="Maximum sequence length for title and description (default: 100).",
    )
    parser.add_argument(
        "--hidden-layers",
        type=int,
        default=10,
        help="Number of recurrent Highway passes matching exp_script/create_highway (default: 10).",
    )
    parser.add_argument(
        "--pool",
        type=str,
        default="mean",
        choices=["mean", "max", "last"],
        help="Sequence pooling mode (default: mean).",
    )
    parser.add_argument(
        "--pretrain",
        type=str,
        default="fixed_lm",
        choices=["fixed_lm", "finetune_lm", "scratch"],
        help="Embedding initialization mode (default: fixed_lm using author NCE lstm2v HDF5).",
    )
    parser.add_argument(
        "--loss",
        type=str,
        default="mse",
        choices=["mse", "mae"],
        help="Training objective (default: mse matching training.py).",
    )
    parser.add_argument("--lr", type=float, default=0.01, help="RMSprop learning rate (default: 0.01).")
    parser.add_argument("--batch-size", type=int, default=100, help="Mini-batch size (default: 100).")
    parser.add_argument("--epochs", type=int, default=300, help="Maximum epochs before early stop (default: 300).")
    parser.add_argument("--seed", type=int, default=1234, help="Random seed matching prepare_data.py (default: 1234).")
    parser.add_argument(
        "--upload-checkpoints",
        action="store_true",
        help="Push per-project best PyTorch checkpoints to HF Model repo.",
    )
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Skip projects whose predictions already exist locally or on HF Dataset repo.",
    )
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--checkpoints-repo", type=str, default=DEFAULT_CHECKPOINTS_REPO_NAME)
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def run_single_project(
    p_name: str,
    args: argparse.Namespace,
    device: torch.device,
    data_cache_dir: str,
    pred_dir: str,
    ckpt_root: str,
    resume_cache_dir: str,
    emb_cache: Dict[str, np.ndarray],
    hf_logger: HFExperimentLogger,
) -> Dict[str, Any]:
    """Train & evaluate Deep-SE on one project (or load resumed predictions)."""
    meta = BENCHMARK_PROJECTS[p_name]
    rel_pred_path = f"predictions/{p_name}.csv"
    local_pred_path = os.path.join(pred_dir, f"{p_name}.csv")

    df_pred = None
    if args.resume:
        if os.path.exists(local_pred_path):
            print(f"  ⏭️ Found local predictions for {p_name}; resuming from disk.")
            df_pred = pd.read_csv(local_pred_path)
        elif hf_logger.remote_file_exists(rel_pred_path, repo_type="dataset"):
            print(f"  ⏭️ Found remote HF predictions for {p_name}; downloading for summary.")
            dl_path = hf_logger.download_result_if_exists(rel_pred_path, resume_cache_dir)
            if dl_path and os.path.exists(dl_path):
                df_pred = pd.read_csv(dl_path)
                df_pred.to_csv(local_pred_path, index=False)

    best_epoch = None
    if df_pred is None:
        pkl_splits = load_deepse_pkl_splits(p_name, data_cache_dir)
        train_y = pkl_splits["train_y"]
        val_y = pkl_splits["val_y"]
        test_y = pkl_splits["test_y"]

        emb_slice = None
        effective_vocab = args.vocab_size
        freeze_emb = args.pretrain == "fixed_lm"
        if args.pretrain in ("fixed_lm", "finetune_lm"):
            repo_name = meta["repo"]
            if repo_name not in emb_cache:
                print(f"  📥 Loading NCE pretrained embedding: lstm2v_{repo_name}_dim{args.dim}.hdf5 ...")
                emb_cache[repo_name] = load_pretrained_lm_embedding(
                    repo_name=repo_name,
                    emb_dim=args.dim,
                    cache_dir=data_cache_dir,
                )
            full_emb = emb_cache[repo_name]
            effective_vocab = min(args.vocab_size, full_emb.shape[0])
            emb_slice = full_emb[:effective_vocab]

        train_tensors = prepare_sequence_tensors(
            pkl_splits["train_t"], pkl_splits["train_d"], vocab_size=effective_vocab, max_len=args.max_length
        )
        val_tensors = prepare_sequence_tensors(
            pkl_splits["val_t"], pkl_splits["val_d"], vocab_size=effective_vocab, max_len=args.max_length
        )
        test_tensors = prepare_sequence_tensors(
            pkl_splits["test_t"], pkl_splits["test_d"], vocab_size=effective_vocab, max_len=args.max_length
        )

        print(
            f"  🏋️ Training {p_name} ({meta['repo']}) | train={len(train_y)} val={len(val_y)} "
            f"test={len(test_y)} | pretrain={args.pretrain} dim={args.dim}"
        )
        proj_ckpt_dir = os.path.join(ckpt_root, p_name)
        train_out = train_deepse_session(
            train_tensors=train_tensors,
            train_y=train_y,
            val_tensors=val_tensors,
            val_y=val_y,
            test_tensors=test_tensors,
            test_y=test_y,
            vocab_size=effective_vocab,
            emb_dim=args.dim,
            hidden_layers=args.hidden_layers,
            pool_mode=args.pool,
            pretrained_embedding=emb_slice,
            freeze_embedding=freeze_emb,
            loss_name=args.loss,
            lr=args.lr,
            batch_size=args.batch_size,
            epochs=args.epochs,
            seed=args.seed,
            device=device,
            ckpt_dir=proj_ckpt_dir,
            verbose=False,
        )
        best_epoch = train_out["best_epoch"]
        preds = train_out["test_preds"]

        train_median = float(np.median(train_y))
        train_mean = float(np.mean(train_y))
        pred_med_arr = np.full(len(test_y), train_median, dtype=np.float64)
        pred_mean_arr = np.full(len(test_y), train_mean, dtype=np.float64)
        pred_plus1_arr = np.full(len(test_y), 1.0 + train_mean, dtype=np.float64)

        df_pred = pd.DataFrame(
            {
                "issue_idx": np.arange(len(test_y)),
                "Ground_Truth_SP": np.asarray(test_y, dtype=np.float64),
                "Pred_DeepSE": np.round(preds, 6),
                "Pred_Median_Baseline": pred_med_arr,
                "Pred_Mean_Baseline": np.round(pred_mean_arr, 6),
                "Pred_Code_Plus1_Guess": np.round(pred_plus1_arr, 6),
                "Error_DeepSE": np.round(np.abs(test_y - preds), 6),
                "Error_Median": np.round(np.abs(test_y - pred_med_arr), 6),
                "Error_Mean": np.round(np.abs(test_y - pred_mean_arr), 6),
            }
        )
        df_pred.to_csv(local_pred_path, index=False)
        hf_logger.upload_result(
            local_pred_path,
            rel_pred_path,
            commit_message=f"Add Deep-SE test predictions for {p_name}",
        )
        if args.upload_checkpoints:
            hf_logger.upload_checkpoint_dir(
                proj_ckpt_dir,
                p_name,
                commit_message=f"Upload Deep-SE best checkpoint for {p_name} (ep {best_epoch})",
            )

        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    y_test = df_pred["Ground_Truth_SP"].to_numpy(dtype=np.float64)
    preds = df_pred["Pred_DeepSE"].to_numpy(dtype=np.float64)
    pred_med = df_pred["Pred_Median_Baseline"].to_numpy(dtype=np.float64)
    pred_mean = df_pred["Pred_Mean_Baseline"].to_numpy(dtype=np.float64)
    pred_plus1 = df_pred["Pred_Code_Plus1_Guess"].to_numpy(dtype=np.float64)

    actual_mae, actual_mdae, err_deepse = compute_mae_mdae(y_test, preds)
    med_mae, med_mdae, err_med = compute_mae_mdae(y_test, pred_med)
    mean_mae, _, _ = compute_mae_mdae(y_test, pred_mean)
    plus1_mae, _, _ = compute_mae_mdae(y_test, pred_plus1)

    sa_med = compute_sa(actual_mae, med_mae)
    sa_mean = compute_sa(actual_mae, mean_mae)
    sa_plus1 = compute_sa(actual_mae, plus1_mae)
    w_stat, p_val = safe_wilcoxon(err_deepse, err_med)
    a12 = vargha_delaney_a12(err_deepse, err_med)

    reported_mae = meta["reported_deepse"]
    delta_paper = actual_mae - reported_mae
    med_inflation = meta["rep_median"] - med_mae
    beats_median = actual_mae < med_mae

    print(
        f"  🎯 {meta['abbr']} | Replicated MAE={actual_mae:.4f} (ep={best_epoch}) | "
        f"Paper={reported_mae:.2f} | RealMed={med_mae:.4f} | SA_Med={sa_med:+.2f}% | "
        f"A12={a12:.3f} | p={p_val:.4e}"
    )

    return {
        "Project": p_name,
        "Abbr": meta["abbr"],
        "Name": meta["name"],
        "Repo": meta["repo"],
        "N_Test": len(y_test),
        "Best_Epoch": best_epoch,
        "DeepSE_Reported_MAE": reported_mae,
        "DeepSE_Actual_MAE": round(actual_mae, 4),
        "DeepSE_Actual_MdAE": round(actual_mdae, 4),
        "Delta_vs_Paper_DeepSE": round(delta_paper, 4),
        "Paper_Rep_Median_MAE": meta["rep_median"],
        "Real_Median_MAE": round(med_mae, 4),
        "Real_Median_MdAE": round(med_mdae, 4),
        "Delta_Paper_Med_vs_Real_Med": round(med_inflation, 4),
        "Real_Mean_MAE": round(mean_mae, 4),
        "Code_Plus1_Guess_MAE": round(plus1_mae, 4),
        "SA_Paper_Reported (%)": meta["reported_deepse_sa"],
        "SA_vs_Real_Median (%)": round(sa_med, 2),
        "SA_vs_Real_Mean (%)": round(sa_mean, 2),
        "SA_Code_Plus1 (%)": round(sa_plus1, 2),
        "Wilcoxon_W_vs_Med": round(w_stat, 2),
        "Wilcoxon_p_vs_Med": p_val,
        "A12_vs_Med": round(a12, 4),
        "Verdict": "BEATS_MEDIAN" if beats_median else "LOSES_TO_MEDIAN",
    }


def save_deepse_benchmark_plot(df_results: pd.DataFrame, plot_path: str) -> None:
    """Create 2-panel 300 DPI publication figure comparing Paper/Replicated Deep-SE vs Real Median."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    x = np.arange(len(df_results))
    width = 0.28

    ax1.bar(
        x - width,
        df_results["DeepSE_Reported_MAE"],
        width,
        label="Paper Deep-SE (TSE 2019 Table II)",
        color="#3498db",
        alpha=0.88,
    )
    ax1.bar(
        x,
        df_results["DeepSE_Actual_MAE"],
        width,
        label="Replicated Deep-SE (PyTorch)",
        color="#e74c3c",
        alpha=0.88,
    )
    ax1.bar(
        x + width,
        df_results["Real_Median_MAE"],
        width,
        label="Real Median Baseline",
        color="#2ecc71",
        alpha=0.88,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_results["Abbr"], fontsize=11, fontweight="bold")
    ax1.set_ylabel("MAE (Story Points)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "(A) Deep-SE Replication: Paper vs. PyTorch vs. Real Median",
        fontsize=13,
        fontweight="bold",
    )
    ax1.legend(frameon=True, fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    colors = ["#27ae60" if sa > 0 else "#e74c3c" for sa in df_results["SA_vs_Real_Median (%)"]]
    bars = ax2.bar(x, df_results["SA_vs_Real_Median (%)"], color=colors, alpha=0.88)
    ax2.axhline(0, color="black", linewidth=1.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_results["Abbr"], fontsize=11, fontweight="bold")
    ax2.set_ylabel("Standardized Accuracy SA (%) vs. Real Median", fontsize=12, fontweight="bold")
    ax2.set_title(
        "(B) Standardized Accuracy: Replicated Deep-SE vs. Honest Median Baseline",
        fontsize=13,
        fontweight="bold",
    )
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        va = "bottom" if yval >= 0 else "top"
        ax2.annotate(
            f"{yval:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, yval),
            xytext=(0, 3 if yval >= 0 else -3),
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=8,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    projects = parse_projects_arg(args.projects)
    run_name = (
        args.run_name
        or f"experiments/deepse/replication/{args.pretrain}_dim{args.dim}_seed{args.seed}"
    )

    out_dir = resolve_output_dir(args.output_dir, run_name)
    data_cache_dir = os.path.join(out_dir, "deepse_cache")
    pred_dir = os.path.join(out_dir, "predictions")
    fig_dir = os.path.join(out_dir, "figures")
    ckpt_root = os.path.join(out_dir, "checkpoints")
    resume_cache_dir = os.path.join(out_dir, "hf_resume_cache")
    os.makedirs(data_cache_dir, exist_ok=True)
    os.makedirs(pred_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(ckpt_root, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 85)
    print(f"🚀 DEEP-SE 16-PROJECT REPLICATION ({len(projects)} projects) | run={run_name}")
    print(
        f"💻 Device: {device} | pretrain={args.pretrain} | dim={args.dim} | "
        f"vocab={args.vocab_size} | len={args.max_length} | hdl={args.hidden_layers}"
    )
    print("=" * 85)

    hf_logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=args.checkpoints_repo if args.upload_checkpoints else None,
        run_prefix=run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    start_ts = time.time()
    emb_cache: Dict[str, np.ndarray] = {}
    rows: List[Dict[str, Any]] = []

    for idx, p_name in enumerate(projects, 1):
        print(f"\n[{idx}/{len(projects)}] Processing {p_name}...")
        row = run_single_project(
            p_name=p_name,
            args=args,
            device=device,
            data_cache_dir=data_cache_dir,
            pred_dir=pred_dir,
            ckpt_root=ckpt_root,
            resume_cache_dir=resume_cache_dir,
            emb_cache=emb_cache,
            hf_logger=hf_logger,
        )
        rows.append(row)

    df_results = pd.DataFrame(rows)
    df_results["Wilcoxon_p_Holm"] = holm_bonferroni(df_results["Wilcoxon_p_vs_Med"].tolist())

    summary_path = os.path.join(out_dir, "summary.csv")
    df_results.to_csv(summary_path, index=False)

    stat_rows = []
    if len(df_results) >= 2:
        comparisons = [
            (
                "DeepSE_Actual_MAE vs Real_Median_MAE",
                df_results["DeepSE_Actual_MAE"].to_numpy(dtype=np.float64),
                df_results["Real_Median_MAE"].to_numpy(dtype=np.float64),
                True,
            ),
            (
                "DeepSE_Actual_MAE vs Paper_Reported_DeepSE_MAE",
                df_results["DeepSE_Actual_MAE"].to_numpy(dtype=np.float64),
                df_results["DeepSE_Reported_MAE"].to_numpy(dtype=np.float64),
                False,
            ),
            (
                "Paper_Reported_Median_MAE vs Real_Median_MAE",
                df_results["Paper_Rep_Median_MAE"].to_numpy(dtype=np.float64),
                df_results["Real_Median_MAE"].to_numpy(dtype=np.float64),
                False,
            ),
        ]
        for label, vec_a, vec_b, include_a12 in comparisons:
            w_val, p_val = safe_wilcoxon(vec_a, vec_b)
            a12_val = round(vargha_delaney_a12(vec_a, vec_b), 4) if include_a12 else None
            stat_rows.append(
                {
                    "Comparison": label,
                    "N_Projects": len(df_results),
                    "Mean_Diff": round(float(np.mean(vec_a - vec_b)), 4),
                    "Wilcoxon_W": round(w_val, 4),
                    "p_value": p_val,
                    "A12": a12_val,
                }
            )

    df_stats = pd.DataFrame(stat_rows)
    stats_path = os.path.join(out_dir, "stat_tests.csv")
    df_stats.to_csv(stats_path, index=False)

    plot_path = os.path.join(fig_dir, "benchmark_audit.png")
    save_deepse_benchmark_plot(df_results, plot_path)

    losses = int((df_results["Verdict"] == "LOSES_TO_MEDIAN").sum())
    meta_path = hf_logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "elapsed_sec": round(time.time() - start_ts, 2),
            "n_projects": len(df_results),
            "projects_losing_to_median": losses,
            "mean_delta_vs_paper_deepse": round(float(df_results["Delta_vs_Paper_DeepSE"].mean()), 4),
            "mean_sa_vs_real_median": round(float(df_results["SA_vs_Real_Median (%)"].mean()), 2),
        },
        upload=False,
    )
    hf_logger.upload_results_batch(
        [
            (summary_path, "summary.csv"),
            (stats_path, "stat_tests.csv"),
            (plot_path, "figures/benchmark_audit.png"),
            (meta_path, "metadata.json"),
        ],
        commit_message=f"Finalize {run_name} summary, stat tests, figure & metadata",
    )

    print("\n" + "=" * 85)
    print(f"✅ Completed {len(df_results)} projects in {time.time() - start_ts:.1f}s")
    print(f"   • Projects losing to Median Baseline: {losses}/{len(df_results)}")
    print(f"   • Mean Delta (Actual - Paper DeepSE): {df_results['Delta_vs_Paper_DeepSE'].mean():+.4f} SP")
    print(f"   • Mean SA vs Real Median Baseline: {df_results['SA_vs_Real_Median (%)'].mean():+.2f}%")
    print(f"   • Summary saved: {summary_path}")
    if hf_logger.enabled:
        print(
            f"   • View on HF Hub: https://huggingface.co/datasets/{hf_logger.results_repo_id}/tree/main/{run_name}"
        )
    print("=" * 85)


if __name__ == "__main__":
    main()
