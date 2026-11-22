"""Strategy 1: 16-project official Hugging Face checkpoint audit for GPT2SP."""

import argparse
import gc
import os
import sys
import time
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

# Allow running either from repo root (`python kaggle/run_gpt2sp_16projects.py`)
# or inside kaggle/ (`python run_gpt2sp_16projects.py`).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BENCHMARK_PROJECTS,
    DEFAULT_RESULTS_REPO_NAME,
    format_issue_texts,
    load_gpt2sp_splits,
    parse_projects_arg,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replicate GPT2SP (IEEE TSE 2023) across 16 projects using official HF checkpoints."
    )
    parser.add_argument(
        "--projects",
        type=str,
        default="all",
        help="Comma-separated project keys or 'all' (default: all).",
    )
    parser.add_argument(
        "--seed-prefix",
        type=str,
        default="0",
        help="Author checkpoint seed prefix on HF Hub (e.g. 0, 1, 2, 6, 7).",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=20,
        help="Token sequence length (default: 20 matching author's training notebook).",
    )
    parser.add_argument(
        "--include-description",
        action="store_true",
        help="Concatenate description to title (Setting 2) instead of title-only (Setting 1).",
    )
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Skip projects whose predictions already exist locally or on HF Dataset repo.",
    )
    parser.add_argument(
        "--cleanup-cache",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Delete downloaded HF pytorch_model.bin files after each project to save disk.",
    )
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def infer_texts(
    model: torch.nn.Module,
    tokenizer,
    texts: List[str],
    max_length: int,
    batch_size: int,
    device: torch.device,
) -> np.ndarray:
    """Run batched forward pass without gradients."""
    encoded = tokenizer(
        texts,
        truncation=True,
        max_length=max_length,
        padding="max_length",
        return_tensors="pt",
    )
    dataset = TensorDataset(encoded["input_ids"], encoded["attention_mask"])
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    preds: List[float] = []
    with torch.no_grad():
        for batch_ids, batch_mask in loader:
            logits = model(batch_ids.to(device), attention_mask=batch_mask.to(device))
            preds.extend(logits.cpu().numpy().tolist())
    return np.asarray(preds, dtype=np.float64)


