"use client";

import Link from "next/link";
import { ShieldCheck, Activity, Zap, CheckCircle2 } from "lucide-react";

export default function WhatIsAegisTwin() {
  return (
    <section className="meadow-container what-is-section" id="what-is-twin">
      {/* Split Header */}
      <div className="what-is-header">
        <div>
          <h2 className="what-is-title">What is AegisTwin?</h2>
          <div style={{ marginTop: "18px" }}>
            <Link href="#simulator" className="btn-plum" style={{ padding: "8px 20px", fontSize: "13px" }}>
              Explore now
            </Link>
          </div>
        </div>

        <p className="what-is-desc">
          AegisTwin is a clinical digital twin platform that pairs your continuous biometric telemetry with health coverage,
          eliminating preventable emergencies and guaranteeing zero surprise hospital bills.
        </p>
      </div>

      {/* 3-Card Grid */}
      <div className="cards-grid">
        {/* Card 1: Wide Light Rose Card with Botanical Flower Graphic */}
        <div className="card-light">
          <div>
            <h3 className="card-title-lg" style={{ color: "var(--text-dark)" }}>
              Care that protects
            </h3>
            <p className="card-text-muted" style={{ maxWidth: "260px" }}>
              Predictive inpatient risk modeling automatically triggers early care management and preventative lab screening.
            </p>
          </div>

          {/* Botanical Floral Artwork in Card 1 */}
          <div style={{ position: "relative", height: "180px", marginTop: "16px", display: "flex", alignItems: "flex-end" }}>
            <svg viewBox="0 0 420 180" fill="none" style={{ width: "100%", height: "100%" }}>
              {/* Meadow cluster */}
              <ellipse cx="260" cy="180" rx="140" ry="50" fill="#b94e7c" />
              <ellipse cx="280" cy="175" rx="110" ry="40" fill="#f2a6c4" opacity="0.6" />
              
              {/* Flower Stem */}
              <path d="M 270 170 Q 268 110 270 65" stroke="#486940" strokeWidth="4" strokeLinecap="round" />
              <ellipse cx="258" cy="120" rx="12" ry="5" fill="#58804e" transform="rotate(-25 258 120)" />

              {/* Flower Blossom */}
              <g transform="translate(270, 65)">
                {/* Petals */}
                {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((deg) => (
                  <ellipse
                    key={deg}
                    cx="0"
                    cy="-22"
                    rx="5"
                    ry="20"
                    fill="#d26a94"
                    transform={`rotate(${deg})`}
                  />
                ))}
                {/* Cone center */}
                <circle cx="0" cy="0" r="14" fill="#a4581f" />
                <circle cx="0" cy="0" r="10" fill="#dc8a37" />
              </g>

              {/* Shield Token Coin nestled in meadow */}
              <g transform="translate(195, 95)">
                <ellipse cx="35" cy="45" rx="28" ry="40" fill="#8e3b5e" />
                <ellipse cx="32" cy="42" rx="26" ry="38" fill="#f2a6c4" />
                <circle cx="32" cy="42" r="12" fill="#fff" opacity="0.85" />
              </g>
            </svg>
          </div>
        </div>

        {/* Card 2: Always Cashless, Always Stable */}
        <div className="card-dark">
          <div>
            <h3 className="card-title-lg" style={{ color: "var(--white)" }}>
              Always cashless,<br />always stable
            </h3>
          </div>

          {/* Sparkline Graphic showing steady $0.00 out-of-pocket */}
          <div style={{ padding: "20px 0" }}>
            <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "6px" }}>
              <span style={{ fontSize: "11px", color: "#d69db3", fontFamily: "monospace", letterSpacing: "0.05em" }}>
                $0.00 COPAY
              </span>
            </div>
            <svg viewBox="0 0 240 40" fill="none" style={{ width: "100%", height: "40px" }}>
              <path
                d="M 10 20 Q 40 18 80 21 Q 120 19 160 21 Q 200 20 230 20"
                stroke="#f2a6c4"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
              <circle cx="230" cy="20" r="4" fill="#f2a6c4" />
              <circle cx="230" cy="20" r="8" fill="#f2a6c4" opacity="0.3" />
            </svg>
          </div>

          <p className="card-text-light">
            Pre-authorized cashless settlement across 14,000+ accredited network hospitals in under 120 seconds.
          </p>
        </div>

        {/* Card 3: 100% Automated Tripwires */}
        <div className="card-dark">
          <div>
            <h3 className="card-title-lg" style={{ color: "var(--white)" }}>
              100%<br />hands-free
            </h3>
          </div>

          {/* Toggle Switch and Radar Indicator Graphic */}
          <div style={{ padding: "10px 0" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", gap: "10px", marginBottom: "16px" }}>
              <span style={{ fontSize: "11px", color: "#d69db3", letterSpacing: "0.1em", fontWeight: 700 }}>
                AUTO · ON
              </span>
              <div
                style={{
                  width: "42px",
                  height: "24px",
                  background: "#d26a94",
                  borderRadius: "999px",
                  position: "relative",
                  padding: "3px",
                }}
              >
                <div
                  style={{
                    width: "18px",
                    height: "18px",
                    background: "#fff",
                    borderRadius: "50%",
                    marginLeft: "auto",
                  }}
                />
              </div>
            </div>

            {/* Radar circle */}
            <div style={{ display: "flex", justifyContent: "center" }}>
              <svg viewBox="0 0 60 60" style={{ width: "50px", height: "50px" }}>
                <circle cx="30" cy="30" r="24" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="1.5" />
                <circle cx="30" cy="30" r="16" fill="none" stroke="rgba(255,255,255,0.25)" strokeDasharray="3 3" />
                <circle cx="30" cy="30" r="4" fill="#f2a6c4" />
                <circle cx="44" cy="20" r="3" fill="#f2a6c4" />
              </svg>
            </div>
          </div>

          <p className="card-text-light">
            Continuous FDA contraindication screening and automated Beers Criteria anticholinergic tripwire alerts.
          </p>
        </div>
      </div>

      {/* Network Accredited Ticker */}
      <div className="ticker-row">
        <span>Accredited clinical network & hospital partners:</span>
        <div className="ticker-item"><CheckCircle2 size={15} color="#d26a94" /> Mayo Clinical Network</div>
        <div className="ticker-item"><CheckCircle2 size={15} color="#d26a94" /> Johns Hopkins Medicine</div>
        <div className="ticker-item"><CheckCircle2 size={15} color="#d26a94" /> Cleveland Clinic</div>
        <div className="ticker-item"><CheckCircle2 size={15} color="#d26a94" /> Mount Sinai Health</div>
        <div className="ticker-item"><CheckCircle2 size={15} color="#d26a94" /> Mass General Brigham</div>
      </div>
    </section>
  );
}
