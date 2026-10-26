"""Comprehensive Clinical ML Metrics and Decision-Curve Analysis (DCA)."""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_auc_score, average_precision_score, brier_score_loss,
    roc_curve, precision_recall_curve
)

def compute_precision_and_lift_at_k(y_true: np.ndarray, y_pred_prob: np.ndarray, k_pct: float) -> Tuple[float, float]:
    """Computes Precision@k and Lift@k for the top k% highest predicted risk members."""
    n = len(y_true)
    if n == 0:
        return 0.0, 1.0
    k = max(1, int(n * k_pct))
    top_indices = np.argsort(y_pred_prob)[::-1][:k]
    
    prec_at_k = float(np.mean(y_true[top_indices]))
    base_rate = float(np.mean(y_true))
    lift_at_k = float(prec_at_k / max(1e-4, base_rate))
    return round(prec_at_k, 4), round(lift_at_k, 2)

def compute_decision_curve_analysis(
    y_true: np.ndarray,
    y_pred_prob: np.ndarray,
    thresholds: Optional[np.ndarray] = None
) -> List[Dict[str, float]]:
    """Calculates Decision Curve Analysis Net Benefit across decision threshold probabilities:

    Net Benefit = (True Positives / N) - (False Positives / N) * [p_t / (1 - p_t)]
    """
    if thresholds is None:
        thresholds = np.linspace(0.05, 0.50, 10)
        
    n = float(len(y_true))
    event_rate = float(np.mean(y_true))
    dca_records: List[Dict[str, float]] = []

    for pt in thresholds:
        # Model policy
        y_decision = (y_pred_prob >= pt).astype(int)
        tp = np.sum((y_decision == 1) & (y_true == 1))
        fp = np.sum((y_decision == 1) & (y_true == 0))
        weight = pt / (1.0 - pt)
        net_benefit_model = (tp / n) - (fp / n) * weight

        # Treat All policy
        net_benefit_all = event_rate - (1.0 - event_rate) * weight
        # Treat None policy
        net_benefit_none = 0.0

        dca_records.append({
            "threshold": round(float(pt), 3),
            "net_benefit_model": round(float(net_benefit_model), 4),
            "net_benefit_all": round(float(net_benefit_all), 4),
            "net_benefit_none": 0.0
        })

    return dca_records

def compute_calibration_curve(
    y_true: np.ndarray,
    y_pred_prob: np.ndarray,
    n_bins: int = 10
) -> List[Dict[str, float]]:
    """Computes empirical reliability calibration bins (Observed vs Predicted)."""
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    curve = []

    for i in range(n_bins):
        low, high = bins[i], bins[i+1]
        mask = (y_pred_prob >= low) & (y_pred_prob < high if i < n_bins - 1 else y_pred_prob <= high)
        if np.sum(mask) > 0:
            pred_mean = float(np.mean(y_pred_prob[mask]))
            obs_mean = float(np.mean(y_true[mask]))
            count = int(np.sum(mask))
        else:
            pred_mean = float((low + high) / 2.0)
            obs_mean = 0.0
            count = 0

        curve.append({
            "bin": f"{int(low*100)}-{int(high*100)}%",
            "predicted_mean": round(pred_mean, 4),
            "observed_rate": round(obs_mean, 4),
            "sample_count": count
        })

    return curve

def evaluate_clinical_model_metrics(
    y_true: np.ndarray,
    y_pred_prob: np.ndarray
) -> Dict[str, Any]:
    """Generates standard clinical ML scorecard."""
    auroc = float(roc_auc_score(y_true, y_pred_prob))
    auprc = float(average_precision_score(y_true, y_pred_prob))
    brier = float(brier_score_loss(y_true, y_pred_prob))

    p1, l1 = compute_precision_and_lift_at_k(y_true, y_pred_prob, 0.01)
    p5, l5 = compute_precision_and_lift_at_k(y_true, y_pred_prob, 0.05)
    p10, l10 = compute_precision_and_lift_at_k(y_true, y_pred_prob, 0.10)

    # Expected Calibration Error (ECE)
    cal_bins = compute_calibration_curve(y_true, y_pred_prob, n_bins=10)
    total_n = max(1, len(y_true))
    ece = sum(abs(b["predicted_mean"] - b["observed_rate"]) * (b["sample_count"] / total_n) for b in cal_bins)

    return {
        "auroc": round(auroc, 4),
        "auprc": round(auprc, 4),
        "brier_score": round(brier, 4),
        "expected_calibration_error": round(float(ece), 4),
        "precision_at_1pct": p1,
        "lift_at_1pct": l1,
        "precision_at_5pct": p5,
        "lift_at_5pct": l5,
        "precision_at_10pct": p10,
        "lift_at_10pct": l10,
        "calibration_curve": cal_bins,
        "decision_curve": compute_decision_curve_analysis(y_true, y_pred_prob)
    }
