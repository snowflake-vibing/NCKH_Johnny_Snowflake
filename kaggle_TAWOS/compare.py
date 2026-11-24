"""Paired statistical comparison across TAWOS settings (final, cross, planning).

Ported directly from JohnnyPhan1712/SR-G3_planning-time-sp (src/compare.py):
- MAE by issue group (all, changed, unchanged)
- Paired Wilcoxon signed-rank test on per-issue absolute errors
- Vargha-Delaney A12 (> 0.5 means the first setting in pair has larger errors / is worse)
- Holm-Bonferroni correction within each (pair, group) family
- 300 DPI 2-panel comparison plot saved cleanly with Agg backend.
"""

from __future__ import annotations

import argparse
import glob
import os
from typing import Dict, List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon

# (a, b): final vs cross = over-optimism when model meets planning-time input;
# cross vs planning = gain from training on planning-time data; final vs planning = full gap.
PAIRS = [("final", "cross"), ("cross", "planning"), ("final", "planning")]


def a12(x, y) -> float:
    """Vargha-Delaney A12 = P(x > y) + 0.5 P(x = y); on errors, > 0.5 means x is worse."""
    return float(mannwhitneyu(x, y).statistic / (len(x) * len(y)))


def magnitude(a: float) -> str:
    """Threshold magnitudes per Vargha & Delaney (2000)."""
    d = abs(a - 0.5)
    return "negligible" if d < 0.06 else "small" if d < 0.14 else "medium" if d < 0.21 else "large"


def holm(p) -> np.ndarray:
    """Step-down Holm-Bonferroni correction."""
    p_arr = np.asarray(p, float)
    if len(p_arr) == 0:
        return p_arr
    order = np.argsort(p_arr)
    adj = np.minimum(np.maximum.accumulate((len(p_arr) - np.arange(len(p_arr))) * p_arr[order]), 1)
    out = np.empty_like(p_arr)
    out[order] = adj
    return out


def load_predictions_frame(pred_dir: str, prefix: str) -> pd.DataFrame:
    """Load `<prefix>_<model>_<setting>.parquet` files into paired wide table by group."""
    pattern = os.path.join(pred_dir, f"{prefix}_*.parquet")
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No prediction parquets matching {pattern}")

    parts: List[pd.DataFrame] = []
    prefix_head = f"{prefix}_"
    for fpath in files:
        stem = os.path.splitext(os.path.basename(fpath))[0]
        if not stem.startswith(prefix_head) or "_" not in stem[len(prefix_head) :]:
            continue
        model, setting = stem[len(prefix_head) :].rsplit("_", 1)
        if setting not in ("final", "cross", "planning"):
            continue
        parts.append(pd.read_parquet(fpath).assign(model=model, setting=setting))

    if not parts:
        raise ValueError(f"No valid setting prediction files found for prefix='{prefix}' in {pred_dir}")

    d = pd.concat(parts, ignore_index=True)
    d["ae"] = (d["y_true"] - d["y_pred"]).abs()
    w = d.set_index(["project", "model", "ID", "changed", "setting"])["ae"].unstack().reset_index()
    return pd.concat(
        [
            w.assign(group="all"),
            w.assign(group=np.where(w["changed"], "changed", "unchanged")),
        ],
        ignore_index=True,
    )


def summarize_mae_by_group(w: pd.DataFrame) -> pd.DataFrame:
    """Compute per-(project, model, group) MAE and count across available settings."""
    settings = [s for s in ("final", "cross", "planning") if s in w.columns]
    if not settings:
        return pd.DataFrame()
    grouped = w.groupby(["project", "model", "group"])[settings]
    mae_mean = grouped.mean().rename(columns={s: f"MAE_{s}" for s in settings})
    counts = w.groupby(["project", "model", "group"]).size().rename("N_Issues")
    return pd.concat([mae_mean, counts], axis=1).reset_index()


def compare(w: pd.DataFrame) -> pd.DataFrame:
    """Run paired Wilcoxon + Vargha-Delaney A12 + Holm across all available setting pairs."""
    available_pairs = [(a, b) for (a, b) in PAIRS if a in w.columns and b in w.columns]
    rows = []
    for (p, m, g), grp in w.groupby(["project", "model", "group"]):
        for a, b in available_pairs:
            sub = grp[[a, b]].dropna()
            if len(sub) == 0:
                continue
            x, y = sub[a], sub[b]
            pval = float(wilcoxon(x, y).pvalue) if (x != y).any() else 1.0
            a12_val = a12(x, y)
            rows.append(
                {
                    "project": p,
                    "model": m,
                    "group": g,
                    "pair": f"{a}-{b}",
                    "n": len(sub),
                    "MAE_a": float(x.mean()),
                    "MAE_b": float(y.mean()),
                    "p": pval,
                    "A12": a12_val,
                }
            )
    t = pd.DataFrame(rows)
    if t.empty:
        return t
    t["p_holm"] = t.groupby(["pair", "group"])["p"].transform(holm)
    t["magnitude"] = t["A12"].map(magnitude)
    return t


