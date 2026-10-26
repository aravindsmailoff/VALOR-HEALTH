"""Probability Calibration (Platt & Isotonic) and Split Conformal Prediction."""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

class CalibratorAndConformalEngine:
    """Calibrates continuous probabilities and produces conformal prediction intervals."""

    def __init__(self, confidence_level: float = 0.90):
        self.confidence_level = confidence_level
        self.alpha = 1.0 - confidence_level
        self.isotonic_model = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        self.platt_model = LogisticRegression(C=1.0, solver="lbfgs")
        self.conformal_quantile_q: float = 0.15
        self.fitted: bool = False

    def fit_calibration(self, raw_probs: np.ndarray, y_true: np.ndarray) -> "CalibratorAndConformalEngine":
        """Fits Isotonic and Platt calibration models on validation predictions."""
        # 1. Fit Isotonic
        self.isotonic_model.fit(raw_probs, y_true)

        # 2. Fit Platt (univariate logistic regression on logits)
        eps = 1e-6
        clipped_p = np.clip(raw_probs, eps, 1.0 - eps)
        logits = np.log(clipped_p / (1.0 - clipped_p)).reshape(-1, 1)
        self.platt_model.fit(logits, y_true)

        # 3. Compute Conformal non-conformity scores on validation set: |y - p|
        calibrated_val = self.calibrate(raw_probs, method="isotonic")
        conformity_scores = np.abs(y_true - calibrated_val)
        
        # Conformal quantile: (1 - alpha) * (1 + 1/n)
        n = len(y_true)
        q_level = float(min(0.99, (1.0 - self.alpha) * (1.0 + 1.0 / max(1, n))))
        self.conformal_quantile_q = float(np.quantile(conformity_scores, q_level))
        self.fitted = True
        return self

    def calibrate(self, raw_probs: np.ndarray, method: str = "isotonic") -> np.ndarray:
        """Transforms uncalibrated model outputs into true empirical probabilities."""
        if not self.fitted:
            return raw_probs
        if method == "isotonic":
            return np.clip(self.isotonic_model.predict(raw_probs), 0.01, 0.98)
        else: # platt
            eps = 1e-6
            clipped_p = np.clip(raw_probs, eps, 1.0 - eps)
            logits = np.log(clipped_p / (1.0 - clipped_p)).reshape(-1, 1)
            return np.clip(self.platt_model.predict_proba(logits)[:, 1], 0.01, 0.98)

    def predict_conformal_interval(
        self,
        calibrated_prob: float,
        is_sparse_data: bool = False
    ) -> Tuple[float, float, str]:
        """Returns [lower_bound, upper_bound] and an uncertainty confidence flag."""
        base_q = min(0.35, max(0.04, self.conformal_quantile_q))
        # Widen interval if sparse data (missing labs or short history)
        if is_sparse_data:
            q = min(0.48, base_q * 1.5 + 0.05)
            flag = "LOW_CONFIDENCE_SPARSE_DATA"
        else:
            q = base_q
            flag = "HIGH_CONFIDENCE"

        lower = max(0.0, calibrated_prob - q)
        upper = min(1.0, calibrated_prob + q)
        return round(lower, 3), round(upper, 3), flag
