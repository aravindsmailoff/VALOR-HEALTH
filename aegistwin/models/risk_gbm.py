"""Multi-Outcome Gradient Boosted Trees with LightGBM and HistGradientBoosting Fallback."""

import logging
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except Exception:
    HAS_LIGHTGBM = False

from sklearn.ensemble import HistGradientBoostingClassifier

logger = logging.getLogger(__name__)

class RiskGBM:
    """Gradient boosted classification engine for a single clinical outcome."""

    def __init__(
        self,
        target_name: str = "outcome_90d_acute",
        n_estimators: int = 120,
        learning_rate: float = 0.05,
        max_depth: int = 4,
        random_state: int = 42
    ):
        self.target_name = target_name
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = None
        self.using_lightgbm = False
        self._init_model()

    def _init_model(self):
        if HAS_LIGHTGBM:
            try:
                self.model = lgb.LGBMClassifier(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    max_depth=self.max_depth,
                    num_leaves=15,
                    subsample=0.85,
                    colsample_bytree=0.85,
                    random_state=self.random_state,
                    verbose=-1,
                    importance_type="gain"
                )
                self.using_lightgbm = True
                return
            except Exception as e:
                logger.warning(f"LightGBM initialization failed ({e}), falling back to HistGradientBoostingClassifier.")

        # Fallback
        self.model = HistGradientBoostingClassifier(
            max_iter=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_state
        )
        self.using_lightgbm = False

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> "RiskGBM":
        self.model.fit(X, y)
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(X)[:, 1]

class MultiOutcomeRiskEngine:
    """Orchestrates multi-outcome prediction models for 90d Acute, 30d Readmit, and 12m Progression."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model_90d_acute = RiskGBM(target_name="outcome_90d_acute", random_state=random_state)
        self.model_30d_readmit = RiskGBM(target_name="outcome_30d_readmission", random_state=random_state)
        self.model_12m_prog = RiskGBM(target_name="outcome_12m_progression", random_state=random_state)

    def fit_all(
        self,
        X_train: pd.DataFrame,
        y_acute: np.ndarray,
        y_readmit: np.ndarray,
        y_prog: np.ndarray
    ) -> "MultiOutcomeRiskEngine":
        self.model_90d_acute.fit(X_train, y_acute)
        self.model_30d_readmit.fit(X_train, y_readmit)
        self.model_12m_prog.fit(X_train, y_prog)
        return self

    def predict_all(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        return {
            "risk_90d_acute": self.model_90d_acute.predict_proba(X),
            "risk_30d_readmit": self.model_30d_readmit.predict_proba(X),
            "risk_12m_prog": self.model_12m_prog.predict_proba(X)
        }
