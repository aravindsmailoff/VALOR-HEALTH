"use client";

import { useState } from "react";
import Link from "next/link";
import { Activity, ShieldAlert, CheckCircle2, ArrowRight, Zap, RefreshCw } from "lucide-react";

export default function AegisSpotlight() {
  const [contraindicationCleared, setContraindicationCleared] = useState(false);

  return (
    <section className="section-page dark aegis-spotlight" id="aegis-spotlight">
      <div className="section-inner">
        <div className="aegis-spotlight-grid">
          {/* Narrative Column */}
          <div>
            <div className="section-kicker" style={{ color: "#38bdf8" }}>
              Payer Intelligence Core
            </div>
            <h2 style={{ color: "#fff" }}>
              Powered by AegisTwin. Insurance that protects before illness happens.
            </h2>
            <p className="lead">
              Traditional insurance only answers the phone after disaster strikes. Folio incorporates the{" "}
              <strong>AegisTwin Enterprise Digital Twin</strong>, replaying claims, electronic health records, SDOH, and
              wearables in real-time to intercept adverse medical events before they happen.
            </p>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "20px",
                marginBottom: "36px",
                fontFamily: "var(--font-sans)",
              }}
            >
              <div
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: "12px",
                  padding: "18px",
                }}
              >
                <div style={{ color: "#38bdf8", fontWeight: 700, fontSize: "20px", marginBottom: "4px" }}>
                  100% Sensitivity
                </div>
                <div style={{ color: "#94a3b8", fontSize: "13px" }}>
                  On Golden Safety Contraindications (DDI, DCI, Beers Criteria).
                </div>
              </div>

              <div
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: "12px",
                  padding: "18px",
                }}
              >
                <div style={{ color: "#4ade80", fontWeight: 700, fontSize: "20px", marginBottom: "4px" }}>
                  Zero Lookahead
                </div>
                <div style={{ color: "#94a3b8", fontSize: "13px" }}>
                  Point-in-time state reconstruction prevents clinical data leakage.
                </div>
              </div>
            </div>

            <Link href="/portal" className="btn-portal-launch" style={{ padding: "14px 28px", fontSize: "15px" }}>
              <Activity size={18} />
              Open Live AegisTwin Portal
              <ArrowRight size={16} />
            </Link>
          </div>

          {/* Interactive Live Mini Flight Simulator */}
          <div>
            <div className="aegis-hero-preview-box">
              <div className="preview-pill-header">
                <div className="live-indicator">
                  <div className="live-pulse" />
                  Twin Sensor: Live Telemetry
                </div>
                <span
                  style={{
                    fontSize: "12px",
                    fontFamily: "var(--font-mono)",
                    color: "#94a3b8",
                  }}
                >
                  MEMBER: PT-001 (E. Vance, 72)
                </span>
              </div>

              <div style={{ marginBottom: "20px" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "14px",
                    color: "#cbd5e1",
                    fontFamily: "var(--font-sans)",
                    marginBottom: "8px",
                  }}
                >
                  <span>Calibrated 90-Day Acute Event Risk</span>
                  <span style={{ fontWeight: 800, color: contraindicationCleared ? "#4ade80" : "#f43f5e" }}>
                    {contraindicationCleared ? "19.4% (Low / Controlled)" : "74.0% (Critical Tripwire)"}
                  </span>
                </div>

                <div
                  style={{
                    height: "10px",
                    background: "rgba(255,255,255,0.1)",
                    borderRadius: "5px",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      height: "100%",
                      width: contraindicationCleared ? "19.4%" : "74%",
                      background: contraindicationCleared
                        ? "linear-gradient(90deg, #10b981, #34d399)"
                        : "linear-gradient(90deg, #f43f5e, #fb7185)",
                      transition: "width 0.5s cubic-bezier(0.16, 1, 0.3, 1), background 0.5s ease",
                    }}
                  />
                </div>
              </div>

              {/* Tripwire Box */}
              {!contraindicationCleared ? (
                <div
                  style={{
                    background: "rgba(244, 63, 94, 0.12)",
                    border: "1px solid rgba(244, 63, 94, 0.4)",
                    borderRadius: "12px",
                    padding: "16px",
                    marginBottom: "20px",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#f43f5e", fontWeight: 700, fontSize: "14px", marginBottom: "6px" }}>
                    <ShieldAlert size={16} />
                    Active DCI Tripwire Detected
                  </div>
                  <div style={{ fontSize: "13px", color: "#e2e8f0", lineHeight: 1.4 }}>
                    Metformin prescribed with renal eGFR 27.4 mL/min (Contraindicated threshold &lt; 30). Elevated lactic acidosis hazard.
                  </div>
                </div>
              ) : (
                <div
                  style={{
                    background: "rgba(16, 185, 129, 0.12)",
                    border: "1px solid rgba(16, 185, 129, 0.4)",
                    borderRadius: "12px",
                    padding: "16px",
                    marginBottom: "20px",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#10b981", fontWeight: 700, fontSize: "14px", marginBottom: "6px" }}>
                    <CheckCircle2 size={16} />
                    Counterfactual Simulation: Contraindication Resolved
                  </div>
                  <div style={{ fontSize: "13px", color: "#e2e8f0", lineHeight: 1.4 }}>
                    Metformin safely deprescribed → transitioned to Linagliptin. Projected insurer 90d savings: $14,200.
                  </div>
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={() => setContraindicationCleared(!contraindicationCleared)}
                style={{
                  width: "100%",
                  padding: "12px",
                  borderRadius: "10px",
                  background: contraindicationCleared ? "rgba(255,255,255,0.1)" : "#f43f5e",
                  color: "#fff",
                  fontFamily: "var(--font-sans)",
                  fontSize: "14px",
                  fontWeight: 600,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "8px",
                  transition: "all 0.2s ease",
                }}
              >
                <RefreshCw size={15} />
                {contraindicationCleared ? "Reset Simulation to Baseline" : "Simulate Clinical Deprescribing Intervention"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
