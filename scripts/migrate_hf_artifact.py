"""Zero-rerun migration: reorganize existing HF GPT2SP & Deep-SE runs into unified Option A artifact."""

import argparse
import os
import shutil
import sys
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "kaggle_GPT2SP"))

from hf_utils import resolve_hf_token  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Migrate existing Snowflake06/NCKH_GPT2SP & Snowflake06/NCKH_DeepSE outputs "
            "into unified Option A repo (NCKH3-StoryPoint-Artifact) without rerunning training."
        )
    )
    parser.add_argument("--gpt2sp-source-repo", type=str, default="Snowflake06/NCKH_GPT2SP")
    parser.add_argument("--gpt2sp-source-prefix", type=str, default="gpt2sp_16proj_seed0_title_len20")
    parser.add_argument("--deepse-source-repo", type=str, default="Snowflake06/NCKH_DeepSE")
    parser.add_argument("--deepse-source-prefix", type=str, default="deepse_16proj_fixed_lm_dim50_seed1234")
    parser.add_argument("--results-repo", type=str, default="NCKH3-StoryPoint-Artifact")
    parser.add_argument("--staging-dir", type=str, default=None)
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    parser.add_argument(
        "--in-place",
        action="store_true",
        help=(
            "Refresh README.md (YAML viewer configs), comparisons/, and datasets/ directly in --results-repo "
            "using summaries already on that repo without touching existing experiments/."
        ),
    )
    return parser.parse_args()


def resolve_staging_dir(explicit_dir: Optional[str]) -> str:
    if explicit_dir:
        base = explicit_dir
    elif os.path.exists("/kaggle/working"):
        base = os.path.join("/kaggle/working", "outputs", "artifact_staging")
    else:
        base = os.path.join("scripts", "outputs", "artifact_staging")
    os.makedirs(base, exist_ok=True)
    return base


