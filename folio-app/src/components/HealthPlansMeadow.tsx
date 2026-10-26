"use client";

import { useState } from "react";
import { Check, ShieldCheck, HeartPulse, Sparkles, Building2, UserCheck } from "lucide-react";

interface PlanItem {
  id: string;
  name: string;
  badge?: string;
  monthlyRate: number;
  description: string;
  features: string[];
  highlighted?: boolean;
}

const HEALTH_PLANS: PlanItem[] = [
  {
    id: "essential",
    name: "VALOR Essential Care",
    monthlyRate: 118,
    description: "Ideal for young professionals and healthy adults needing foundational protection and hospital security.",
    features: [
      "14,000+ cashless network hospitals nationwide",
      "Under 120-second emergency pre-authorizations",
      "Routine preventive wellness checkups & annual blood panels",
      "Basic AegisTwin biometric sync (wearables & labs)",
      "Generic pharmacy coverage with zero deductible",
    ],
  },
  {
    id: "aegis-complete",
    name: "AegisTwin Complete",
    badge: "MOST POPULAR",
    monthlyRate: 184,
    highlighted: true,
    description: "Our signature proactive health policy with continuous AI-monitored safety tripwires and zero inpatient copay.",
    features: [
      "Continuous FDA Black-Box drug clash & DDI interceptor",
      "Full inpatient hospitalization & private room coverage",
      "Live biomarker forecasting (eGFR, HbA1c, BP telemetry)",
      "Dedicated 24/7 Nurse Care Navigator (RN) assignment",
      "Specialty medications & brand-name biologic drug access",
      "Zero out-of-pocket discharge settlement guarantee",
    ],
  },
  {
    id: "senior-advantage",
    name: "Senior Medicare Shield",
    badge: "65+ SPECIALIZED",
    monthlyRate: 236,
    description: "Engineered specifically for seniors and individuals managing multi-morbidity and chronic polypharmacy.",
    features: [
      "AGS Beers Criteria safety audits for high-risk medications",
      "Personalized click-to-deprescribe geriatrician consultation",
      "In-home vitals monitoring kit & wearable fall-detection",
      "Comprehensive chronic disease management (CKD, AFib, HTN)",
      "Zero-dollar medical transit assistance for specialist visits",
      "Quarterly family care-circle health briefing reports",
    ],
  },
];

