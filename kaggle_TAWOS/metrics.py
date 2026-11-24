"""Evaluation metrics and statistical helpers for TAWOS Story Point Estimation."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple
import numpy as np
from scipy.stats import rankdata, wilcoxon


def compute_mae_mdae(
    y_true: Iterable[float], y_pred: Iterable[float]
) -> Tuple[float, float, np.ndarray]:
    """Compute MAE, MdAE, and individual absolute errors array."""
    yt = np.asarray(list(y_true), dtype=np.float64)
    yp = np.asarray(list(y_pred), dtype=np.float64)
    abs_errors = np.abs(yt - yp)
    return float(np.mean(abs_errors)), float(np.median(abs_errors)), abs_errors


def compute_metrics(
    y_true: Sequence[float] | np.ndarray,
    y_pred: Sequence[float] | np.ndarray,
    pool: Sequence[float] | np.ndarray | None = None,
    seed: int = 42,
    rg_runs: int = 1000,
) -> dict[str, float]:
    """Calculate PR #2 bug-fixed MAE, MdAE, and Standardized Accuracy (SA) via random guessing."""
    y_t = np.asarray(y_true, dtype=np.float64).ravel()
    y_p = np.asarray(y_pred, dtype=np.float64).ravel()

    if len(y_t) != len(y_p):
        raise ValueError(
            f"Length mismatch: len(y_true)={len(y_t)} != len(y_pred)={len(y_p)}"
        )

    if len(y_t) == 0:
        res = {"MAE": 0.0, "MdAE": 0.0}
        if pool is not None:
            res["SA"] = 0.0
        return res

    abs_errors = np.abs(y_t - y_p)
    mae = float(np.mean(abs_errors))
    mdae = float(np.median(abs_errors))
    result: dict[str, float] = {"MAE": mae, "MdAE": mdae}

    if pool is not None:
        pool_arr = np.asarray(pool, dtype=np.float64).ravel()
        if len(pool_arr) > 0:
            rng = np.random.default_rng(seed)
            guesses = rng.choice(pool_arr, size=(rg_runs, len(y_t)))
            mae_rg = np.abs(guesses - y_t).mean()
            sa = (1.0 - mae / mae_rg) * 100.0 if mae_rg > 0 else 0.0
            result["SA"] = float(sa)
        else:
            result["SA"] = 0.0

    return result


def sa_vs_median(mae_model: float, mae_median: float) -> float:
    """Compute Standardized Accuracy (SA %) relative to the Median Effort Baseline."""
    if mae_median <= 0.0:
        return 0.0
    return float((1.0 - (mae_model / mae_median)) * 100.0)


def compute_sa(model_mae: float, baseline_mae: float) -> float:
    """Alias for sa_vs_median matching kaggle_GPT2SP/metrics.py."""
    return sa_vs_median(model_mae, baseline_mae)


def safe_wilcoxon(errors_a: Iterable[float], errors_b: Iterable[float]) -> Tuple[float, float]:
    """Run paired Wilcoxon Signed-Rank Test safely, handling identical error vectors."""
    a = np.asarray(list(errors_a), dtype=np.float64)
    b = np.asarray(list(errors_b), dtype=np.float64)
    if len(a) == 0 or len(a) != len(b):
        raise ValueError(f"Mismatched or empty arrays for Wilcoxon: {len(a)} vs {len(b)}")
    if np.allclose(a - b, 0.0):
        return 0.0, 1.0
    stat, p_val = wilcoxon(a, b)
    return float(stat), float(p_val)


def vargha_delaney_a12(
    errors_model: Iterable[float], errors_baseline: Iterable[float]
) -> float:
    """Compute Vargha-Delaney A12 where > 0.5 means model errors tend to be smaller than baseline."""
    m_arr = np.asarray(list(errors_model), dtype=np.float64)
    n_arr = np.asarray(list(errors_baseline), dtype=np.float64)
    m = len(m_arr)
    n = len(n_arr)
    if m == 0 or n == 0:
        raise ValueError("Input arrays for Vargha-Delaney A12 must be non-empty.")

    combined = np.concatenate([m_arr, n_arr])
    ranks = rankdata(combined, method="average")
    r1 = float(np.sum(ranks[:m]))
    a12_baseline_smaller = (r1 / m - (m + 1.0) / 2.0) / n
    return float(1.0 - a12_baseline_smaller)


def holm_bonferroni(p_values: Iterable[float]) -> List[float]:
    """Adjust p-values using step-down Holm-Bonferroni family-wise error control."""
    p_arr = np.asarray(list(p_values), dtype=np.float64)
    m = len(p_arr)
    if m == 0:
        return []
    order = np.argsort(p_arr)
    adjusted = np.empty(m, dtype=np.float64)
    running_max = 0.0
    for rank_idx, orig_idx in enumerate(order):
        scaled = (m - rank_idx) * p_arr[orig_idx]
        running_max = max(running_max, min(1.0, scaled))
        adjusted[orig_idx] = running_max
    return [float(x) for x in adjusted]