def resolve_clean_dataset_path() -> Optional[str]:
    candidates = [
        os.path.join(REPO_ROOT, "data", "clean", "springxd_cleaned_dataset.csv"),
        os.path.join(REPO_ROOT, "docs", "draft", "springxd_cleaned_dataset.csv"),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    return None


def download_and_reorganize_run(
    api: HfApi,
    src_repo: str,
    src_prefix: str,
    dest_root: str,
    dest_run_rel: str,
    dl_cache_dir: str,
    token: Optional[str],
    summary_filename: str,
    stat_tests_filename: str,
    figure_filename: str,
) -> Dict[str, str]:
    """Download existing run artifacts from HF and copy into standardized Option A layout."""
    repo_files = sorted(api.list_repo_files(repo_id=src_repo, repo_type="dataset", token=token))
    clean_prefix = src_prefix.strip("/")
    prefix_slash = f"{clean_prefix}/"
    matching = [f for f in repo_files if f.startswith(prefix_slash)]
    if not matching:
        raise FileNotFoundError(f"No files under '{prefix_slash}' in {src_repo}")

    dest_run_dir = os.path.join(dest_root, os.path.normpath(dest_run_rel))
    os.makedirs(os.path.join(dest_run_dir, "figures"), exist_ok=True)
    os.makedirs(os.path.join(dest_run_dir, "predictions"), exist_ok=True)

    direct_map = {
        summary_filename: "summary.csv",
        stat_tests_filename: "stat_tests.csv",
        figure_filename: os.path.join("figures", "benchmark_audit.png"),
        "run_metadata.json": "metadata.json",
    }

    local_paths: Dict[str, str] = {}
    pred_count = 0

    for remote_file in matching:
        rel = remote_file[len(prefix_slash) :]
        if rel in direct_map:
            target_rel = direct_map[rel]
        elif rel.startswith("predictions/") and rel.endswith(".csv"):
            base_name = os.path.basename(rel)
            if base_name.endswith("_predictions.csv"):
                base_name = base_name[: -len("_predictions.csv")] + ".csv"
            target_rel = os.path.join("predictions", base_name)
            pred_count += 1
        else:
            target_rel = os.path.normpath(rel)

        downloaded = hf_hub_download(
            repo_id=src_repo,
            filename=remote_file,
            repo_type="dataset",
            local_dir=dl_cache_dir,
            token=token,
        )
        dest_file = os.path.join(dest_run_dir, target_rel)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(downloaded, dest_file)
        local_paths[target_rel.replace("\\", "/")] = dest_file

    print(
        f"  ✓ Staged {src_repo}/{clean_prefix} -> {dest_run_rel}/ "
        f"({pred_count} prediction CSVs + summary/stat_tests/figure/metadata)"
    )
    return local_paths


def build_cross_model_comparison(
    gpt_summary_path: str,
    deep_summary_path: str,
    out_csv_path: str,
    out_fig_path: str,
) -> pd.DataFrame:
    """Build joined 16-project cross-model CSV and 300 DPI comparison chart."""
    df_gpt = pd.read_csv(gpt_summary_path)
    df_deep = pd.read_csv(deep_summary_path)

    merged = pd.merge(
        df_gpt[
            [
                "Project",
                "Abbr",
                "Name",
                "N_Test",
                "Real_Median_MAE",
                "GPT2SP_Reported_MAE",
                "GPT2SP_Actual_MAE",
                "SA_vs_Median (%)",
            ]
        ].rename(
            columns={
                "N_Test": "N_Test_GPT2SP",
                "Real_Median_MAE": "Real_Median_MAE_GPT2SP",
                "GPT2SP_Reported_MAE": "GPT2SP_Paper_MAE",
                "SA_vs_Median (%)": "GPT2SP_SA_vs_Med (%)",
            }
        ),
        df_deep[
            [
                "Project",
                "N_Test",
                "Real_Median_MAE",
                "DeepSE_Reported_MAE",
                "DeepSE_Actual_MAE",
                "SA_vs_Real_Median (%)",
            ]
        ].rename(
            columns={
                "N_Test": "N_Test_DeepSE",
                "Real_Median_MAE": "Real_Median_MAE_DeepSE",
                "DeepSE_Reported_MAE": "DeepSE_Paper_MAE",
                "SA_vs_Real_Median (%)": "DeepSE_SA_vs_Med (%)",
            }
        ),
        on="Project",
        how="inner",
    )

    best_labels: List[str] = []
    for _, row in merged.iterrows():
        candidates = {
            "Real_Median": 0.0,
            "DeepSE": float(row["DeepSE_SA_vs_Med (%)"]),
            "GPT2SP": float(row["GPT2SP_SA_vs_Med (%)"]),
        }
        best_labels.append(max(candidates, key=candidates.get))

    merged["Best_By_SA_vs_Own_Median"] = best_labels
    ordered_cols = [
        "Project",
        "Abbr",
        "Name",
        "N_Test_GPT2SP",
        "N_Test_DeepSE",
        "Real_Median_MAE_GPT2SP",
        "Real_Median_MAE_DeepSE",
        "DeepSE_Paper_MAE",
        "DeepSE_Actual_MAE",
        "DeepSE_SA_vs_Med (%)",
        "GPT2SP_Paper_MAE",
        "GPT2SP_Actual_MAE",
        "GPT2SP_SA_vs_Med (%)",
        "Best_By_SA_vs_Own_Median",
    ]
    merged = merged[ordered_cols]

    os.makedirs(os.path.dirname(out_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(out_fig_path), exist_ok=True)
    merged.to_csv(out_csv_path, index=False)

    # 2-panel 300 DPI Cross-Model Benchmark Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    x = np.arange(len(merged))
    w = 0.20

    ax1.bar(x - 1.5 * w, merged["Real_Median_MAE_GPT2SP"], w, label="Real Median (GPT2SP)", color="#2ecc71", alpha=0.9)
    ax1.bar(x - 0.5 * w, merged["GPT2SP_Actual_MAE"], w, label="GPT2SP Actual", color="#e74c3c", alpha=0.9)
    ax1.bar(x + 0.5 * w, merged["Real_Median_MAE_DeepSE"], w, label="Real Median (Deep-SE)", color="#27ae60", alpha=0.9)
    ax1.bar(x + 1.5 * w, merged["DeepSE_Actual_MAE"], w, label="Deep-SE Actual", color="#3498db", alpha=0.9)
    ax1.set_xticks(x)
    ax1.set_xticklabels(merged["Abbr"], fontsize=11, fontweight="bold")
    ax1.set_ylabel("MAE (Story Points)", fontsize=12, fontweight="bold")
    ax1.set_title("(A) 16-Project MAE: Own-Split Median vs. GPT2SP & Deep-SE", fontsize=13, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.65)

    w2 = 0.36
    ax2.bar(x - w2 / 2, merged["DeepSE_SA_vs_Med (%)"], w2, label="Deep-SE SA vs. Median (%)", color="#3498db", alpha=0.88)
    ax2.bar(x + w2 / 2, merged["GPT2SP_SA_vs_Med (%)"], w2, label="GPT2SP SA vs. Median (%)", color="#e74c3c", alpha=0.88)
    ax2.axhline(0, color="black", linewidth=1.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(merged["Abbr"], fontsize=11, fontweight="bold")
    ax2.set_ylabel("Standardized Accuracy SA (%) vs. Real Median", fontsize=12, fontweight="bold")
    ax2.set_title("(B) Standardized Accuracy Over Honest Train-Only Median Baseline", fontsize=13, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.65)

    plt.tight_layout()
    plt.savefig(out_fig_path, dpi=300)
    plt.close(fig)
    return merged


def write_dataset_card(
    staging_dir: str,
    df_gpt_sum: pd.DataFrame,
    df_gpt_stats: pd.DataFrame,
    df_deep_sum: pd.DataFrame,
    df_deep_stats: pd.DataFrame,
    df_cross: pd.DataFrame,
    has_clean_dataset: bool,
    extra_remote_files: Optional[List[str]] = None,
) -> str:
    """Write Hugging Face Dataset Card README.md with YAML configs for HF Viewer."""
    gpt_losses = int((df_gpt_sum["Verdict"] == "LOSES_TO_MEDIAN").sum())
    gpt_mean_sa = float(df_gpt_sum["SA_vs_Median (%)"].mean())
    deep_losses = int((df_deep_sum["Verdict"] == "LOSES_TO_MEDIAN").sum())
    deep_mean_sa = float(df_deep_sum["SA_vs_Real_Median (%)"].mean())
    med_wins = int((df_cross["Best_By_SA_vs_Own_Median"] == "Real_Median").sum())

    def _find_stat(df_st: pd.DataFrame, prefix: str) -> Tuple[str, str, str]:
        row = df_st[df_st["Comparison"].str.startswith(prefix)]
        if row.empty:
            return "N/A", "N/A", "N/A"
        r = row.iloc[0]
        a12_val = f"{r['A12']:.4f}" if pd.notna(r["A12"]) else "—"
        return f"{r['Mean_Diff']:+.4f}", f"{r['p_value']:.4e}", a12_val

    gpt_med_diff, gpt_med_p, gpt_med_a12 = _find_stat(df_gpt_stats, "Actual_Checkpoint_MAE vs Real_Median_MAE")
    gpt_rep_diff, gpt_rep_p, _ = _find_stat(df_gpt_stats, "Actual_Checkpoint_MAE vs Paper_Reported_MAE")
    deep_med_diff, deep_med_p, deep_med_a12 = _find_stat(df_deep_stats, "DeepSE_Actual_MAE vs Real_Median_MAE")
    deep_rep_diff, deep_rep_p, _ = _find_stat(df_deep_stats, "DeepSE_Actual_MAE vs Paper_Reported_DeepSE_MAE")

    clean_yaml = ""
    clean_tree_line = ""
    if has_clean_dataset:
        clean_yaml = (
            "  - config_name: springxd_planning_clean\n"
            "    data_files:\n"
            "      - split: full\n"
            "        path: datasets/springxd_planning_clean.csv\n"
        )
        clean_tree_line = "│   └── springxd_planning_clean.csv     # Leakage-free Spring XD snapshot at SP_Estimation_Date\n"

    remote_set = set(extra_remote_files or [])
    tawos_yaml = ""
    tawos_tree_line = ""
    tawos_snap_line = ""
    if "datasets/tawos_snapshots/dataset_summary.csv" in remote_set:
        tawos_yaml += (
            "  - config_name: tawos_snapshots_summary\n"
            "    data_files:\n"
            "      - split: eval\n"
            "        path: datasets/tawos_snapshots/dataset_summary.csv\n"
        )
        tawos_snap_line = "│   └── tawos_snapshots/              # 13-project TAWOS planning-time parquets & audit CSV\n"
    if "experiments/tawos/baseline/13proj_3settings_seed42/summary.csv" in remote_set:
        tawos_yaml += (
            "  - config_name: tawos_baseline_summary\n"
            "    data_files:\n"
            "      - split: eval\n"
            "        path: experiments/tawos/baseline/13proj_3settings_seed42/summary.csv\n"
        )
        tawos_tree_line += "    ├── tawos/baseline/13proj_3settings_seed42/\n"
    if "experiments/tawos/baseline/13proj_3settings_seed42/wilcoxon.csv" in remote_set:
        tawos_yaml += (
            "  - config_name: tawos_baseline_wilcoxon\n"
            "    data_files:\n"
            "      - split: eval\n"
            "        path: experiments/tawos/baseline/13proj_3settings_seed42/wilcoxon.csv\n"
        )
    if "experiments/tawos/gpt2sp/13proj_3settings_seed42/summary.csv" in remote_set:
        tawos_yaml += (
            "  - config_name: tawos_gpt2sp_summary\n"
            "    data_files:\n"
            "      - split: eval\n"
            "        path: experiments/tawos/gpt2sp/13proj_3settings_seed42/summary.csv\n"
        )
        tawos_tree_line += "    ├── tawos/gpt2sp/13proj_3settings_seed42/\n"
    if "experiments/tawos/gpt2sp/13proj_3settings_seed42/wilcoxon.csv" in remote_set:
        tawos_yaml += (
            "  - config_name: tawos_gpt2sp_wilcoxon\n"
            "    data_files:\n"
            "      - split: eval\n"
            "        path: experiments/tawos/gpt2sp/13proj_3settings_seed42/wilcoxon.csv\n"
        )

    datasets_header = "├── datasets/\n" if (clean_tree_line or tawos_snap_line) else ""

    content = f"""---
license: mit
task_categories:
  - tabular-regression
language:
  - en
pretty_name: NCKH 3 — Agile Story Point Estimation Artifact (GPT2SP, Deep-SE & Planning-Time Leakage Control)
configs:
  - config_name: cross_model_16proj
    default: true
    data_files:
      - split: eval
        path: comparisons/cross_model_16proj.csv
  - config_name: gpt2sp_summary
    data_files:
      - split: eval
        path: experiments/gpt2sp/replication/seed0_title_len20/summary.csv
  - config_name: gpt2sp_stat_tests
    data_files:
      - split: eval
        path: experiments/gpt2sp/replication/seed0_title_len20/stat_tests.csv
  - config_name: gpt2sp_predictions
    data_files:
      - split: test
        path: experiments/gpt2sp/replication/seed0_title_len20/predictions/*.csv
  - config_name: deepse_summary
    data_files:
      - split: eval
        path: experiments/deepse/replication/fixed_lm_dim50_seed1234/summary.csv
  - config_name: deepse_stat_tests
    data_files:
      - split: eval
        path: experiments/deepse/replication/fixed_lm_dim50_seed1234/stat_tests.csv
  - config_name: deepse_predictions
    data_files:
      - split: test
        path: experiments/deepse/replication/fixed_lm_dim50_seed1234/predictions/*.csv
{clean_yaml}{tawos_yaml}---

# NCKH 3 — Agile Story Point Estimation Artifact (WSESE / ICSE 2026 Research Track)

Unified experimental artifact for **"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"** (Group 3, UIT - VNUHCM).  
Source code & provenance: [`snowflake-vibing/NCKH_Johnny_Snowflake`](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake).

## Key Verified Findings Across 16 Open-Source Projects

| Model / Experiment | Loses to Train-Only Median | Mean SA vs. Median | Global Wilcoxon vs. Median (`Diff`, `p`, `A12`) | Global Wilcoxon vs. Paper MAE (`Diff`, `p`) |
| :--- | :---: | :---: | :---: | :---: |
| **GPT2SP** (Official HF Checkpoints, Seed 0, `title_len20`) | **{gpt_losses}/16** | `{gpt_mean_sa:+.2f}%` | `{gpt_med_diff}`, `p={gpt_med_p}`, `A12={gpt_med_a12}` | `{gpt_rep_diff}`, `p={gpt_rep_p}` *(1.80x PR #2 bug)* |
| **Deep-SE** (PyTorch LD-RNN, `fixed_lm`, `dim=50`, Seed 1234) | **{deep_losses}/16** | `{deep_mean_sa:+.2f}%` | `{deep_med_diff}`, `p={deep_med_p}`, `A12={deep_med_a12}` | `{deep_rep_diff}`, `p={deep_rep_p}` *(faithful port)* |

* Across all 16 projects in `comparisons/cross_model_16proj.csv`, neither replicated model outperforms its own train-only Median Baseline (SA <= 0%) on **{med_wins}/16 projects**.

## Repository Structure (Option A Standard)

```text
NCKH3-StoryPoint-Artifact/
├── README.md                           # Dataset Card + YAML viewer configs
{datasets_header}{clean_tree_line}{tawos_snap_line}├── comparisons/
│   ├── cross_model_16proj.csv          # Joined 16-project benchmark table (Median vs Deep-SE vs GPT2SP)
│   └── figures/
│       └── cross_model_benchmark.png   # 300 DPI cross-model MAE & SA chart
└── experiments/
{tawos_tree_line}    ├── gpt2sp/
    │   └── replication/seed0_title_len20/
    │       ├── summary.csv
    │       ├── stat_tests.csv
    │       ├── metadata.json
    │       ├── figures/benchmark_audit.png
    │       └── predictions/<project>.csv (16 projects)
    └── deepse/
        └── replication/fixed_lm_dim50_seed1234/
            ├── summary.csv
            ├── stat_tests.csv
            ├── metadata.json
            ├── figures/benchmark_audit.png
            └── predictions/<project>.csv (16 projects)
```
"""
    readme_path = os.path.join(staging_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return readme_path


def main() -> None:
    args = parse_args()
    staging_dir = resolve_staging_dir(args.staging_dir)
    cache_dir = staging_dir.rstrip("/\\") + "_dl_cache"
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)

    token = resolve_hf_token()
    api = HfApi(token=token) if token else HfApi()

    if "/" in args.results_repo:
        target_repo_id = args.results_repo
    elif token:
        target_repo_id = f"{api.whoami()['name']}/{args.results_repo}"
    else:
        target_repo_id = f"Snowflake06/{args.results_repo}"

    gpt_rel = "experiments/gpt2sp/replication/seed0_title_len20"
    deep_rel = "experiments/deepse/replication/fixed_lm_dim50_seed1234"
    extra_remote_files: Optional[List[str]] = None

    print("=" * 85)
    if args.in_place:
        print(f"🔄 IN-PLACE REFRESH ON {target_repo_id} (README + comparisons + datasets)")
    else:
        print("🔄 MIGRATING EXISTING HF ARTIFACTS TO OPTION A (ZERO-RERUN)")
    print("=" * 85)

    if args.in_place:
        dl_token = token
        try:
            extra_remote_files = sorted(
                api.list_repo_files(repo_id=target_repo_id, repo_type="dataset", token=dl_token)
            )
        except Exception:
            extra_remote_files = []

        def _fetch_existing(rel_path: str) -> str:
            dl_dir = os.path.join(cache_dir, "inplace")
            os.makedirs(dl_dir, exist_ok=True)
            return hf_hub_download(
                repo_id=target_repo_id,
                filename=rel_path,
                repo_type="dataset",
                local_dir=dl_dir,
                token=dl_token,
            )

        gpt_files = {
            "summary.csv": _fetch_existing(f"{gpt_rel}/summary.csv"),
            "stat_tests.csv": _fetch_existing(f"{gpt_rel}/stat_tests.csv"),
        }
        deep_files = {
            "summary.csv": _fetch_existing(f"{deep_rel}/summary.csv"),
            "stat_tests.csv": _fetch_existing(f"{deep_rel}/stat_tests.csv"),
        }
        print(f"  ✓ Loaded existing GPT2SP & Deep-SE summaries directly from {target_repo_id}")
    else:
        dl_token = None if args.no_hf_push else token
        gpt_files = download_and_reorganize_run(
            api=api,
            src_repo=args.gpt2sp_source_repo,
            src_prefix=args.gpt2sp_source_prefix,
            dest_root=staging_dir,
            dest_run_rel=gpt_rel,
            dl_cache_dir=os.path.join(cache_dir, "gpt2sp"),
            token=dl_token,
            summary_filename="gpt2sp_16_projects_summary.csv",
            stat_tests_filename="gpt2sp_16_projects_statistical_tests.csv",
            figure_filename="gpt2sp_16_projects_benchmark_audit.png",
        )
        deep_files = download_and_reorganize_run(
            api=api,
            src_repo=args.deepse_source_repo,
            src_prefix=args.deepse_source_prefix,
            dest_root=staging_dir,
            dest_run_rel=deep_rel,
            dl_cache_dir=os.path.join(cache_dir, "deepse"),
            token=dl_token,
            summary_filename="deepse_16_projects_summary.csv",
            stat_tests_filename="deepse_16_projects_statistical_tests.csv",
            figure_filename="deepse_16_projects_benchmark_audit.png",
        )

    clean_src = resolve_clean_dataset_path()
    has_clean = False
    if clean_src:
        ds_dir = os.path.join(staging_dir, "datasets")
        os.makedirs(ds_dir, exist_ok=True)
        shutil.copy2(clean_src, os.path.join(ds_dir, "springxd_planning_clean.csv"))
        has_clean = True
        print("  ✓ Copied planning-time clean dataset -> datasets/springxd_planning_clean.csv")

    cross_csv = os.path.join(staging_dir, "comparisons", "cross_model_16proj.csv")
    cross_fig = os.path.join(staging_dir, "comparisons", "figures", "cross_model_benchmark.png")
    df_cross = build_cross_model_comparison(
        gpt_summary_path=gpt_files["summary.csv"],
        deep_summary_path=deep_files["summary.csv"],
        out_csv_path=cross_csv,
        out_fig_path=cross_fig,
    )
    print(f"  ✓ Built cross-model comparison ({len(df_cross)} projects) & 300 DPI chart")

    df_gpt_sum = pd.read_csv(gpt_files["summary.csv"])
    df_gpt_stats = pd.read_csv(gpt_files["stat_tests.csv"])
    df_deep_sum = pd.read_csv(deep_files["summary.csv"])
    df_deep_stats = pd.read_csv(deep_files["stat_tests.csv"])

    write_dataset_card(
        staging_dir=staging_dir,
        df_gpt_sum=df_gpt_sum,
        df_gpt_stats=df_gpt_stats,
        df_deep_sum=df_deep_sum,
        df_deep_stats=df_deep_stats,
        df_cross=df_cross,
        has_clean_dataset=has_clean,
        extra_remote_files=extra_remote_files,
    )
    print("  ✓ Generated HF Dataset Card README.md with YAML configs")

    if args.no_hf_push:
        staged_rels = sorted(
            os.path.relpath(os.path.join(r, f), staging_dir).replace("\\", "/")
            for r, _, fs in os.walk(staging_dir)
            for f in fs
        )
        print(f"ℹ️ Dry-run complete (--no-hf-push). Staged {len(staged_rels)} files at: {staging_dir}")
        for rel in staged_rels:
            print(f"   • {rel}")
        return

    if not token:
        raise RuntimeError(
            "No HF write token found in HF_TOKEN/hf_token or Kaggle Secrets. "
            "Pass --no-hf-push for local staging or configure a Write token."
        )

    api.create_repo(repo_id=target_repo_id, repo_type="dataset", private=args.private_hf, exist_ok=True)
    if args.in_place:
        ops = [
            CommitOperationAdd(
                path_in_repo=os.path.relpath(os.path.join(r, f), staging_dir).replace("\\", "/"),
                path_or_fileobj=os.path.join(r, f),
            )
            for r, _, fs in os.walk(staging_dir)
            for f in sorted(fs)
        ]
        api.create_commit(
            repo_id=target_repo_id,
            repo_type="dataset",
            operations=ops,
            commit_message="Refresh Dataset Card YAML configs, cross-model comparisons & clean dataset in-place",
        )
        print("\n" + "=" * 85)
        print(f"✅ Refreshed {len(ops)} files in-place on {target_repo_id} (existing experiments/ untouched)!")
    else:
        api.upload_folder(
            folder_path=staging_dir,
            repo_id=target_repo_id,
            repo_type="dataset",
            commit_message="Initialize unified NCKH3-StoryPoint-Artifact (GPT2SP + Deep-SE + Cross-Model Comparison)",
        )
        print("\n" + "=" * 85)
        print("✅ Migrated & published in 1 single commit!")
    print(f"   • View unified HF Artifact: https://huggingface.co/datasets/{target_repo_id}")
    print("=" * 85)


if __name__ == "__main__":
    main()
