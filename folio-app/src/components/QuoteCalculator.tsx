"use client";

import { useState } from "react";
import Link from "next/link";
import { Sparkles, ShieldCheck, ArrowRight } from "lucide-react";

export default function QuoteCalculator() {
  const [policyType, setPolicyType] = useState<"bundle" | "health" | "home" | "auto">("bundle");
  const [ageTier, setAgeTier] = useState<"young" | "mid" | "senior">("mid");
  const [deductible, setDeductible] = useState<number>(1000);
  const [hasTelemetry, setHasTelemetry] = useState<boolean>(true);
  const [hasPharmacy, setHasPharmacy] = useState<boolean>(true);

  // Compute calculated pricing
  let basePrice = 0;
  if (policyType === "bundle") basePrice = 210;
  else if (policyType === "health") basePrice = 135;
  else if (policyType === "home") basePrice = 75;
  else if (policyType === "auto") basePrice = 90;

  let ageMult = 1.0;
  if (ageTier === "young") ageMult = 0.85;
  else if (ageTier === "senior") ageMult = 1.35;

  let dedDiscount = 0;
  if (deductible === 1000) dedDiscount = 15;
  else if (deductible === 2500) dedDiscount = 32;

  const telemetryDisc = hasTelemetry ? 22 : 0;
  const pharmacyCost = hasPharmacy ? 18 : 0;

  const monthlyTotal = Math.max(
    35,
    Math.round(basePrice * ageMult - dedDiscount - telemetryDisc + pharmacyCost)
  );

  return (
    <section className="page" id="quotes">
      <div className="section-label">Transparent Actuarial Pricing</div>
      <h2>Quotes that respect your time.</h2>
      <p className="lead">
        No opaque quotes or aggressive telemarketing calls. Adjust your coverage scope, deductibles, and preventative
        health telemetry below for an instant locked rate.
      </p>

      <div className="quote-paper-layout">
        {/* Left: Controls */}
        <div>
          {/* Policy Segmented */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", font: "700 13px 'Bricolage Grotesque', sans-serif" }}>
              <span>Select Coverage Folders</span>
              <span style={{ color: "var(--oak)" }}>15% Bundle Savings</span>
            </div>
            <div style={{ display: "flex", gap: "8px", background: "var(--paper-warm)", padding: "4px", borderRadius: "8px" }}>
              {[
                { id: "bundle", label: "All 4 (Bundle)" },
                { id: "health", label: "Health" },
                { id: "home", label: "Home" },
                { id: "auto", label: "Auto" },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => setPolicyType(item.id as any)}
                  style={{
                    flex: 1,
                    padding: "8px 12px",
                    borderRadius: "6px",
                    font: "600 14px 'Bricolage Grotesque', sans-serif",
                    background: policyType === item.id ? "var(--white)" : "transparent",
                    color: "var(--ink)",
                    boxShadow: policyType === item.id ? "0 1px 4px rgba(0,0,0,0.06)" : "none",
                  }}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Age Bracket */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ marginBottom: "8px", font: "700 13px 'Bricolage Grotesque', sans-serif" }}>
              Insured Age Cohort
            </div>
            <div style={{ display: "flex", gap: "8px", background: "var(--paper-warm)", padding: "4px", borderRadius: "8px" }}>
              {[
                { id: "young", label: "18 – 35 yrs" },
                { id: "mid", label: "36 – 55 yrs" },
                { id: "senior", label: "56+ (Senior)" },
              ].map((tier) => (
                <button
                  key={tier.id}
                  onClick={() => setAgeTier(tier.id as any)}
                  style={{
                    flex: 1,
                    padding: "8px 12px",
                    borderRadius: "6px",
                    font: "600 14px 'Bricolage Grotesque', sans-serif",
                    background: ageTier === tier.id ? "var(--white)" : "transparent",
                    color: "var(--ink)",
                    boxShadow: ageTier === tier.id ? "0 1px 4px rgba(0,0,0,0.06)" : "none",
                  }}
                >
                  {tier.label}
                </button>
              ))}
            </div>
          </div>

          {/* Deductible Slider */}
          <div style={{ marginBottom: "28px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", font: "700 13px 'Bricolage Grotesque', sans-serif" }}>
              <span>Annual Deductible</span>
              <span>${deductible.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="500"
              max="2500"
              step="500"
              value={deductible}
              onChange={(e) => setDeductible(Number(e.target.value))}
              style={{ width: "100%", accentColor: "var(--oak)" }}
            />
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "#6b7280", marginTop: "6px" }}>
              <span>$500 (Low out-of-pocket)</span>
              <span>$1,000 (Standard)</span>
              <span>$2,500 (Max discount)</span>
            </div>
          </div>

          {/* Checkboxes */}
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <label
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "12px 16px",
                background: "var(--white)",
                border: "1px solid var(--line)",
                borderRadius: "8px",
                cursor: "pointer",
              }}
            >
              <span style={{ fontSize: "15px" }}>AegisTwin Connected Wearable Telemetry Discount (-$22/mo)</span>
              <input
                type="checkbox"
                checked={hasTelemetry}
                onChange={(e) => setHasTelemetry(e.target.checked)}
                style={{ width: "18px", height: "18px", accentColor: "var(--oak)" }}
              />
            </label>

            <label
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "12px 16px",
                background: "var(--white)",
                border: "1px solid var(--line)",
                borderRadius: "8px",
                cursor: "pointer",
              }}
            >
              <span style={{ fontSize: "15px" }}>Cashless Pharmacy Pre-Clearance Rider (+$18/mo)</span>
              <input
                type="checkbox"
                checked={hasPharmacy}
                onChange={(e) => setHasPharmacy(e.target.checked)}
                style={{ width: "18px", height: "18px", accentColor: "var(--oak)" }}
              />
            </label>
          </div>
        </div>

        {/* Right: Summary Box */}
        <div className="quote-sidebar-box">
          <div>
            <h4>Estimated Premium</h4>
            <div className="quote-big-price">
              ${monthlyTotal}
              <span> / month</span>
            </div>
            <p style={{ fontSize: "15px", color: "var(--mist)", lineHeight: 1.5, margin: 0 }}>
              Rate guaranteed for 12 calendar months with zero hidden administrative fees.
            </p>

            <div
              style={{
                marginTop: "24px",
                paddingTop: "18px",
                borderTop: "1px solid rgba(255,255,255,0.12)",
                fontSize: "14px",
                display: "flex",
                flexDirection: "column",
                gap: "8px",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--mist)" }}>Deductible Tier</span>
                <span>${deductible}</span>
              </div>
              {hasTelemetry && (
                <div style={{ display: "flex", justifyContent: "space-between", color: "#38bdf8" }}>
                  <span>Digital Twin Biometric Credit</span>
                  <span>-$22 / mo</span>
                </div>
              )}
              {policyType === "bundle" && (
                <div style={{ display: "flex", justifyContent: "space-between", color: "#4ade80" }}>
                  <span>Multi-Policy Bundle Discount</span>
                  <span>15% Off</span>
                </div>
              )}
            </div>
          </div>

          <div style={{ marginTop: "28px" }}>
            <Link
              href="#twin"
              className="btn"
              style={{
                display: "block",
                textAlign: "center",
                background: "var(--oak)",
                color: "var(--ink)",
                margin: 0,
              }}
            >
              Review Twin & Bind Policy
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
