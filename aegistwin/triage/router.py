"""3-Tier CDS Alert Router and Care-Team Capacity Tiering Engine."""

from typing import Any, Dict, List, Optional
import numpy as np
from pydantic import BaseModel

from aegistwin.config.settings import settings
from aegistwin.safety.ddi_engine import SafetyFinding
from aegistwin.twin.state import MemberDigitalTwin

class CDSTriageAlert(BaseModel):
    alert_id: str
    patient_id: str
    tier: str  # TIER_1_RED, TIER_2_YELLOW, TIER_3_GREEN
    title: str
    summary_clinical: str
    summary_layman: str
    requires_interrupt: bool
    requires_override_reason: bool
    recommended_action: str
    target_queue: str  # CLINICAL_PHARMACIST_STAT, CARE_MANAGER_WEEKLY, PASSIVE_AUDIT_LOG

class TriageRouter:
    """Classifies risk tiers and routes CDS alerts through the anti-alert-fatigue matrix."""

    def __init__(
        self,
        high_risk_quantile: float = settings.TIER_HIGH_QUANTILE,
        med_risk_quantile: float = settings.TIER_MEDIUM_QUANTILE
    ):
        self.high_risk_quantile = high_risk_quantile
        self.med_risk_quantile = med_risk_quantile

    def assign_population_risk_tiers(
        self,
        risk_scores: np.ndarray,
        uplift_scores: Optional[np.ndarray] = None
    ) -> List[str]:
        """Assigns High (Top 5%), Medium (Next 15%), and Low (Remaining 80%) tiers aligned with capacity."""
        n = len(risk_scores)
        if n == 0:
            return []

        # Weighted priority = risk * (1.0 + max(0, uplift))
        if uplift_scores is not None:
            priority_scores = risk_scores * (1.0 + np.maximum(0.0, uplift_scores))
        else:
            priority_scores = risk_scores

        high_thresh = np.quantile(priority_scores, self.high_risk_quantile)
        med_thresh = np.quantile(priority_scores, self.med_risk_quantile)

        tiers = []
        for s in priority_scores:
            if s >= high_thresh:
                tiers.append("High")
            elif s >= med_thresh:
                tiers.append("Medium")
            else:
                tiers.append("Low")
        return tiers

    def route_alert(
        self,
        twin: MemberDigitalTwin,
        risk_90d: float,
        safety_findings: List[SafetyFinding],
        risk_delta: float = 0.0,
        has_wearable_decompensation: bool = False
    ) -> CDSTriageAlert:
        """Applies 3-Tier Anti-Alert-Fatigue Matrix."""
        pid = twin.patient_id
        critical_findings = [f for f in safety_findings if f.severity == "CRITICAL"]
        moderate_findings = [f for f in safety_findings if f.severity == "MODERATE"]

        # 1. Tier 1 — RED ALERT (Interruptive Safety Hard-Stop)
        if critical_findings:
            top_f = critical_findings[0]
            return CDSTriageAlert(
                alert_id=f"ALT-RED-{pid}",
                patient_id=pid,
                tier="TIER_1_RED",
                title=f"CRITICAL SAFETY INTERRUPT: {top_f.rule_id}",
                summary_clinical=f"{top_f.category} Contraindication: {top_f.clinical_mechanism}",
                summary_layman=top_f.plain_english_explanation,
                requires_interrupt=True,
                requires_override_reason=True,
                recommended_action=top_f.recommended_action,
                target_queue="CLINICAL_PHARMACIST_STAT"
            )

        # 2. Tier 2 — YELLOW ALERT (Escalating Trajectory / Outreach Queue)
        if (
            risk_90d >= 0.35 or
            risk_delta >= 0.10 or
            has_wearable_decompensation or
            len(moderate_findings) >= 1
        ):
            reason_parts = []
            if risk_90d >= 0.35: reason_parts.append(f"High Acute Risk ({risk_90d*100:.1f}%)")
            if risk_delta >= 0.10: reason_parts.append(f"Risk Spike ({risk_delta*100:+.1f}%)")
            if has_wearable_decompensation: reason_parts.append("Wearable Decompensation")
            if moderate_findings: reason_parts.append(f"{len(moderate_findings)} Moderate Med Warning(s)")

            return CDSTriageAlert(
                alert_id=f"ALT-YELLOW-{pid}",
                patient_id=pid,
                tier="TIER_2_YELLOW",
                title="RISING RISK ESCALATION",
                summary_clinical=f"Member trajectory accelerating into high risk tier: {'; '.join(reason_parts)}.",
                summary_layman="Patient health data shows increasing strain or missing refills that warrant nurse check-in.",
                requires_interrupt=False,
                requires_override_reason=False,
                recommended_action="Route to weekly Nurse Care Management queue for telephonic clinical outreach.",
                target_queue="CARE_MANAGER_WEEKLY"
            )

        # 3. Tier 3 — GREEN (Passive Longitudinal Log)
        return CDSTriageAlert(
            alert_id=f"ALT-GREEN-{pid}",
            patient_id=pid,
            tier="TIER_3_GREEN",
            title="STABLE LONGITUDINAL TRAJECTORY",
            summary_clinical=f"Stable clinical metrics (Risk 90d: {risk_90d*100:.1f}%, Delta: {risk_delta:+.2f}). No critical contraindications.",
            summary_layman="All health indicators are stable and no active medication clashes were detected.",
            requires_interrupt=False,
            requires_override_reason=False,
            recommended_action="Silent log. Zero clinical interruption required.",
            target_queue="PASSIVE_AUDIT_LOG"
        )
