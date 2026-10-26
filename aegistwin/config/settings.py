"""AegisTwin Global Configuration & Operational Parameters."""

from pathlib import Path
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "artifacts" / "data"
    MODELS_DIR: Path = BASE_DIR / "artifacts" / "models"
    EVAL_DIR: Path = BASE_DIR / "artifacts" / "evaluation"
    AUDIT_LOG_FILE: Path = BASE_DIR / "artifacts" / "audit_log.jsonl"
    
    # Capacity-Tiering Quantiles
    TIER_HIGH_QUANTILE: float = 0.95    # Top 5%
    TIER_MEDIUM_QUANTILE: float = 0.80  # Next 15% (80th to 95th percentile)
    
    # Temporal & Feature Engineering
    LOOKBACK_DAYS: int = 365
    PREDICTION_HORIZON_ACUTE_DAYS: int = 90
    PREDICTION_HORIZON_READMISSION_DAYS: int = 30
    PREDICTION_HORIZON_PROGRESSION_DAYS: int = 365
    
    # Adherence Thresholds
    PDC_ADHERENT_THRESHOLD: float = 0.80
    REFILL_GAP_DISCONTINUED_MULTIPLIER: float = 1.5
    
    # Physiological Drift Thresholds
    EGFR_ACUTE_DROP_THRESHOLD: float = 5.0  # mL/min over 90 days
    HBA1C_SPIKE_THRESHOLD: float = 1.0       # absolute % jump
    WEARABLE_HR_SPIKE_BPM: float = 8.0      # Resting HR increase over 14 days
    WEARABLE_STEPS_DROP_PCT: float = 0.30   # Step volume reduction over 14 days
    
    # Uncertainty & Conformal Prediction
    CONFORMAL_CONFIDENCE_LEVEL: float = 0.90
    SPARSE_DATA_ENROLLMENT_DAYS: int = 90
    
    # Cost & Payer ROI Parameters (Averaged CMS/Health Plan benchmarks)
    AVOIDABLE_ED_COST_USD: float = 1850.0
    AVOIDABLE_INPATIENT_ADM_COST_USD: float = 14200.0
    CARE_MANAGEMENT_OUTREACH_COST_USD: float = 350.0
    
    # RBAC Roles
    ROLE_CLINICAL_DIRECTOR: str = "CLINICAL_DIRECTOR"
    ROLE_CARE_MANAGER: str = "CARE_MANAGER"
    ROLE_PHARMACIST: str = "PHARMACIST"
    ROLE_PAYER_EXECUTIVE: str = "PAYER_EXECUTIVE"
    ROLE_OUTREACH_COORDINATOR: str = "OUTREACH_COORDINATOR"

settings = Settings()
