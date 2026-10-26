"""L2-Regularized Logistic Regression Baseline Pipeline."""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class BaselineLogisticRegression:
    """Standardized L2-regularized baseline model for clinical benchmark comparisons."""

    def __init__(self, c_param: float = 1.0, random_state: int = 42):
        self.c_param = c_param
        self.random_state = random_state
        self.pipeline: Pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                C=c_param,
                penalty="l2",
                solver="lbfgs",
                max_iter=500,
                random_state=random_state,
                class_weight="balanced"
            ))
        ])

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> "BaselineLogisticRegression":
        self.pipeline.fit(X, y)
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.pipeline.predict_proba(X)[:, 1]

    def get_coefficients(self, feature_names: list) -> Dict[str, float]:
        coefs = self.pipeline.named_steps["clf"].coef_[0]
        return {name: float(c) for name, c in zip(feature_names, coefs)}