def run_single_project(
    p_name: str,
    args: argparse.Namespace,
    tokenizer,
    config,
    device: torch.device,
    csv_cache_dir: str,
    pred_dir: str,
    hf_logger: HFExperimentLogger,
) -> Dict:
    """Evaluate one project (or load existing resumed predictions) and return metrics dict."""
    meta = BENCHMARK_PROJECTS[p_name]
    rel_pred_path = f"predictions/{p_name}_predictions.csv"
    local_pred_path = os.path.join(pred_dir, f"{p_name}_predictions.csv")

    df_pred = None
    if args.resume:
        if os.path.exists(local_pred_path):
            print(f"  ⏭️ Found local predictions for {p_name}; resuming from disk.")
            df_pred = pd.read_csv(local_pred_path)
        elif hf_logger.remote_file_exists(rel_pred_path, repo_type="dataset"):
            print(f"  ⏭️ Found remote HF predictions for {p_name}; downloading for summary.")
            dl_path = hf_logger.download_result_if_exists(rel_pred_path, pred_dir)
            if dl_path and os.path.exists(dl_path):
                df_pred = pd.read_csv(dl_path)

    if df_pred is None:
        from model import cleanup_downloaded_file, load_official_gpt2sp_checkpoint

        splits = load_gpt2sp_splits(p_name, csv_cache_dir)
        train_df, test_df = splits["train"], splits["test"]
        y_train = pd.to_numeric(train_df["storypoint"], errors="coerce").dropna().values
        y_test = pd.to_numeric(test_df["storypoint"], errors="coerce").fillna(0.0).values
        texts_test = format_issue_texts(test_df, include_description=args.include_description)

        train_median = float(np.median(y_train))
        train_mean = float(np.mean(y_train))

        repo_id = f"MickyMike/{args.seed_prefix}-GPT2SP-{p_name}"
        print(f"  📥 Loading checkpoint: {repo_id} ...")
        model, weights_path = load_official_gpt2sp_checkpoint(
            repo_id=repo_id,
            config=config,
            device=device,
            hf_token=hf_logger.token,
        )
        preds = infer_texts(model, tokenizer, texts_test, args.max_length, args.batch_size, device)

        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if args.cleanup_cache:
            cleanup_downloaded_file(weights_path)

        issue_keys = (
            test_df["issuekey"].tolist()
            if "issuekey" in test_df.columns
            else list(range(len(y_test)))
        )
        pred_med_arr = np.full(len(y_test), train_median, dtype=np.float64)
        pred_mean_arr = np.full(len(y_test), train_mean, dtype=np.float64)

        df_pred = pd.DataFrame(
            {
                "issuekey": issue_keys,
                "Ground_Truth_SP": y_test,
                "Pred_GPT2SP": np.round(preds, 6),
                "Pred_Median_Baseline": pred_med_arr,
                "Pred_Mean_Baseline": np.round(pred_mean_arr, 6),
                "Error_GPT2SP": np.round(np.abs(y_test - preds), 6),
                "Error_Median": np.round(np.abs(y_test - pred_med_arr), 6),
                "Error_Mean": np.round(np.abs(y_test - pred_mean_arr), 6),
            }
        )
        df_pred.to_csv(local_pred_path, index=False)
        hf_logger.upload_result(
            local_pred_path,
            rel_pred_path,
            commit_message=f"Add GPT2SP inference predictions for {p_name}",
        )

    y_test = df_pred["Ground_Truth_SP"].values
    preds = df_pred["Pred_GPT2SP"].values
    pred_med = df_pred["Pred_Median_Baseline"].values
    pred_mean = df_pred["Pred_Mean_Baseline"].values

    actual_mae, actual_mdae, err_gpt = compute_mae_mdae(y_test, preds)
    med_mae, med_mdae, err_med = compute_mae_mdae(y_test, pred_med)
    mean_mae, _, _ = compute_mae_mdae(y_test, pred_mean)

    sa_med = compute_sa(actual_mae, med_mae)
    w_stat, p_val = safe_wilcoxon(err_gpt, err_med)
    a12 = vargha_delaney_a12(err_gpt, err_med)

    reported_mae = meta["reported_gpt2sp"]
    repro_gap = actual_mae - reported_mae
    beats_median = actual_mae < med_mae

    print(
        f"  🎯 {meta['abbr']} | Actual MAE={actual_mae:.4f} | Paper={reported_mae:.2f} | "
        f"Real Median={med_mae:.4f} | SA={sa_med:+.2f}% | A12={a12:.3f} | p={p_val:.4e}"
    )

    return {
        "Project": p_name,
        "Abbr": meta["abbr"],
        "Name": meta["name"],
        "N_Test": len(y_test),
        "GPT2SP_Reported_MAE": reported_mae,
        "GPT2SP_Actual_MAE": round(actual_mae, 4),
        "GPT2SP_Actual_MdAE": round(actual_mdae, 4),
        "Reproduction_Gap": round(repro_gap, 4),
        "Real_Median_MAE": round(med_mae, 4),
        "Real_Median_MdAE": round(med_mdae, 4),
        "Real_Mean_MAE": round(mean_mae, 4),
        "SA_vs_Median (%)": round(sa_med, 2),
        "DeepSE_Reported_MAE": meta["reported_deepse_in_gpt2sp"],
        "Wilcoxon_W_vs_Med": round(w_stat, 2),
        "Wilcoxon_p_vs_Med": p_val,
        "A12_vs_Med": round(a12, 4),
        "Verdict": "BEATS_MEDIAN" if beats_median else "LOSES_TO_MEDIAN",
    }


