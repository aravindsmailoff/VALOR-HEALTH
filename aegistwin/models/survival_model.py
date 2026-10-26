"""Time-to-Event Survival Analysis Engine for Acute Decompensation Hazards."""

import logging
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

try:
    from lifelines import CoxPHFitter
    HAS_LIFELINES = True
except Exception:
    HAS_LIFELINES = False

logger = logging.getLogger(__name__)

class SurvivalEngine:
    """Estimates time-to-event survival curves and hazard rates for acute clinical events."""

    def __init__(self, penalizer: float = 0.1):
        self.penalizer = penalizer
        self.cph = None
        self.baseline_hazard_scale = 0.003
        self.feature_weights = None

    def fit(
        self,
        X: pd.DataFrame,
        durations: np.ndarray,
        events: np.ndarray
    ) -> "SurvivalEngine":
        df = X.copy()
        df["duration"] = durations
        df["event"] = events

        # Select top stable clinical features for Cox PH to prevent collinear singularity
        top_cols = [
            "age", "charlson_comorbidity_index", "has_chf", "has_renal_disease",
            "ed_visits_90d", "latest_egfr", "avg_rolling_pdc_90d",
            "active_critical_safety_alert_count", "care_management_enrolled"
        ]
        subset_cols = [c for c in top_cols if c in df.columns] + ["duration", "event"]
        train_df = df[subset_cols].dropna()

        if HAS_LIFELINES:
            try:
                self.cph = CoxPHFitter(penalizer=self.penalizer)
                self.cph.fit(train_df, duration_col="duration", event_col="event")
                return self
            except Exception as e:
                logger.warning(f"Lifelines CoxPH fitting encountered ({e}), using parametric proportional hazard fallback.")

        # Parametric fallback using normalized log-hazard linear model
        feature_matrix = train_df.drop(columns=["duration", "event"])
        # Estimate weights via correlation with event
        self.feature_weights = {}
        for col in feature_matrix.columns:
            corr = np.corrcoef(feature_matrix[col], train_df["event"])[0, 1]
            self.feature_weights[col] = float(np.nan_to_num(corr, nan=0.0))
        return self

    def predict_survival_at_days(
        self,
        X: pd.DataFrame,
        time_horizons: List[int] = [30, 60, 90, 180]
    ) -> Dict[int, np.ndarray]:
        """Returns P(T > t) event-free survival probabilities for each time horizon in days."""
        results: Dict[int, np.ndarray] = {}
        n_samples = len(X)

        if self.cph is not None:
            try:
                # Use lifelines baseline hazard
                surv_funcs = self.cph.predict_survival_function(X)
                for t in time_horizons:
                    # Find closest index
                    closest_idx = min(surv_funcs.index, key=lambda x: abs(x - t))
                    results[t] = surv_funcs.loc[closest_idx].values
                return results
            except Exception as e:
                logger.warning(f"Error predicting with lifelines ({e}), falling back to parametric.")

        # Parametric proportional hazards: S(t) = exp(-H0(t) * exp(beta * X))
        # H0(t) = (t / 120)^1.4
        scores = np.zeros(n_samples)
        if self.feature_weights:
            for col, w in self.feature_weights.items():
                if col in X.columns:
                    col_vals = (X[col] - X[col].mean()) / max(1e-3, X[col].std())
                    scores += w * col_vals.fillna(0.0).values
        relative_risk = np.exp(np.clip(scores * 0.5, -2.5, 2.5))

        for t in time_horizons:
            base_cum_hazard = (t / 110.0) ** 1.35 * self.baseline_hazard_scale * 15.0
            cum_hazard = base_cum_hazard * relative_risk
            surv_prob = np.exp(-cum_hazard)
            results[t] = np.clip(surv_prob, 0.05, 0.99)

        return results
