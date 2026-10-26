"""Causal Uplift Modeling (T-Learner) for Estimating Individual Treatment Effects."""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

class CausalUpliftEngine:
    """T-Learner causal uplift model estimating Individual Treatment Effect (ITE) of Care Management."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        # Model for Control group (No Care Outreach)
        self.model_control = HistGradientBoostingClassifier(
            max_iter=80,
            learning_rate=0.06,
            max_depth=3,
            random_state=random_state
        )
        # Model for Treated group (Care Management Outreach Enrolled)
        self.model_treated = HistGradientBoostingClassifier(
            max_iter=80,
            learning_rate=0.06,
            max_depth=3,
            random_state=random_state
        )
        self.fitted = False

    def fit(
        self,
        X: pd.DataFrame,
        treatment: np.ndarray, # 1 = Care outreach, 0 = Standard care
        y: np.ndarray          # 1 = Acute event, 0 = No event
    ) -> "CausalUpliftEngine":
        treat_mask = (treatment == 1)
        ctrl_mask = (treatment == 0)

        # Train control model
        self.model_control.fit(X[ctrl_mask], y[ctrl_mask])
        # Train treated model
        self.model_treated.fit(X[treat_mask], y[treat_mask])
        self.fitted = True
        return self

    def predict_uplift(self, X: pd.DataFrame) -> np.ndarray:
        """Computes ITE = P(Event | Control) - P(Event | Treated).

        Higher positive uplift means the intervention achieves a greater reduction
        in the probability of an acute adverse event.
        """
        p_ctrl = self.model_control.predict_proba(X)[:, 1]
        p_treat = self.model_treated.predict_proba(X)[:, 1]
        # Uplift is risk reduction
        uplift = p_ctrl - p_treat
        return np.clip(uplift, -0.40, 0.50)

    def classify_uplift_segment(self, risk_no_outreach: float, uplift: float) -> str:
        """Classifies member into standard 4-quadrant uplift segments."""
        if uplift > 0.08:
            return "IMPACTABLE_HIGH_PRIORITY"  # Will benefit significantly from care coordination
        elif risk_no_outreach > 0.40 and uplift <= 0.03:
            return "LOST_CAUSE_CHRONIC"        # High baseline risk but refractory to standard outreach
        elif risk_no_outreach < 0.10:
            return "SURE_THING_LOW_RISK"       # Stable, will not have adverse event regardless
        else:
            return "MODERATE_BENEFIT"
