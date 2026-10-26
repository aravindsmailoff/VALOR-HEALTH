"""Event Sensor: Medication Diff, Rolling PDC Adherence, and Physiological Anomaly Detection."""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel

from aegistwin.data.schemas import MedicationDispense, MemberEvent, MemberEventType, Observation
from aegistwin.twin.state import MemberDigitalTwin

class MedicationDiff(BaseModel):
    diff_type: str  # NEW_DRUG, DOSE_MODIFIED, DISCONTINUED, NON_ADHERENT
    rxnorm_cui: str
    drug_name: str
    details: str
    severity: str = "INFO"  # INFO, WARNING, CRITICAL

class PhysiologicalAnomaly(BaseModel):
    anomaly_type: str  # LAB_DETERIORATION, WEARABLE_DECOMPENSATION
    metric: str
    delta: float
    description: str
    severity: str = "WARNING"

class SensorTelemetryReport(BaseModel):
    medication_diffs: List[MedicationDiff] = []
    physiological_anomalies: List[PhysiologicalAnomaly] = []
    rolling_pdc: Dict[str, float] = {}

class TwinEventSensor:
    """Senses and classifies discrete delta events across medication, lab, and wearable streams."""

    def __init__(self, pdc_threshold: float = 0.80, gap_multiplier: float = 1.5):
        self.pdc_threshold = pdc_threshold
        self.gap_multiplier = gap_multiplier

    def evaluate_new_fill(
        self,
        twin: MemberDigitalTwin,
        new_dispense: MedicationDispense
    ) -> List[MedicationDiff]:
        """Detects whether a prescription fill is a NEW_DRUG, DOSE_MODIFIED, or normal continuation."""
        diffs: List[MedicationDiff] = []
        cui = new_dispense.rxnorm_cui

        if cui not in twin.active_medications:
            diffs.append(MedicationDiff(
                diff_type="NEW_DRUG",
                rxnorm_cui=cui,
                drug_name=new_dispense.drug_name,
                details=f"New chemical entity initiated ({new_dispense.drug_name}, class: {new_dispense.therapeutic_class}) at {new_dispense.dose_mg_per_day} mg/day.",
                severity="INFO"
            ))
        else:
            prev_med = twin.active_medications[cui]
            if abs(new_dispense.dose_mg_per_day - prev_med.dose_mg_per_day) > 1e-3:
                pct = ((new_dispense.dose_mg_per_day - prev_med.dose_mg_per_day) / max(0.1, prev_med.dose_mg_per_day)) * 100
                diffs.append(MedicationDiff(
                    diff_type="DOSE_MODIFIED",
                    rxnorm_cui=cui,
                    drug_name=new_dispense.drug_name,
                    details=f"Dose titration detected: changed from {prev_med.dose_mg_per_day} mg/day to {new_dispense.dose_mg_per_day} mg/day ({pct:+.1f}%).",
                    severity="WARNING" if abs(pct) >= 50 else "INFO"
                ))

        return diffs

    def calculate_rolling_pdc(
        self,
        twin: MemberDigitalTwin,
        as_of: date,
        lookback_days: int = 90
    ) -> Dict[str, float]:
        """Calculates true Proportion of Days Covered (PDC) over lookback_days window per drug."""
        window_start = as_of - timedelta(days=lookback_days)
        pdc_map: Dict[str, float] = {}

        # Group dispenses by RxCUI in the window
        dispenses_in_window: Dict[str, List[Tuple[date, int]]] = {}
        for ev in twin.event_log:
            if ev.event_type == MemberEventType.PRESCRIPTION_FILL:
                d_date = ev.timestamp.date()
                if window_start <= d_date <= as_of:
                    p = ev.payload
                    cui = p["rxnorm_cui"]
                    dispenses_in_window.setdefault(cui, []).append((d_date, int(p.get("days_supply", 30))))

        for cui, fills in dispenses_in_window.items():
            covered_days: set = set()
            for f_date, supply in fills:
                for day_offset in range(supply):
                    c_date = f_date + timedelta(days=day_offset)
                    if window_start <= c_date <= as_of:
                        covered_days.add(c_date)
            pdc = round(len(covered_days) / float(lookback_days), 3)
            pdc_map[cui] = float(min(1.0, pdc))

        return pdc_map

    def check_adherence_and_discontinuations(
        self,
        twin: MemberDigitalTwin,
        as_of: date
    ) -> List[MedicationDiff]:
        """Detects gaps, abrupt discontinuations, and PDC breaches."""
        diffs: List[MedicationDiff] = []
        pdc_map = self.calculate_rolling_pdc(twin, as_of=as_of, lookback_days=90)

        for cui, med in twin.active_medications.items():
            elapsed_days = (as_of - med.last_fill_date).days
            max_allowed = int(med.days_supply * self.gap_multiplier)
            
            # Check Discontinuation
            if elapsed_days > max_allowed:
                is_rebound_risk = cui in ["8703", "6918"] # Beta-blockers (Propranolol, Metoprolol)
                diffs.append(MedicationDiff(
                    diff_type="DISCONTINUED",
                    rxnorm_cui=cui,
                    drug_name=med.drug_name,
                    details=f"Prescription elapsed {elapsed_days} days since fill (exceeds {max_allowed}d threshold)."
                    + (" Severe risk of rebound tachycardia/hypertension from abrupt beta-blocker cessation." if is_rebound_risk else ""),
                    severity="CRITICAL" if is_rebound_risk else "WARNING"
                ))

            # Check rolling PDC
            pdc = pdc_map.get(cui, 0.0)
            if pdc < self.pdc_threshold and elapsed_days > 15:
                diffs.append(MedicationDiff(
                    diff_type="NON_ADHERENT",
                    rxnorm_cui=cui,
                    drug_name=med.drug_name,
                    details=f"Rolling 90-day PDC is {pdc:.2f} (below target {self.pdc_threshold:.2f}). High risk of therapy failure.",
                    severity="WARNING"
                ))

        return diffs

    def check_physiological_drift(
        self,
        twin: MemberDigitalTwin,
        as_of: datetime
    ) -> List[PhysiologicalAnomaly]:
        """Evaluates eGFR slopes, HbA1c spikes, and 14-day wearable decompensation."""
        anomalies: List[PhysiologicalAnomaly] = []

        # 1. eGFR slope over 90 days
        egfr_traj = twin.get_lab_trajectory("33914-3", days=90, as_of=as_of)
        if len(egfr_traj) >= 2:
            first_val = egfr_traj[0][1]
            last_val = egfr_traj[-1][1]
            drop = first_val - last_val
            if drop >= 5.0:
                anomalies.append(PhysiologicalAnomaly(
                    anomaly_type="LAB_DETERIORATION",
                    metric="eGFR",
                    delta=-drop,
                    description=f"Rapid renal decline: eGFR dropped by {drop:.1f} mL/min over past 90 days (from {first_val} to {last_val}).",
                    severity="CRITICAL" if last_val < 30.0 else "WARNING"
                ))

        # 2. HbA1c spike over 180 days
        a1c_traj = twin.get_lab_trajectory("4548-4", days=180, as_of=as_of)
        if len(a1c_traj) >= 2:
            first_val = a1c_traj[0][1]
            last_val = a1c_traj[-1][1]
            rise = last_val - first_val
            if rise >= 1.0:
                anomalies.append(PhysiologicalAnomaly(
                    anomaly_type="LAB_DETERIORATION",
                    metric="HbA1c",
                    delta=rise,
                    description=f"Glycemic decompensation: HbA1c spiked by +{rise:.1f}% to {last_val:.1f}%.",
                    severity="WARNING"
                ))

        # 3. Wearable telemetry decompensation over 14 days
        ref_d = as_of.date()
        w_records = [w for w in twin.wearables if (ref_d - timedelta(days=14)) <= w.date <= ref_d]
        if len(w_records) >= 10:
            w_records.sort(key=lambda x: x.date)
            baseline_steps = sum(w.daily_steps for w in w_records[:5]) / 5.0
            recent_steps = sum(w.daily_steps for w in w_records[-5:]) / 5.0
            baseline_hr = sum(w.resting_heart_rate for w in w_records[:5]) / 5.0
            recent_hr = sum(w.resting_heart_rate for w in w_records[-5:]) / 5.0

            step_drop_pct = (baseline_steps - recent_steps) / max(1.0, baseline_steps)
            hr_rise = recent_hr - baseline_hr

            if step_drop_pct >= 0.30 and hr_rise >= 8.0:
                anomalies.append(PhysiologicalAnomaly(
                    anomaly_type="WEARABLE_DECOMPENSATION",
                    metric="Steps_and_Resting_HR",
                    delta=hr_rise,
                    description=f"Wearable early-warning decompensation: Daily steps plunged {step_drop_pct*100:.1f}% while resting heart rate increased by +{hr_rise:.1f} bpm.",
                    severity="CRITICAL"
                ))

        return anomalies