def save_audit_plot(df_results: pd.DataFrame, plot_path: str) -> None:
    """Create 2-panel 300 DPI publication figure comparing MAE and SA across projects."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    x = np.arange(len(df_results))
    width = 0.28

    ax1.bar(
        x - width,
        df_results["GPT2SP_Reported_MAE"],
        width,
        label="Paper Reported MAE (TSE 2023 Table 4)",
        color="#3498db",
        alpha=0.88,
    )
    ax1.bar(
        x,
        df_results["GPT2SP_Actual_MAE"],
        width,
        label="Actual Checkpoint MAE (HF Hub)",
        color="#e74c3c",
        alpha=0.88,
    )
    ax1.bar(
        x + width,
        df_results["Real_Median_MAE"],
        width,
        label="Real Median Baseline MAE",
        color="#2ecc71",
        alpha=0.88,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_results["Abbr"], fontsize=11, fontweight="bold")
    ax1.set_ylabel("MAE (Story Points)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "(A) Replication Gap: Reported vs. Actual Checkpoint vs. Median",
        fontsize=13,
        fontweight="bold",
    )
    ax1.legend(frameon=True, fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    colors = ["#27ae60" if sa > 0 else "#e74c3c" for sa in df_results["SA_vs_Median (%)"]]
    bars = ax2.bar(x, df_results["SA_vs_Median (%)"], color=colors, alpha=0.88)
    ax2.axhline(0, color="black", linewidth=1.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_results["Abbr"], fontsize=11, fontweight="bold")
    ax2.set_ylabel("Standardized Accuracy SA (%) vs. Median", fontsize=12, fontweight="bold")
    ax2.set_title(
        "(B) Standardized Accuracy: Checkpoint Performance vs. Median Baseline",
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
    mode_tag = "full" if args.include_description else "title"
    run_name = (
        args.run_name
        or f"gpt2sp_16proj_seed{args.seed_prefix}_{mode_tag}_len{args.max_length}"
    )

    out_dir = resolve_output_dir(args.output_dir, run_name)
    csv_cache_dir = os.path.join(out_dir, "csv_cache")
    pred_dir = os.path.join(out_dir, "predictions")
    os.makedirs(csv_cache_dir, exist_ok=True)
    os.makedirs(pred_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 85)
    print(f"🚀 GPT2SP MULTI-PROJECT REPLICATION ({len(projects)} projects) | run={run_name}")
    print(f"💻 Device: {device} | Input: {mode_tag} | max_len={args.max_length}")
    print("=" * 85)

    hf_logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=None,
        run_prefix=run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    from model import build_tokenizer_and_config

    tokenizer, config = build_tokenizer_and_config("gpt2")
    start_ts = time.time()
    rows = []

    for idx, p_name in enumerate(projects, 1):
        print(f"\n[{idx}/{len(projects)}] Processing {p_name}...")
        row = run_single_project(
            p_name=p_name,
            args=args,
            tokenizer=tokenizer,
            config=config,
            device=device,
            csv_cache_dir=csv_cache_dir,
            pred_dir=pred_dir,
            hf_logger=hf_logger,
        )
        rows.append(row)

    df_results = pd.DataFrame(rows)
    df_results["Wilcoxon_p_Holm"] = holm_bonferroni(df_results["Wilcoxon_p_vs_Med"].tolist())

    summary_path = os.path.join(out_dir, "gpt2sp_16_projects_summary.csv")
    df_results.to_csv(summary_path, index=False)
    hf_logger.upload_result(
        summary_path, "gpt2sp_16_projects_summary.csv", "Upload 16-project summary"
    )

    # Project-level global statistical comparisons
    stat_rows = []
    if len(df_results) >= 2:
        w_gap, p_gap = safe_wilcoxon(
            df_results["GPT2SP_Actual_MAE"].values, df_results["GPT2SP_Reported_MAE"].values
        )
        w_med, p_med = safe_wilcoxon(
            df_results["GPT2SP_Actual_MAE"].values, df_results["Real_Median_MAE"].values
        )
        a12_global = vargha_delaney_a12(
            df_results["GPT2SP_Actual_MAE"].values, df_results["Real_Median_MAE"].values
        )
        stat_rows.extend(
            [
                {
                    "Comparison": "Actual_Checkpoint_MAE vs Paper_Reported_MAE",
                    "N_Projects": len(df_results),
                    "Mean_Diff": round(float(df_results["Reproduction_Gap"].mean()), 4),
                    "Wilcoxon_W": round(w_gap, 4),
                    "p_value": p_gap,
                    "A12": None,
                },
                {
                    "Comparison": "Actual_Checkpoint_MAE vs Real_Median_MAE",
                    "N_Projects": len(df_results),
                    "Mean_Diff": round(
                        float(
                            (df_results["GPT2SP_Actual_MAE"] - df_results["Real_Median_MAE"]).mean()
                        ),
                        4,
                    ),
                    "Wilcoxon_W": round(w_med, 4),
                    "p_value": p_med,
                    "A12": round(a12_global, 4),
                },
            ]
        )

    df_stats = pd.DataFrame(stat_rows)
    stats_path = os.path.join(out_dir, "gpt2sp_16_projects_statistical_tests.csv")
    df_stats.to_csv(stats_path, index=False)
    hf_logger.upload_result(
        stats_path, "gpt2sp_16_projects_statistical_tests.csv", "Upload global stats"
    )

    plot_path = os.path.join(out_dir, "gpt2sp_16_projects_benchmark_audit.png")
    save_audit_plot(df_results, plot_path)
    hf_logger.upload_result(
        plot_path, "gpt2sp_16_projects_benchmark_audit.png", "Upload 300 DPI audit chart"
    )

    losses = int((df_results["Verdict"] == "LOSES_TO_MEDIAN").sum())
    hf_logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "elapsed_sec": round(time.time() - start_ts, 2),
            "n_projects": len(df_results),
            "projects_losing_to_median": losses,
            "mean_reproduction_gap": round(float(df_results["Reproduction_Gap"].mean()), 4),
            "mean_sa_vs_median": round(float(df_results["SA_vs_Median (%)"].mean()), 2),
        },
    )

    print("\n" + "=" * 85)
    print(f"✅ Completed {len(df_results)} projects in {time.time() - start_ts:.1f}s")
    print(f"   • Projects losing to Median Baseline: {losses}/{len(df_results)}")
    print(f"   • Mean Reproduction Gap (Actual - Reported): {df_results['Reproduction_Gap'].mean():+.4f} SP")
    print(f"   • Mean SA vs Median Baseline: {df_results['SA_vs_Median (%)'].mean():+.2f}%")
    print(f"   • Summary saved: {summary_path}")
    if hf_logger.enabled:
        print(
            f"   • View on HF Hub: https://huggingface.co/datasets/{hf_logger.results_repo_id}/tree/main/{run_name}"
        )
    print("=" * 85)


if __name__ == "__main__":
    main()
