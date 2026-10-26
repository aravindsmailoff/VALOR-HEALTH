"""Population Stability Index (PSI) and Post-Deployment Drift Detection."""

from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd

def calculate_psi(
    expected: np.ndarray,
    actual: np.ndarray,
    num_buckets: int = 10
) -> float:
    """Calculates Population Stability Index (PSI) between baseline and production distributions:

    PSI = sum((Actual% - Expected%) * ln(Actual% / Expected%))
    """
    if len(expected) == 0 or len(actual) == 0:
        return 0.0

    # Determine quantiles on expected distribution
    percentiles = np.linspace(0, 100, num_buckets + 1)
    bucket_bounds = np.percentile(expected, percentiles)
    bucket_bounds[0] = -np.inf
    bucket_bounds[-1] = np.inf

    eps = 1e-4
    n_exp = float(len(expected))
    n_act = float(len(actual))

    psi_total = 0.0
    for i in range(num_buckets):
        b_low, b_high = bucket_bounds[i], bucket_bounds[i+1]
        exp_count = np.sum((expected > b_low) & (expected <= b_high))
        act_count = np.sum((actual > b_low) & (actual <= b_high))

        exp_pct = max(eps, exp_count / n_exp)
        act_pct = max(eps, act_count / n_act)

        psi_total += (act_pct - exp_pct) * np.log(act_pct / exp_pct)

    return round(float(psi_total), 4)

class DriftDetector:
    """Monitors feature drift, score distribution shift, and calibration degradation."""

    def __init__(self, psi_warning_threshold: float = 0.10, psi_action_threshold: float = 0.20):
        self.psi_warning_threshold = psi_warning_threshold
        self.psi_action_threshold = psi_action_threshold
        self.baseline_feature_distributions: Dict[str, np.ndarray] = {}
        self.baseline_scores: Optional[np.ndarray] = None

    def fit_baseline(self, X_baseline: pd.DataFrame, scores_baseline: np.ndarray) -> "DriftDetector":
        """Captures reference distributions from the validation cohort."""
        for col in X_baseline.columns:
            self.baseline_feature_distributions[col] = X_baseline[col].dropna().values
        self.baseline_scores = scores_baseline
        return self

    def check_drift(
        self,
        X_current: pd.DataFrame,
        scores_current: np.ndarray
    ) -> Dict[str, Any]:
        """Evaluates incoming production batch against reference baseline."""
        feature_psi_results: Dict[str, float] = {}
        flagged_features: List[str] = []

        for col, base_vals in self.baseline_feature_distributions.items():
            if col in X_current.columns:
                curr_vals = X_current[col].dropna().values
                psi_val = calculate_psi(base_vals, curr_vals)
                feature_psi_results[col] = psi_val
                if psi_val >= self.psi_action_threshold:
                    flagged_features.append(f"{col} (PSI={psi_val})")

        # Score drift
        score_psi = 0.0
        if self.baseline_scores is not None and len(scores_current) > 0:
            score_psi = calculate_psi(self.baseline_scores, scores_current)

        needs_retraining = (score_psi >= self.psi_action_threshold) or (len(flagged_features) >= 3)
        status = "CRITICAL_DRIFT_RETRAIN_TRIGGERED" if needs_retraining else (
            "WARNING_MODERATE_DRIFT" if score_psi >= self.psi_warning_threshold or len(flagged_features) >= 1 else "STABLE"
        )

        return {
            "status": status,
            "prediction_score_psi": score_psi,
            "needs_model_retraining": needs_retraining,
            "flagged_features_count": len(flagged_features),
            "flagged_features": flagged_features,
            "feature_psis": feature_psi_results
        }
