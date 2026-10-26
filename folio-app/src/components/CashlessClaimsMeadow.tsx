"use client";

import { useState } from "react";
import { UploadCloud, CheckCircle2, ShieldCheck, Clock } from "lucide-react";

export default function CashlessClaimsMeadow() {
  const [claimUploaded, setClaimUploaded] = useState(false);

  return (
    <section className="meadow-container" id="claims" style={{ marginBottom: "60px" }}>
      <div
        style={{
          background: "var(--white)",
          borderRadius: "36px",
          padding: "50px 44px",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.04)",
          display: "grid",
          gridTemplateColumns: "1.15fr 1fr",
          gap: "50px",
          alignItems: "center",
        }}
      >
        {/* Left Side Info */}
        <div>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.1em",
              color: "var(--rose-accent)",
              marginBottom: "10px",
            }}
          >
            Frictionless Direct Settlement
          </div>
          <h2
            style={{
              fontSize: "clamp(32px, 3.8vw, 46px)",
              fontWeight: 700,
              letterSpacing: "-0.03em",
              lineHeight: 1.15,
              marginBottom: "16px",
              color: "var(--text-dark)",
            }}
          >
            Zero Out-of-Pocket Hospital Clearance
          </h2>
          <p style={{ fontSize: "16px", color: "#554953", lineHeight: 1.6, margin: "0 0 24px" }}>
            Because your Digital Twin continuously validates active diagnosis codes, recent eGFR & HbA1c labs, and
            prescribed medications, admissions and discharges are pre-approved in under 120 seconds across 14,000+ accredited network hospitals.
          </p>

          <div style={{ display: "flex", gap: "24px", flexWrap: "wrap" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "14px", fontWeight: 600, color: "#362233" }}>
              <Clock size={16} color="var(--rose-accent)" />
              <span>Under 120s Pre-Approval</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "14px", fontWeight: 600, color: "#362233" }}>
              <ShieldCheck size={16} color="var(--rose-accent)" />
              <span>100% Cashless Network</span>
            </div>
          </div>
        </div>

        {/* Right Side Upload Simulator */}
        <div
          style={{
            background: "#f7ebf1",
            border: "2px dashed rgba(210, 106, 148, 0.35)",
            borderRadius: "24px",
            padding: "36px 28px",
            textAlign: "center",
          }}
        >
          {!claimUploaded ? (
            <>
              <div
                style={{
                  width: "56px",
                  height: "56px",
                  borderRadius: "50%",
                  background: "#fff",
                  display: "grid",
                  placeContent: "center",
                  margin: "0 auto 16px",
                  boxShadow: "0 4px 14px rgba(210, 106, 148, 0.15)",
                }}
              >
                <UploadCloud size={28} color="#241622" />
              </div>
              <h3 style={{ fontSize: "19px", fontWeight: 700, color: "var(--text-dark)", marginBottom: "6px" }}>
                File a new cashless claim
              </h3>
              <p style={{ color: "#6b5f6a", fontSize: "14px", margin: "0 0 20px", lineHeight: 1.5 }}>
                Upload hospital discharge summaries, emergency admittance slips, or pharmacy receipts.
              </p>
              <button
                onClick={() => setClaimUploaded(true)}
                className="btn-plum"
                style={{ padding: "12px 28px", fontSize: "14px" }}
              >
                Simulate Cashless Discharge Filing
              </button>
            </>
          ) : (
            <div>
              <div
                style={{
                  width: "56px",
                  height: "56px",
                  borderRadius: "50%",
                  background: "#edfcf2",
                  display: "grid",
                  placeContent: "center",
                  margin: "0 auto 16px",
                }}
              >
                <CheckCircle2 size={32} color="#16a34a" />
              </div>
              <div style={{ font: "700 19px sans-serif", color: "#15803d", marginBottom: "6px" }}>
                Claim #CLM-8491 Approved
              </div>
              <p style={{ color: "#4b5563", fontSize: "14px", margin: "0 0 18px", lineHeight: 1.5 }}>
                <strong>$1,450.00</strong> cashless discharge pre-cleared. Funds settled directly with provider with zero out-of-pocket patient copay.
              </p>
              <button
                onClick={() => setClaimUploaded(false)}
                style={{
                  fontSize: "13px",
                  fontWeight: 600,
                  color: "var(--rose-accent)",
                  background: "none",
                  border: "none",
                  textDecoration: "underline",
                  cursor: "pointer",
                }}
              >
                Reset Demo
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
