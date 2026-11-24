"""TAWOS 13-project x 3-setting Baseline Suite (Mean, Median, TF-IDF + Ridge).

Ported directly from JohnnyPhan1712/SR-G3_planning-time-sp (`src/baseline.py` + `src/compare.py`):
- Chronological 60/20/20 split by `Planning_Date` (tie-broken by `ID`), shared across `final`, `cross`, `planning`.
- Filters out SP > 100 (`MAX_SP = 100`).
- Tunes TF-IDF + Ridge alpha on validation MAE, refits on train+val, evaluates on test.
- Saves 9-column prediction parquets, summary CSV, Wilcoxon/A12/Holm tables, and 300 DPI plot.
- Publishes all results to Hugging Face Dataset Repo in 1 single batch commit.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from kaggle_TAWOS.compare import run_compare
    from kaggle_TAWOS.config import (
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        PREDICTION_COLS,
        SEED,
        SETTINGS,
        parse_projects_arg,
        resolve_data_dir,
        resolve_output_dir,
    )
    from kaggle_TAWOS.dataset import load_tawos_snapshot
    from kaggle_TAWOS.hf_utils import HFExperimentLogger, ensure_tawos_snapshots
    from kaggle_TAWOS.metrics import compute_metrics, sa_vs_median
except ImportError:
    from compare import run_compare  # type: ignore
    from config import (  # type: ignore
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        PREDICTION_COLS,
        SEED,
        SETTINGS,
        parse_projects_arg,
        resolve_data_dir,
        resolve_output_dir,
    )
    from dataset import load_tawos_snapshot  # type: ignore
    from hf_utils import HFExperimentLogger, ensure_tawos_snapshots  # type: ignore
    from metrics import compute_metrics, sa_vs_median  # type: ignore


ALPHAS = [0.1, 1, 10, 100]
RG_RUNS = 1000


def _constant_model(stat: str):
    def _fit_predict(train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, text_col: str, label_col: str, test_text_col: str):
        val_agg = float(pd.concat([train, val])[label_col].agg(stat))
        return np.full(len(test), val_agg, dtype=np.float64), None
    return _fit_predict


def _tfidf_ridge_model(train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, text_col: str, label_col: str, test_text_col: str):
    def _fit(df: pd.DataFrame, alpha: float):
        pipe = make_pipeline(
            TfidfVectorizer(min_df=2, ngram_range=(1, 2), sublinear_tf=True),
            Ridge(alpha=alpha),
        )
        return pipe.fit(df[text_col].fillna("").astype(str), df[label_col].astype(float))

    val_mae = {
        a: float(
            np.abs(
                val[label_col].astype(float)
                - _fit(train, a).predict(val[text_col].fillna("").astype(str)).clip(0)
            ).mean()
        )
        for a in ALPHAS
    }
    best_alpha = min(val_mae, key=val_mae.get)
    pool = pd.concat([train, val], ignore_index=True)
    pred = _fit(pool, best_alpha).predict(test[test_text_col].fillna("").astype(str)).clip(0)
    return pred.astype(np.float64), float(best_alpha)


BASE_MODELS = {
    "mean": _constant_model("mean"),
    "median": _constant_model("median"),
    "tfidf_ridge": _tfidf_ridge_model,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run TAWOS 13-project x 3-setting baselines (Mean, Median, TF-IDF+Ridge) + Wilcoxon/A12/Holm."
    )
    parser.add_argument("--projects", type=str, default="all", help="'all' or comma-separated TAWOS project keys")
    parser.add_argument(
        "--settings",
        type=str,
        default="all",
        choices=["all", "final", "cross", "planning"],
        help="Settings to evaluate",
    )
    parser.add_argument(
        "--input-mode",
        type=str,
        default="title_description",
        choices=["title_description", "title_only"],
        help="Text fields concatenated as input",
    )
    parser.add_argument("--data-dir", type=str, default=None, help="Directory holding <PROJECT>_snapshot.parquet files")
    parser.add_argument("--output-dir", type=str, default=None, help="Local output folder")
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--snapshots-subdir", type=str, default=DEFAULT_SNAPSHOTS_SUBDIR)
    parser.add_argument(
        "--run-name",
        type=str,
        default="experiments/tawos/baseline/13proj_3settings_seed42",
        help="HF dataset subdirectory prefix",
    )
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    projects = parse_projects_arg(args.projects)
    target_settings = ["final", "cross", "planning"] if args.settings == "all" else [args.settings]

    out_dir = resolve_output_dir(args.output_dir, args.run_name)
    pred_dir = os.path.join(out_dir, "predictions")
    os.makedirs(pred_dir, exist_ok=True)
    data_cache_dir = resolve_data_dir(args.data_dir)
    extra_dirs = [args.data_dir] if args.data_dir else []

    snapshot_paths = ensure_tawos_snapshots(
        projects=projects,
        local_dir=data_cache_dir,
        results_repo=args.results_repo,
        remote_subdir=args.snapshots_subdir,
        extra_search_dirs=extra_dirs,
    )

    logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=None,
        run_prefix=args.run_name,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )

    print("=" * 85)
    print(f"📊 TAWOS BASELINES (Mean / Median / TF-IDF+Ridge) | projects={len(projects)} | settings={target_settings}")
    print("=" * 85)

    rows: List[Dict[str, object]] = []
    preds_map: Dict[Tuple[str, str], List[pd.DataFrame]] = {}

    for proj in projects:
        train_df, val_df, test_df = load_tawos_snapshot(
            proj,
            parquet_path=snapshot_paths[proj],
            setting=None,
            input_mode=args.input_mode,
            max_sp=MAX_SP,
        )
        pool = pd.concat([train_df, val_df], ignore_index=True)

        for setting in target_settings:
            text_col, label_col, test_text_col, test_label_col = SETTINGS[setting]
            y_true = test_df[test_label_col].astype(np.float64)
            pool_labels = pool[label_col].astype(np.float64)

            med_pred, _ = BASE_MODELS["median"](train_df, val_df, test_df, text_col, label_col, test_text_col)
            med_mae = float(np.abs(y_true - med_pred).mean())

            for m_name, fit_predict in BASE_MODELS.items():
                pred, alpha = fit_predict(train_df, val_df, test_df, text_col, label_col, test_text_col)
                m = compute_metrics(y_true, pred, pool=pool_labels, seed=SEED, rg_runs=RG_RUNS)
                rows.append(
                    {
                        "project": proj,
                        "setting": setting,
                        "model": m_name,
                        "n_train": len(pool),
                        "n_test": len(test_df),
                        "alpha": alpha,
                        "MAE": m["MAE"],
                        "MdAE": m["MdAE"],
                        "SA": m["SA"],
                        "SA_vs_Median (%)": sa_vs_median(m["MAE"], med_mae),
                    }
                )
                pred_df = test_df.assign(
                    project=proj,
                    y_true=y_true.astype(np.float64),
                    y_pred=pred.astype(np.float64),
                )[PREDICTION_COLS].copy()
                pred_df["ID"] = pred_df["ID"].astype(np.int64)
                pred_df["changed"] = pred_df["changed"].astype(bool)
                preds_map.setdefault((m_name, setting), []).append(pred_df)

        print(f"  ✓ {proj:10s} (n_train={len(pool):5d}, n_test={len(test_df):4d})")

    batch_items: List[Tuple[str, str]] = []
    for (m_name, setting), dfs in sorted(preds_map.items()):
        comb = pd.concat(dfs, ignore_index=True)
        fname = f"baseline_{m_name}_{setting}.parquet"
        p_out = os.path.join(pred_dir, fname)
        comb.to_parquet(p_out, index=False)
        batch_items.append((p_out, f"predictions/{fname}"))

    summary_df = pd.DataFrame(rows)
    summary_path = os.path.join(out_dir, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    batch_items.append((summary_path, "summary.csv"))

    comp_outputs = run_compare(
        pred_dir=pred_dir,
        prefix="baseline",
        out_dir=out_dir,
        title_prefix="TAWOS Baseline",
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

    print("\nSummary MAE pivot:")
    print(summary_df.pivot_table(index="project", columns=["model", "setting"], values="MAE").round(3).to_string())

    if logger.enabled:
        ok = logger.upload_results_batch(
            batch_items,
            f"Finalize {args.run_name} summary, Wilcoxon/A12 tables, predictions & figure",
        )
        if ok:
            print(f"\n✅ Uploaded {len(batch_items)} artifacts to {logger.results_repo_id}/{args.run_name} in 1 commit!")


if __name__ == "__main__":
    main()
