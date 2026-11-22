"""Deep-SE (Choetkiertikul et al., IEEE TSE 2019) 16-project baseline inflation & +1.0 audit."""

import argparse
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BENCHMARK_PROJECTS,
    DEFAULT_RESULTS_REPO_NAME,
    load_deepse_splits,
    parse_projects_arg,
    resolve_output_dir,
)
from hf_utils import HFExperimentLogger
from metrics import compute_mae_mdae, compute_sa, safe_wilcoxon, vargha_delaney_a12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Deep-SE (IEEE TSE 2019) Table II baselines and create_model.py +1.0 SA bias."
    )
    parser.add_argument("--projects", type=str, default="all")
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--run-name", type=str, default="deepse_16projects_audit")
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def save_deepse_plot(df_audit: pd.DataFrame, plot_path: str) -> None:
    """Create 2-panel 300 DPI figure showing Reported Median inflation and real Deep-SE margin."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    x = np.arange(len(df_audit))
    width = 0.35

    ax1.bar(
        x - width / 2,
        df_audit["Rep_Med_MAE"],
        width,
        label="Reported Median (Paper Table II)",
        color="#e74c3c",
        alpha=0.88,
    )
    ax1.bar(
        x + width / 2,
        df_audit["Real_Med_MAE"],
        width,
        label="Real Median (Test Set)",
        color="#2ecc71",
        alpha=0.88,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_audit["Abbr"], fontsize=11, fontweight="bold")
    ax1.set_ylabel("MAE (Story Points)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "(A) Baseline Inflation: Reported Median vs. Real Median (16 Projects)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.legend(frameon=True, fontsize=11)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    colors = [
        "#27ae60" if g > 0.1 else ("#e74c3c" if g < 0 else "#f39c12")
        for g in df_audit["Real_Gain_vs_Med"]
    ]
    bars = ax2.bar(x, df_audit["Real_Gain_vs_Med"], color=colors, alpha=0.88)
    ax2.axhline(0, color="black", linewidth=1.2)
    ax2.axhline(0.1, color="gray", linewidth=1.0, linestyle="--", label="Negligible threshold (0.1 SP)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_audit["Abbr"], fontsize=11, fontweight="bold")
    ax2.set_ylabel("Delta MAE (Real Median - LD-RNN)", fontsize=12, fontweight="bold")
    ax2.set_title(
        "(B) Real Margin of Deep-SE over Honest Median Baseline",
        fontsize=13,
        fontweight="bold",
    )
    ax2.legend(frameon=True, fontsize=11)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        va = "bottom" if yval >= 0 else "top"
        ax2.annotate(
            f"{yval:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, yval),
            xytext=(0, 3 if yval >= 0 else -3),
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=9,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    projects = parse_projects_arg(args.projects)
    out_dir = resolve_output_dir(args.output_dir, args.run_name)
    cache_dir = os.path.join(out_dir, "deepse_cache")
    os.makedirs(cache_dir, exist_ok=True)

    print("=" * 85)
    print(f"🚀 DEEP-SE 16-PROJECT BASELINE & CODE-BIAS AUDIT ({len(projects)} projects)")
    print("=" * 85)

    hf_logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=None,
        run_prefix=args.run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    start_ts = time.time()
    audit_rows = []

    for p in projects:
        meta = BENCHMARK_PROJECTS[p]
        splits = load_deepse_splits(p, cache_dir)
        y_train = pd.to_numeric(splits["train"]["storypoint"], errors="coerce").dropna().values
        y_test = pd.to_numeric(splits["test"]["storypoint"], errors="coerce").dropna().values

        train_mean = float(np.mean(y_train))
        train_med = float(np.median(y_train))

        real_mean_mae, _, _ = compute_mae_mdae(y_test, np.full(len(y_test), train_mean))
        real_med_mae, _, _ = compute_mae_mdae(y_test, np.full(len(y_test), train_med))
        # Audit of create_model.py line 114: y_pred_guess = numpy.ones(...) + numpy.mean(train_label)
        biased_guess_mae, _, _ = compute_mae_mdae(y_test, np.full(len(y_test), 1.0 + train_mean))

        ld_rnn = meta["reported_deepse"]
        med_inflation = meta["rep_median"] - real_med_mae
        gain_vs_med = real_med_mae - ld_rnn

        sa_honest_med = compute_sa(ld_rnn, real_med_mae)
        sa_honest_mean = compute_sa(ld_rnn, real_mean_mae)
        sa_code_plus1 = compute_sa(ld_rnn, biased_guess_mae)

        if real_med_mae <= ld_rnn:
            flag = "MEDIAN_BEATS_DEEPSE"
        elif abs(gain_vs_med) <= 0.10:
            flag = "NEGLIGIBLE_<=0.1"
        else:
            flag = "NORMAL"

        print(
            f"  ✓ {meta['abbr']} ({p:<18}) | LD-RNN={ld_rnn:.2f} | RepMed={meta['rep_median']:.2f} | "
            f"RealMed={real_med_mae:.4f} | Inf={med_inflation:+.4f} | SA_Rep={meta['reported_deepse_sa']:.1f}% | "
            f"SA_HonestMed={sa_honest_med:+.2f}% [{flag}]"
        )

        audit_rows.append(
            {
                "Project": p,
                "Abbr": meta["abbr"],
                "N_Test": len(y_test),
                "LD_RNN_MAE": ld_rnn,
                "Rep_Med_MAE": meta["rep_median"],
                "Real_Med_MAE": round(real_med_mae, 4),
                "Med_Inflation": round(med_inflation, 4),
                "Rep_Mean_MAE": meta["rep_mean"],
                "Real_Mean_MAE": round(real_mean_mae, 4),
                "Code_Plus1_Guess_MAE": round(biased_guess_mae, 4),
                "Real_Gain_vs_Med": round(gain_vs_med, 4),
                "SA_Reported (%)": meta["reported_deepse_sa"],
                "SA_Code_+1 (%)": round(sa_code_plus1, 2),
                "SA_Honest_Mean (%)": round(sa_honest_mean, 2),
                "SA_Honest_Med (%)": round(sa_honest_med, 2),
                "SA_Drop_vs_Med": round(meta["reported_deepse_sa"] - sa_honest_med, 2),
                "Flag_Anomaly": flag,
            }
        )

    df_audit = pd.DataFrame(audit_rows)
    w_inf, p_inf = safe_wilcoxon(df_audit["Rep_Med_MAE"], df_audit["Real_Med_MAE"])
    w_gain, p_gain = safe_wilcoxon(df_audit["LD_RNN_MAE"], df_audit["Real_Med_MAE"])
    a12_gain = vargha_delaney_a12(df_audit["LD_RNN_MAE"], df_audit["Real_Med_MAE"])

    csv_path = os.path.join(out_dir, "deep_se_16_projects_empirical_audit.csv")
    df_audit.to_csv(csv_path, index=False)
    hf_logger.upload_result(
        csv_path, "deep_se_16_projects_empirical_audit.csv", "Upload Deep-SE 16-project audit CSV"
    )

    plot_path = os.path.join(out_dir, "deep_se_baseline_inflation_audit.png")
    save_deepse_plot(df_audit, plot_path)
    hf_logger.upload_result(
        plot_path, "deep_se_baseline_inflation_audit.png", "Upload Deep-SE audit figure"
    )

    inflated_n = int((df_audit["Med_Inflation"] > 0).sum())
    hf_logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "elapsed_sec": round(time.time() - start_ts, 2),
            "inflated_median_projects": inflated_n,
            "mean_median_inflation": round(float(df_audit["Med_Inflation"].mean()), 4),
            "wilcoxon_inflation_p": p_inf,
            "wilcoxon_gain_p": p_gain,
            "a12_ld_rnn_vs_real_median": round(a12_gain, 4),
        },
    )

    print("\n" + "=" * 85)
    print(f"✅ Deep-SE Audit Complete | Inflated Medians: {inflated_n}/{len(df_audit)}")
    print(f"   • Mean SA drop (Reported - Honest Median): {df_audit['SA_Drop_vs_Med'].mean():.2f}%")
    print(f"   • Wilcoxon Inflation p={p_inf:.4f} | LD-RNN vs Real Med A12={a12_gain:.4f}, p={p_gain:.4e}")
    print(f"   • Saved: {csv_path}")
    print("=" * 85)


if __name__ == "__main__":
    main()