def plot_tawos_3setting_comparison(
    mae_df: pd.DataFrame,
    wilcoxon_df: pd.DataFrame,
    out_path: str,
    title_prefix: str = "TAWOS",
) -> str:
    """Plot 300 DPI 2-panel figure: (A) All-issue MAE across 3 settings, (B) Changed A12 effect sizes."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.8))

    # Panel (A): focus on the primary non-constant model if multiple exist
    all_df = mae_df[mae_df["group"] == "all"].copy()
    models = sorted(all_df["model"].unique().tolist())
    focus_model = "gpt2sp" if "gpt2sp" in models else ("tfidf_ridge" if "tfidf_ridge" in models else models[0])
    sub_all = all_df[all_df["model"] == focus_model].sort_values("project").reset_index(drop=True)

    setting_cols = [(s, f"MAE_{s}") for s in ("final", "cross", "planning") if f"MAE_{s}" in sub_all.columns]
    if not sub_all.empty and setting_cols:
        x = np.arange(len(sub_all))
        w = 0.25 if len(setting_cols) == 3 else 0.35
        colors = {"final": "#e74c3c", "cross": "#f39c12", "planning": "#2ecc71"}
        offsets = np.linspace(-(len(setting_cols) - 1) / 2.0, (len(setting_cols) - 1) / 2.0, len(setting_cols)) * w
        for (sname, col), off in zip(setting_cols, offsets):
            ax1.bar(x + off, sub_all[col], w, label=sname, color=colors.get(sname, "#3498db"), alpha=0.9)
        ax1.set_xticks(x)
        ax1.set_xticklabels(sub_all["project"], rotation=30, ha="right", fontsize=10, fontweight="bold")
        ax1.set_ylabel("MAE (Story Points)", fontsize=11, fontweight="bold")
        ax1.set_title(f"(A) {title_prefix} ({focus_model}): MAE Across 3 Settings (All Issues)", fontsize=12, fontweight="bold")
        ax1.legend(frameon=True)
        ax1.grid(axis="y", linestyle="--", alpha=0.6)
    else:
        ax1.set_title(f"(A) {title_prefix}: No MAE data available")

    # Panel (B): Vargha-Delaney A12 on changed issues
    chg = wilcoxon_df[(wilcoxon_df["group"] == "changed") & (wilcoxon_df["model"] == focus_model)].copy()
    if not chg.empty:
        piv = chg.pivot_table(index="project", columns="pair", values="A12", aggfunc="first").sort_index()
        sig = chg.pivot_table(index="project", columns="pair", values="p_holm", aggfunc="first").sort_index()
        pairs_present = [f"{a}-{b}" for (a, b) in PAIRS if f"{a}-{b}" in piv.columns]
        x2 = np.arange(len(piv))
        w2 = 0.25 if len(pairs_present) == 3 else 0.35
        pair_colors = {"final-cross": "#3498db", "cross-planning": "#9b59b6", "final-planning": "#e67e22"}
        offsets2 = np.linspace(-(len(pairs_present) - 1) / 2.0, (len(pairs_present) - 1) / 2.0, len(pairs_present)) * w2
        for pname, off in zip(pairs_present, offsets2):
            vals = piv[pname].fillna(0.5).to_numpy()
            bars = ax2.bar(x2 + off, vals, w2, label=pname, color=pair_colors.get(pname, "#34495e"), alpha=0.9)
            pvals = sig[pname].reindex(piv.index).to_numpy()
            for bar, pv in zip(bars, pvals):
                if pd.notna(pv) and pv < 0.05:
                    ax2.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        bar.get_height() + 0.012,
                        "*",
                        ha="center",
                        va="bottom",
                        fontsize=12,
                        fontweight="bold",
                    )
        ax2.axhline(0.5, color="black", linewidth=1.2, linestyle="--", label="A12 = 0.5 (Parity)")
        ax2.set_ylim(0.0, 1.05)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(piv.index, rotation=30, ha="right", fontsize=10, fontweight="bold")
        ax2.set_ylabel("Vargha-Delaney A12 (> 0.5 = First Worse)", fontsize=11, fontweight="bold")
        ax2.set_title(f"(B) {title_prefix} ({focus_model}): Changed-Issue A12 (* Holm p < 0.05)", fontsize=12, fontweight="bold")
        ax2.legend(frameon=True)
        ax2.grid(axis="y", linestyle="--", alpha=0.6)
    else:
        ax2.set_title(f"(B) {title_prefix}: No changed-issue paired comparisons")

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def run_compare(
    pred_dir: str,
    prefix: str,
    out_dir: str,
    title_prefix: str = "TAWOS",
) -> Dict[str, str]:
    """Run comparison suite on `<pred_dir>/<prefix>_*.parquet` and save CSVs + PNG figure."""
    os.makedirs(out_dir, exist_ok=True)
    fig_dir = os.path.join(out_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    w = load_predictions_frame(pred_dir, prefix)
    mae_df = summarize_mae_by_group(w)
    wilcoxon_df = compare(w)

    mae_path = os.path.join(out_dir, "mae_by_group.csv")
    wilcoxon_path = os.path.join(out_dir, "wilcoxon.csv")
    fig_path = os.path.join(fig_dir, "tawos_3setting_comparison.png")

    mae_df.to_csv(mae_path, index=False)
    wilcoxon_df.to_csv(wilcoxon_path, index=False)
    plot_tawos_3setting_comparison(mae_df, wilcoxon_df, fig_path, title_prefix=title_prefix)

    return {
        "mae_by_group.csv": mae_path,
        "wilcoxon.csv": wilcoxon_path,
        "figures/tawos_3setting_comparison.png": fig_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paired statistical comparison (Wilcoxon, A12, Holm) across TAWOS 3 settings."
    )
    parser.add_argument("--pred-dir", type=str, required=True, help="Directory holding prediction parquets.")
    parser.add_argument("--prefix", type=str, default="baseline", help="Filename prefix (baseline or gpt2sp).")
    parser.add_argument("--out-dir", type=str, required=True, help="Output directory for CSVs and figure.")
    parser.add_argument("--title-prefix", type=str, default="TAWOS", help="Chart title prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = run_compare(
        pred_dir=args.pred_dir,
        prefix=args.prefix,
        out_dir=args.out_dir,
        title_prefix=args.title_prefix,
    )
    print("✓ Comparison completed:")
    for k, v in outputs.items():
        print(f"  • {k}: {v}")


if __name__ == "__main__":
    main()