export default function HealthPlansMeadow() {
  const [selectedPlan, setSelectedPlan] = useState<string>("aegis-complete");

  return (
    <section className="meadow-container" id="plans" style={{ marginBottom: "60px" }}>
      <div
        style={{
          background: "#ffffff",
          borderRadius: "36px",
          padding: "50px 44px",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.04)",
          border: "1px solid var(--rose-border)",
        }}
      >
        <div style={{ textAlign: "center", maxWidth: "660px", margin: "0 auto 40px" }}>
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
            <span>✦</span> TRANSPARENT HEALTH COVERAGE
          </div>
          <h2
            style={{
              fontSize: "clamp(30px, 3.6vw, 44px)",
              fontWeight: 700,
              letterSpacing: "-0.03em",
              color: "var(--text-dark)",
              lineHeight: 1.15,
              margin: "0 0 12px",
            }}
          >
            Health plans tailored to every stage of life.
          </h2>
          <p style={{ fontSize: "16px", color: "var(--text-muted)", lineHeight: 1.6, margin: 0 }}>
            Choose continuous proactive health insurance powered by your digital twin. Guaranteed locked monthly rates
            with zero surprise bills or hidden deductibles.
          </p>
        </div>

        {/* 3 Plans Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(310px, 1fr))",
            gap: "24px",
          }}
        >
          {HEALTH_PLANS.map((plan) => {
            const isSelected = selectedPlan === plan.id;
            return (
              <div
                key={plan.id}
                onClick={() => setSelectedPlan(plan.id)}
                style={{
                  background: plan.highlighted ? "#fbf4f7" : "#ffffff",
                  border: plan.highlighted
                    ? "2px solid var(--rose-accent)"
                    : "1px solid rgba(210, 106, 148, 0.22)",
                  borderRadius: "28px",
                  padding: "36px 30px",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  position: "relative",
                  boxShadow: plan.highlighted
                    ? "0 12px 36px rgba(210, 106, 148, 0.14)"
                    : "0 4px 20px rgba(0, 0, 0, 0.02)",
                  transition: "all 0.2s ease",
                  cursor: "pointer",
                }}
              >
                {plan.badge && (
                  <div
                    style={{
                      position: "absolute",
                      top: "20px",
                      right: "24px",
                      fontSize: "10px",
                      fontWeight: 800,
                      letterSpacing: "0.08em",
                      textTransform: "uppercase",
                      background: plan.highlighted ? "var(--plum-dark)" : "#f4edf1",
                      color: plan.highlighted ? "#ffffff" : "var(--plum-dark)",
                      padding: "4px 12px",
                      borderRadius: "9999px",
                    }}
                  >
                    {plan.badge}
                  </div>
                )}

                <div>
                  <h3
                    style={{
                      fontSize: "22px",
                      fontWeight: 700,
                      color: "var(--text-dark)",
                      margin: "0 0 8px",
                    }}
                  >
                    {plan.name}
                  </h3>
                  <p
                    style={{
                      fontSize: "14px",
                      color: "#6b5f6a",
                      lineHeight: 1.5,
                      margin: "0 0 24px",
                      minHeight: "42px",
                    }}
                  >
                    {plan.description}
                  </p>

                  <div style={{ display: "flex", alignItems: "baseline", gap: "6px", marginBottom: "26px" }}>
                    <span
                      style={{
                        fontSize: "44px",
                        fontWeight: 800,
                        color: "var(--text-dark)",
                        letterSpacing: "-0.03em",
                      }}
                    >
                      ${plan.monthlyRate}
                    </span>
                    <span style={{ fontSize: "14px", color: "#8c7e8a", fontWeight: 500 }}>
                      / month
                    </span>
                  </div>

                  <div style={{ borderTop: "1px solid rgba(210, 106, 148, 0.15)", paddingTop: "20px", marginBottom: "28px" }}>
                    <div style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--rose-accent)", marginBottom: "14px" }}>
                      Plan Safeguards & Benefits:
                    </div>
                    <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "12px" }}>
                      {plan.features.map((feat, idx) => (
                        <li
                          key={idx}
                          style={{
                            display: "flex",
                            alignItems: "flex-start",
                            gap: "10px",
                            fontSize: "13.5px",
                            color: "#473b45",
                            lineHeight: 1.45,
                          }}
                        >
                          <div
                            style={{
                              width: "18px",
                              height: "18px",
                              borderRadius: "50%",
                              background: plan.highlighted ? "#fcebf2" : "#f4edf1",
                              display: "grid",
                              placeContent: "center",
                              flexShrink: 0,
                              marginTop: "1px",
                            }}
                          >
                            <Check size={12} color="var(--rose-accent)" strokeWidth={3} />
                          </div>
                          <span>{feat}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <button
                  className={plan.highlighted ? "btn-plum" : "btn-meadow"}
                  style={{
                    width: "100%",
                    padding: "14px",
                    borderRadius: "9999px",
                    fontSize: "14px",
                    fontWeight: 700,
                    cursor: "pointer",
                    textAlign: "center",
                    border: plan.highlighted ? "none" : "1.5px solid var(--plum-dark)",
                    background: plan.highlighted ? "var(--plum-dark)" : "transparent",
                    color: plan.highlighted ? "#ffffff" : "var(--plum-dark)",
                    transition: "all 0.2s ease",
                  }}
                >
                  Select {plan.name.split(" ")[1]} Plan
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
