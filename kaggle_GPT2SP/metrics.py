"""Statistical metrics and hypothesis testing helpers for effort estimation."""

from typing import Iterable, List, Tuple
import numpy as np
from scipy.stats import rankdata, wilcoxon


def compute_mae_mdae(y_true: Iterable[float], y_pred: Iterable[float]) -> Tuple[float, float, np.ndarray]:
    """Compute MAE, MdAE, and element-wise absolute error array."""
    yt = np.asarray(y_true, dtype=np.float64)
    yp = np.asarray(y_pred, dtype=np.float64)
    abs_errors = np.abs(yt - yp)
    return float(np.mean(abs_errors)), float(np.median(abs_errors)), abs_errors


def compute_sa(model_mae: float, baseline_mae: float) -> float:
    """Compute Standardized Accuracy (SA %) relative to a baseline MAE."""
    if baseline_mae <= 0.0:
        return 0.0
    return float((1.0 - (model_mae / baseline_mae)) * 100.0)


def safe_wilcoxon(errors_a: Iterable[float], errors_b: Iterable[float]) -> Tuple[float, float]:
    """Run paired Wilcoxon Signed-Rank Test safely, handling identical vectors."""
    a = np.asarray(errors_a, dtype=np.float64)
    b = np.asarray(errors_b, dtype=np.float64)
    if len(a) == 0 or len(a) != len(b):
        raise ValueError(f"Mismatched or empty arrays for Wilcoxon: {len(a)} vs {len(b)}")
    diff = a - b
    if np.allclose(diff, 0.0):
        return 0.0, 1.0
    stat, p_val = wilcoxon(a, b)
    return float(stat), float(p_val)


def vargha_delaney_a12(errors_model: Iterable[float], errors_baseline: Iterable[float]) -> float:
    """Compute Vargha-Delaney A12 effect size (probability errors_model < errors_baseline).

    Returns values in [0, 1]:
    - A12 > 0.5: model errors tend to be smaller (model outperforms baseline)
    - A12 < 0.5: baseline errors tend to be smaller (baseline outperforms model)
    - A12 == 0.5: stochastic equivalence
    """
    m_arr = np.asarray(errors_model, dtype=np.float64)
    n_arr = np.asarray(errors_baseline, dtype=np.float64)
    m = len(m_arr)
    n = len(n_arr)
    if m == 0 or n == 0:
        raise ValueError("Input arrays for Vargha-Delaney A12 must be non-empty.")

    # Rank-based formulation for lower-is-better metric (smaller error = stochastic superiority)
    combined = np.concatenate([m_arr, n_arr])
    ranks = rankdata(combined, method="average")
    r1 = float(np.sum(ranks[:m]))
    # Note: rankdata assigns smaller ranks to smaller errors; invert so smaller error => higher A12
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
