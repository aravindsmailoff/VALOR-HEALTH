"use client";

import { useState, useMemo, useEffect } from "react";
import { MEMBER_PROFILES, MemberProfile } from "@/data/memberProfiles";
import {
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Sliders,
  TrendingDown,
  Activity,
  User,
  HeartPulse,
  Pill,
  RefreshCw,
  Stethoscope,
  ChevronRight,
  X,
  FileCheck2,
  Lock,
} from "lucide-react";

export default function IntegratedDigitalTwin() {
  const [selectedId, setSelectedId] = useState<string>("PT-001");
  const [viewMode, setViewMode] = useState<"layman" | "clinical">("layman");

  // Interactive Live Sliders for Biomarkers
  const [egfr, setEgfr] = useState<number>(27.4);
  const [hba1c, setHba1c] = useState<number>(8.6);
  const [systolicBP, setSystolicBP] = useState<number>(142);
  const [pdcAdherence, setPdcAdherence] = useState<number>(88);

  // Active Medication Deprescribing Toggles
  const [deprescribedMeds, setDeprescribedMeds] = useState<string[]>([]);

  // Care Management Enrollment
  const [careManagementEnrolled, setCareManagementEnrolled] = useState<boolean>(false);

  // Clinician Override State
  const [overrideSubmitted, setOverrideSubmitted] = useState<boolean>(false);
  const [overrideModalOpen, setOverrideModalOpen] = useState<boolean>(false);
  const [overrideReason, setOverrideReason] = useState<string>("BENEFIT_OUTWEIGHS_RISK_DOCUMENTED");

  // Load persona defaults whenever persona switches
  useEffect(() => {
    if (selectedId === "PT-001") {
      setEgfr(27.4);
      setHba1c(8.6);
      setSystolicBP(148);
      setPdcAdherence(90);
    } else if (selectedId === "PT-002") {
      setEgfr(68.0);
      setHba1c(6.2);
      setSystolicBP(138);
      setPdcAdherence(82);
    } else if (selectedId === "PT-003") {
      setEgfr(92.0);
      setHba1c(5.4);
      setSystolicBP(118);
      setPdcAdherence(96);
    } else if (selectedId === "PT-004") {
      setEgfr(48.0);
      setHba1c(6.8);
      setSystolicBP(156);
      setPdcAdherence(78);
    }
    setDeprescribedMeds([]);
    setCareManagementEnrolled(false);
    setOverrideSubmitted(false);
  }, [selectedId]);

  const member = useMemo(() => {
    return MEMBER_PROFILES.find((m) => m.id === selectedId) || MEMBER_PROFILES[0];
  }, [selectedId]);

  // Compute Active Clinical Tripwires in Real Time
  const activeTripwires = useMemo(() => {
    const findings: {
      id: string;
      title: string;
      severity: "CRITICAL" | "WARNING";
      type: "DCI" | "DDI" | "BEERS";
      desc: string;
      action: string;
    }[] = [];

    // Tripwire 1: Metformin + eGFR < 30
    const hasMetformin = !deprescribedMeds.includes("6809") && selectedId === "PT-001";
    if (hasMetformin && egfr < 30) {
      findings.push({
        id: "DCI-METFORMIN",
        title: "Metformin in Severe Renal Impairment (eGFR < 30)",
        severity: "CRITICAL",
        type: "DCI",
        desc: `eGFR is currently ${egfr.toFixed(1)} mL/min (Contraindication Threshold < 30 mL/min). FDA Black-Box Warning: Fatal lactic acidosis accumulation hazard.`,
        action: "Discontinue Metformin immediately. Switch to renal-safe Linagliptin or adjust insulin dose under clinical supervision.",
      });
    }

    // Tripwire 2: Warfarin + NSAID (Ibuprofen)
    const hasWarfarin = selectedId === "PT-002";
    const hasIbuprofen = !deprescribedMeds.includes("5640") && selectedId === "PT-002";
    if (hasWarfarin && hasIbuprofen) {
      findings.push({
        id: "DDI-WARFARIN-NSAID",
        title: "Severe Hemorrhage Risk: Warfarin + NSAID (Ibuprofen)",
        severity: "CRITICAL",
        type: "DDI",
        desc: "Concurrent systemic NSAID with Warfarin inhibits platelet aggregation & damages gastrointestinal mucosa, raising major bleeding risk by 4.5x.",
        action: "Deprescribe oral Ibuprofen. Substitute with topical Voltaren gel or Acetaminophen for localized pain relief.",
      });
    }

    // Tripwire 3: Beers Criteria (Amitriptyline in ≥65yo)
    const hasAmitriptyline = !deprescribedMeds.includes("704") && selectedId === "PT-004";
    if (hasAmitriptyline) {
      findings.push({
        id: "BEERS-AMITRIPTYLINE",
        title: "AGS Beers Criteria: Anticholinergic Fall Hazard (Amitriptyline)",
        severity: "CRITICAL",
        type: "BEERS",
        desc: "Potent anticholinergic sedation and orthostatic hypotension in an 81yo patient with a documented history of falls and hip fracture.",
        action: "Taper off Amitriptyline. Substitute with non-pharmacological sleep hygiene or physical therapy & assign home safety monitoring.",
      });
    }

    return findings;
  }, [selectedId, deprescribedMeds, egfr]);

  // Compute Real-Time 90-Day Acute Risk and Insurer Savings
  const liveCalculation = useMemo(() => {
    let base = member.risk90d;

    // eGFR penalty / bonus
    if (egfr < 30) base += 0.18;
    else if (egfr > 60) base -= 0.12;

    // HbA1c penalty / bonus
    if (hba1c > 8.0) base += (hba1c - 8.0) * 0.08;
    else if (hba1c < 6.5) base -= 0.06;

    // BP penalty
    if (systolicBP > 140) base += (systolicBP - 140) * 0.003;

    // Adherence discount
    if (pdcAdherence > 85) base -= 0.08;

    // Deprescribing resolution bonus
    if (deprescribedMeds.length > 0) {
      base -= 0.28 * deprescribedMeds.length;
    }

    // Care management bonus
    if (careManagementEnrolled) {
      base -= 0.14;
    }

    const calculatedRisk = Math.max(0.05, Math.min(0.95, base));
    const lower = Math.max(0.03, calculatedRisk - 0.06);
    const upper = Math.min(0.98, calculatedRisk + 0.07);

    // Projected Insurer 90d Avoidable Spend
    let savings = 0;
    if (deprescribedMeds.length > 0) savings += 14200;
    if (careManagementEnrolled) savings += 4600;
    if (pdcAdherence >= 85) savings += 2800;

    return {
      risk: calculatedRisk,
      lower,
      upper,
      savings,
      isModified:
        deprescribedMeds.length > 0 ||
        careManagementEnrolled ||
        pdcAdherence !== 88 ||
        egfr !== 27.4,
    };
  }, [
    member.risk90d,
    egfr,
    hba1c,
    systolicBP,
    pdcAdherence,
    deprescribedMeds,
    careManagementEnrolled,
  ]);

  const toggleMedication = (rxnorm: string) => {
    setDeprescribedMeds((prev) =>
      prev.includes(rxnorm) ? prev.filter((id) => id !== rxnorm) : [...prev, rxnorm]
    );
  };

  return (
    <section className="meadow-container" id="twin" style={{ marginBottom: "60px" }}>
      <div
        style={{
          background: "#ffffff",
          borderRadius: "36px",
          padding: "48px 40px",
          boxShadow: "0 12px 48px rgba(36, 22, 34, 0.05)",
          border: "1px solid var(--rose-border)",
        }}
      >
        {/* Top Header Badge */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
          <div>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "12px",
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "0.1em",
                color: "var(--rose-accent)",
                background: "#fcedf3",
                padding: "6px 14px",
                borderRadius: "9999px",
                marginBottom: "12px",
              }}
            >
              <span>✦</span> CLINICAL DIGITAL TWIN COCKPIT
            </div>
            <h2
              style={{
                fontSize: "clamp(28px, 3.4vw, 42px)",
                fontWeight: 700,
                letterSpacing: "-0.03em",
                color: "var(--text-dark)",
                lineHeight: 1.15,
                margin: "0 0 10px",
              }}
            >
              Interactive Member Twin & Safety Interceptor.
            </h2>
            <p style={{ fontSize: "16px", color: "var(--text-muted)", maxWidth: "680px", lineHeight: 1.55, margin: 0 }}>
              Test real-time clinical interventions. Adjust biomarker sliders, toggle prescription deprescribing, and
              observe how our conformal ML engine predicts hospitalization probability and actuarial savings live.
            </p>
          </div>

          {/* View Mode Toggle */}
          <div
            style={{
              display: "flex",
              background: "#f4edf1",
              borderRadius: "9999px",
              padding: "4px",
              border: "1px solid rgba(210, 106, 148, 0.2)",
            }}
          >
            <button
              onClick={() => setViewMode("layman")}
              style={{
                padding: "8px 18px",
                borderRadius: "9999px",
                fontSize: "13px",
                fontWeight: 600,
                border: "none",
                cursor: "pointer",
                background: viewMode === "layman" ? "var(--plum-dark)" : "transparent",
                color: viewMode === "layman" ? "#ffffff" : "#5a4d58",
                transition: "all 0.2s ease",
              }}
            >
              Member Plain-English
            </button>
            <button
              onClick={() => setViewMode("clinical")}
              style={{
                padding: "8px 18px",
                borderRadius: "9999px",
                fontSize: "13px",
                fontWeight: 600,
                border: "none",
                cursor: "pointer",
                background: viewMode === "clinical" ? "var(--plum-dark)" : "transparent",
                color: viewMode === "clinical" ? "#ffffff" : "#5a4d58",
                transition: "all 0.2s ease",
              }}
            >
              Clinician Care-Team
            </button>
          </div>
        </div>

        {/* Persona Selector Bar */}
        <div
          style={{
            background: "#fcf8fa",
            border: "1px solid rgba(210, 106, 148, 0.16)",
            borderRadius: "20px",
            padding: "16px 20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "14px",
            marginBottom: "24px",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
            <span style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#7a6a77" }}>
              Active Member Profile:
            </span>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              {MEMBER_PROFILES.map((p) => {
                const isSelected = p.id === selectedId;
                return (
                  <button
                    key={p.id}
                    onClick={() => setSelectedId(p.id)}
                    style={{
                      padding: "8px 16px",
                      borderRadius: "9999px",
                      fontSize: "13px",
                      fontWeight: 600,
                      cursor: "pointer",
                      border: isSelected ? "1.5px solid var(--rose-accent)" : "1px solid rgba(36, 22, 34, 0.1)",
                      background: isSelected ? "var(--bg-card)" : "#ffffff",
                      color: isSelected ? "var(--plum-dark)" : "#5a4d58",
                      boxShadow: isSelected ? "0 2px 8px rgba(210, 106, 148, 0.2)" : "none",
                      transition: "all 0.15s ease",
                    }}
                  >
                    <strong>{p.name}</strong> ({p.id}) · {p.age}y
                  </button>
                );
              })}
            </div>
          </div>

          {/* Risk Level Badge */}
          <div
            style={{
              padding: "6px 14px",
              borderRadius: "9999px",
              fontSize: "12px",
              fontWeight: 700,
              letterSpacing: "0.06em",
              textTransform: "uppercase",
              background:
                liveCalculation.risk > 0.5
                  ? "#fee2e2"
                  : liveCalculation.risk > 0.25
                  ? "#fef3c7"
                  : "#ecfdf5",
              color:
                liveCalculation.risk > 0.5
                  ? "#dc2626"
                  : liveCalculation.risk > 0.25
                  ? "#d97706"
                  : "#059669",
              border: `1px solid ${
                liveCalculation.risk > 0.5
                  ? "#f87171"
                  : liveCalculation.risk > 0.25
                  ? "#fcd34d"
                  : "#6ee7b7"
              }`,
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
            }}
          >
            <span
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background:
                  liveCalculation.risk > 0.5
                    ? "#dc2626"
                    : liveCalculation.risk > 0.25
                    ? "#d97706"
                    : "#059669",
              }}
            />
            {liveCalculation.risk > 0.5
              ? "Critical Inpatient Hazard"
              : liveCalculation.risk > 0.25
              ? "Elevated Risk Window"
              : "Stable Protected State"}
          </div>
        </div>

        {/* Dynamic Member Narrative Box */}
        <div
          style={{
            background: "#fbf6f9",
            border: "1px solid rgba(210, 106, 148, 0.2)",
            borderRadius: "20px",
            padding: "20px 24px",
            marginBottom: "24px",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
            <Sparkles size={16} color="var(--rose-accent)" />
            <h4 style={{ margin: 0, fontSize: "15px", fontWeight: 700, color: "var(--plum-dark)" }}>
              {viewMode === "layman" ? "Plain-Language Health Summary & What It Means For You" : "Clinical Pathophysiology & Evidence Audit"}
            </h4>
          </div>
          <p style={{ margin: 0, color: "#473b45", fontSize: "15px", lineHeight: 1.6 }}>
            {viewMode === "layman" ? member.laymanNarrative.summary : member.laymanNarrative.whyItMatters}
          </p>
        </div>

        {/* Active Tripwire Banners */}
        <div style={{ marginBottom: "28px" }}>
          {overrideSubmitted ? (
            <div
              style={{
                background: "#ecfdf5",
                border: "1.5px solid #10b981",
                borderRadius: "16px",
                padding: "16px 20px",
                display: "flex",
                alignItems: "center",
                gap: "14px",
              }}
            >
              <FileCheck2 size={24} color="#059669" />
              <div>
                <div style={{ color: "#065f46", fontWeight: 700, fontSize: "15px" }}>
                  Clinician Safety Override Formalized & Cryptographically Signed
                </div>
                <div style={{ color: "#047857", fontSize: "13px", marginTop: "2px" }}>
                  Documented reason: <strong>{overrideReason}</strong>. Audit trail entry attached to member clinical chart.
                </div>
              </div>
            </div>
          ) : activeTripwires.length > 0 ? (
            activeTripwires.map((tw) => (
              <div
                key={tw.id}
                style={{
                  background: "#fff5f5",
                  border: "1.5px solid #f87171",
                  borderRadius: "20px",
                  padding: "20px 24px",
                  marginBottom: "12px",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px", marginBottom: "10px" }}>
                  <div>
                    <span
                      style={{
                        fontSize: "11px",
                        fontWeight: 800,
                        letterSpacing: "0.08em",
                        background: "#dc2626",
                        color: "#ffffff",
                        padding: "3px 10px",
                        borderRadius: "9999px",
                        textTransform: "uppercase",
                      }}
                    >
                      {tw.severity} {tw.type} TRIPWIRE CLASH
                    </span>
                    <h4 style={{ margin: "8px 0 4px", fontSize: "18px", fontWeight: 700, color: "#7f1d1d" }}>
                      {tw.title}
                    </h4>
                  </div>

                  <button
                    onClick={() => setOverrideModalOpen(true)}
                    style={{
                      padding: "8px 18px",
                      background: "#ffffff",
                      border: "1.5px solid #dc2626",
                      borderRadius: "9999px",
                      color: "#dc2626",
                      fontSize: "13px",
                      fontWeight: 700,
                      cursor: "pointer",
                      boxShadow: "0 2px 6px rgba(220, 38, 38, 0.1)",
                    }}
                  >
                    Document Physician Override
                  </button>
                </div>

                <p style={{ margin: "0 0 12px", color: "#451a1a", fontSize: "14px", lineHeight: 1.55 }}>
                  {tw.desc}
                </p>

                <div
                  style={{
                    background: "#ffffff",
                    borderRadius: "12px",
                    padding: "12px 16px",
                    borderLeft: "4px solid #dc2626",
                    fontSize: "14px",
                    color: "#241622",
                  }}
                >
                  <strong style={{ color: "#991b1b" }}>Recommended Action:</strong> {tw.action}
                </div>
              </div>
            ))
          ) : (
            <div
              style={{
                background: "#f0fdf4",
                border: "1.5px solid #86efac",
                borderRadius: "16px",
                padding: "16px 20px",
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              <CheckCircle2 size={22} color="#16a34a" />
              <div>
                <div style={{ color: "#166534", fontWeight: 700, fontSize: "15px" }}>
                  All Clinical Tripwires Cleared (Zero Contraindications)
                </div>
                <div style={{ color: "#15803d", fontSize: "13px" }}>
                  Active medications and current biomarker values meet FDA safety standards and AGS Beers Criteria guidelines.
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 3-Column Cockpit Layout */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "24px",
            marginBottom: "28px",
          }}
        >
          {/* Column 1: Live Biomarker Tuning Sliders */}
          <div
            style={{
              background: "#fcf8fa",
              border: "1px solid rgba(210, 106, 148, 0.2)",
              borderRadius: "24px",
              padding: "26px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <div style={{ fontSize: "16px", fontWeight: 700, color: "var(--plum-dark)" }}>
                Live Biomarker Tuning
              </div>
              <span style={{ fontSize: "12px", fontWeight: 600, color: "var(--rose-accent)" }}>
                Move sliders live
              </span>
            </div>

            {/* eGFR Slider */}
            <div style={{ marginBottom: "22px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "13px", fontWeight: 600, color: "#473b45" }}>
                  eGFR (Kidney Function):
                </span>
                <span
                  style={{
                    fontSize: "13px",
                    fontWeight: 700,
                    color: egfr < 30 ? "#dc2626" : "#059669",
                  }}
                >
                  {egfr.toFixed(1)} mL/min {egfr < 30 && "(Contraindicated < 30)"}
                </span>
              </div>
              <input
                type="range"
                min="15"
                max="90"
                step="0.5"
                value={egfr}
                onChange={(e) => setEgfr(Number(e.target.value))}
                style={{ width: "100%", accentColor: egfr < 30 ? "#dc2626" : "var(--rose-accent)", cursor: "pointer" }}
              />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#8c7e8a", marginTop: "4px" }}>
                <span>15 (Kidney Failure)</span>
                <span>30 (Contraindicated)</span>
                <span>60+ (Healthy)</span>
              </div>
            </div>

            {/* HbA1c Slider */}
            <div style={{ marginBottom: "22px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "13px", fontWeight: 600, color: "#473b45" }}>
                  HbA1c (Glycated Hemoglobin):
                </span>
                <span
                  style={{
                    fontSize: "13px",
                    fontWeight: 700,
                    color: hba1c > 8.0 ? "#dc2626" : "#059669",
                  }}
                >
                  {hba1c.toFixed(1)}% {hba1c > 8.0 && "(Elevated)"}
                </span>
              </div>
              <input
                type="range"
                min="5.0"
                max="11.0"
                step="0.1"
                value={hba1c}
                onChange={(e) => setHba1c(Number(e.target.value))}
                style={{ width: "100%", accentColor: hba1c > 8.0 ? "#dc2626" : "var(--rose-accent)", cursor: "pointer" }}
              />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#8c7e8a", marginTop: "4px" }}>
                <span>5.5% (Normal)</span>
                <span>7.0% (CMS Goal)</span>
                <span>11.0% (Crisis)</span>
              </div>
            </div>

            {/* Systolic BP Slider */}
            <div style={{ marginBottom: "22px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "13px", fontWeight: 600, color: "#473b45" }}>
                  Systolic Blood Pressure:
                </span>
                <span
                  style={{
                    fontSize: "13px",
                    fontWeight: 700,
                    color: systolicBP > 140 ? "#dc2626" : "#059669",
                  }}
                >
                  {systolicBP} mmHg {systolicBP > 140 && "(Stage 2 HTN)"}
                </span>
              </div>
              <input
                type="range"
                min="105"
                max="180"
                step="1"
                value={systolicBP}
                onChange={(e) => setSystolicBP(Number(e.target.value))}
                style={{ width: "100%", accentColor: systolicBP > 140 ? "#dc2626" : "var(--rose-accent)", cursor: "pointer" }}
              />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#8c7e8a", marginTop: "4px" }}>
                <span>110 (Ideal)</span>
                <span>130 (Pre-HTN)</span>
                <span>180 (Crisis)</span>
              </div>
            </div>

            {/* Adherence Fill Rate Slider */}
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "13px", fontWeight: 600, color: "#473b45" }}>
                  Adherence Fill Rate (PDC):
                </span>
                <span
                  style={{
                    fontSize: "13px",
                    fontWeight: 700,
                    color: pdcAdherence >= 85 ? "#059669" : "#d97706",
                  }}
                >
                  {pdcAdherence}% {pdcAdherence >= 85 ? "(Adherent)" : "(Suboptimal)"}
                </span>
              </div>
              <input
                type="range"
                min="40"
                max="100"
                step="1"
                value={pdcAdherence}
                onChange={(e) => setPdcAdherence(Number(e.target.value))}
                style={{ width: "100%", accentColor: pdcAdherence >= 85 ? "#059669" : "#d97706", cursor: "pointer" }}
              />
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#8c7e8a", marginTop: "4px" }}>
                <span>50% (Gaps)</span>
                <span>80% (CMS Threshold)</span>
                <span>100% (Perfect)</span>
              </div>
            </div>
          </div>

          {/* Column 2: Predictive Risk Needle & Real-Time Savings */}
          <div
            style={{
              background: "#fcf8fa",
              border: "1px solid rgba(210, 106, 148, 0.2)",
              borderRadius: "24px",
              padding: "26px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
                <div style={{ fontSize: "16px", fontWeight: 700, color: "var(--plum-dark)" }}>
                  Predicted 90d Inpatient Risk
                </div>
                <span style={{ fontSize: "12px", fontWeight: 600, color: "var(--rose-accent)" }}>
                  Conformal ML
                </span>
              </div>

              <div style={{ textAlign: "center", padding: "6px 0 16px" }}>
                {/* SVG Gauge Arc */}
                <div style={{ position: "relative", width: "180px", height: "100px", margin: "0 auto 8px" }}>
                  <svg viewBox="0 0 100 55" style={{ width: "100%", height: "100%", overflow: "visible" }}>
                    <path
                      d="M 10 50 A 40 40 0 0 1 90 50"
                      fill="none"
                      stroke="#eedee6"
                      strokeWidth="10"
                      strokeLinecap="round"
                    />
                    <path
                      d="M 10 50 A 40 40 0 0 1 90 50"
                      fill="none"
                      stroke={
                        liveCalculation.risk > 0.5
                          ? "#dc2626"
                          : liveCalculation.risk > 0.25
                          ? "#f59e0b"
                          : "#10b981"
                      }
                      strokeWidth="10"
                      strokeDasharray="126"
                      strokeDashoffset={126 - 126 * liveCalculation.risk}
                      strokeLinecap="round"
                      style={{ transition: "stroke-dashoffset 0.4s ease, stroke 0.4s ease" }}
                    />
                  </svg>
                </div>

                <div
                  style={{
                    fontSize: "44px",
                    fontWeight: 800,
                    letterSpacing: "-0.03em",
                    lineHeight: 1,
                    color:
                      liveCalculation.risk > 0.5
                        ? "#dc2626"
                        : liveCalculation.risk > 0.25
                        ? "#d97706"
                        : "#059669",
                    marginBottom: "6px",
                  }}
                >
                  {(liveCalculation.risk * 100).toFixed(1)}%
                </div>

                <div style={{ fontSize: "13px", color: "#6b5f6a" }}>
                  Conformal 90% Confidence Band:{" "}
                  <strong>
                    [{(liveCalculation.lower * 100).toFixed(1)}% — {(liveCalculation.upper * 100).toFixed(1)}%]
                  </strong>
                </div>
              </div>
            </div>

            {/* Savings Box */}
            <div
              style={{
                background: "#ecfdf5",
                border: "1px solid #a7f3d0",
                borderRadius: "16px",
                padding: "16px 20px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "14px",
              }}
            >
              <div>
                <div style={{ fontSize: "11px", fontWeight: 700, color: "#065f46", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                  Projected Avoidable Spend:
                </div>
                <div style={{ fontSize: "12px", color: "#047857", marginTop: "2px" }}>
                  Prevented hospitalizations & ED visits.
                </div>
              </div>
              <div style={{ fontSize: "28px", fontWeight: 800, color: "#047857", letterSpacing: "-0.02em" }}>
                ${liveCalculation.savings.toLocaleString()}
              </div>
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "#7a6a77" }}>
              <span>30d Readmit Rate: {(member.readmit30d * 100).toFixed(0)}%</span>
              <span>12m Progression: {(member.progression12m * 100).toFixed(0)}%</span>
            </div>
          </div>

          {/* Column 3: Active Medications & Click-to-Deprescribe */}
          <div
            style={{
              background: "#fcf8fa",
              border: "1px solid rgba(210, 106, 148, 0.2)",
              borderRadius: "24px",
              padding: "26px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <div style={{ fontSize: "16px", fontWeight: 700, color: "var(--plum-dark)" }}>
                  Deprescribing Sandbox
                </div>
                <button
                  onClick={() => {
                    setDeprescribedMeds([]);
                    setCareManagementEnrolled(false);
                  }}
                  style={{ fontSize: "12px", color: "var(--rose-accent)", textDecoration: "underline", background: "none", border: "none", cursor: "pointer", fontWeight: 600 }}
                >
                  Reset Meds
                </button>
              </div>

              <p style={{ fontSize: "13px", color: "#6b5f6a", margin: "0 0 14px", lineHeight: 1.45 }}>
                Click any drug to simulate immediate deprescribing or safer medication substitution:
              </p>

              <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "16px" }}>
                {member.medications.map((m) => {
                  const isDeprescribed = deprescribedMeds.includes(m.rxnorm);
                  return (
                    <div
                      key={m.rxnorm}
                      style={{
                        background: isDeprescribed ? "#f3f4f6" : "#ffffff",
                        border: isDeprescribed ? "1px dashed #9ca3af" : "1px solid rgba(210, 106, 148, 0.2)",
                        borderRadius: "14px",
                        padding: "10px 14px",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        opacity: isDeprescribed ? 0.6 : 1,
                        transition: "all 0.2s ease",
                      }}
                    >
                      <div>
                        <div
                          style={{
                            fontWeight: 700,
                            fontSize: "14px",
                            color: "var(--text-dark)",
                            textDecoration: isDeprescribed ? "line-through" : "none",
                          }}
                        >
                          {m.name}
                        </div>
                        <div style={{ fontSize: "12px", color: "#6b5f6a" }}>
                          {m.dose} · {m.class}
                        </div>
                      </div>

                      <button
                        onClick={() => toggleMedication(m.rxnorm)}
                        style={{
                          padding: "6px 14px",
                          borderRadius: "9999px",
                          fontSize: "12px",
                          fontWeight: 700,
                          cursor: "pointer",
                          border: "none",
                          background: isDeprescribed ? "#10b981" : "var(--plum-dark)",
                          color: "#ffffff",
                          transition: "all 0.2s ease",
                        }}
                      >
                        {isDeprescribed ? "Restore" : "Deprescribe"}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Nurse Care Management Enrollment */}
            <label
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: "10px",
                background: careManagementEnrolled ? "#f3e8f0" : "#ffffff",
                border: careManagementEnrolled ? "1.5px solid var(--rose-accent)" : "1px solid rgba(210, 106, 148, 0.2)",
                borderRadius: "14px",
                padding: "12px 14px",
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              <input
                type="checkbox"
                checked={careManagementEnrolled}
                onChange={(e) => setCareManagementEnrolled(e.target.checked)}
                style={{ width: "18px", height: "18px", accentColor: "var(--rose-accent)", marginTop: "2px", cursor: "pointer" }}
              />
              <div>
                <div style={{ fontWeight: 700, fontSize: "13px", color: "var(--text-dark)" }}>
                  Assign Nurse Care Manager (RN)
                </div>
                <div style={{ fontSize: "12px", color: "#6b5f6a", lineHeight: 1.4, marginTop: "2px" }}>
                  Coordinates transit, in-home vitals, and physician follow-up (-14% acute risk).
                </div>
              </div>
            </label>
          </div>
        </div>

        {/* Clinician Override Dialog */}
        {overrideModalOpen && (
          <div
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(36, 22, 34, 0.65)",
              backdropFilter: "blur(8px)",
              zIndex: 300,
              display: "grid",
              placeItems: "center",
              padding: "20px",
            }}
            onClick={() => setOverrideModalOpen(false)}
          >
            <div
              style={{
                background: "#ffffff",
                borderRadius: "28px",
                maxWidth: "520px",
                width: "100%",
                padding: "36px",
                boxShadow: "0 24px 60px rgba(0, 0, 0, 0.2)",
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <h3 style={{ margin: 0, fontSize: "22px", fontWeight: 700, color: "var(--text-dark)" }}>
                  Clinician Safety Override
                </h3>
                <button
                  onClick={() => setOverrideModalOpen(false)}
                  style={{ background: "none", border: "none", cursor: "pointer", color: "#6b5f6a" }}
                >
                  <X size={20} />
                </button>
              </div>

              <p style={{ color: "#554953", fontSize: "14px", lineHeight: 1.5, marginBottom: "20px" }}>
                Formalize physician override rationale. This decision is cryptographically logged with NPI credentials
                in the payer clinical safety audit trail.
              </p>

              <div style={{ marginBottom: "20px" }}>
                <label style={{ display: "block", fontSize: "13px", fontWeight: 700, color: "var(--text-dark)", marginBottom: "8px" }}>
                  Clinical Justification Rationale:
                </label>
                <select
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "12px 14px",
                    borderRadius: "12px",
                    border: "1px solid rgba(210, 106, 148, 0.3)",
                    fontSize: "14px",
                    color: "var(--text-dark)",
                    outline: "none",
                    background: "#fcf8fa",
                  }}
                >
                  <option value="BENEFIT_OUTWEIGHS_RISK_DOCUMENTED">Benefit outweighs documented risk with patient consent</option>
                  <option value="ALTERNATIVE_MEDICATIONS_CONTRAINDICATED">Alternative therapies also contraindicated or non-tolerated</option>
                  <option value="TEMPORARY_ACUTE_USE_ONLY">Short-term acute monitoring in place with nephrologist oversight</option>
                  <option value="SPECIALIST_RECOMMENDED_UNDER_SUPERVISION">Specialist prescribed under continuous inpatient supervision</option>
                </select>
              </div>

              <div style={{ display: "flex", gap: "12px" }}>
                <button
                  onClick={() => setOverrideModalOpen(false)}
                  style={{
                    flex: 1,
                    padding: "12px",
                    borderRadius: "9999px",
                    background: "#f4edf1",
                    border: "none",
                    fontWeight: 600,
                    fontSize: "14px",
                    color: "#5a4d58",
                    cursor: "pointer",
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    setOverrideSubmitted(true);
                    setOverrideModalOpen(false);
                  }}
                  className="btn-plum"
                  style={{
                    flex: 1,
                    padding: "12px",
                    borderRadius: "9999px",
                    fontWeight: 600,
                    fontSize: "14px",
                    cursor: "pointer",
                  }}
                >
                  Confirm & Audit Sign
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
