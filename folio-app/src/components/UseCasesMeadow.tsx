"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

interface UseCaseData {
  id: string;
  num: string;
  title: string;
  desc: string;
  details: string;
}

const USE_CASES: UseCaseData[] = [
  {
    id: "inpatient",
    num: "01",
    title: "Hospitalization",
    desc: "Direct cashless hospital clearance pre-approved in under 120 seconds. Continuous telemetry ensures ICUs, day-care surgeries, and emergency admissions are validated without out-of-pocket bills.",
    details: "Zero deductible friction with 14,000+ accredited network providers.",
  },
  {
    id: "chronic",
    num: "02",
    title: "Metabolic Care",
    desc: "Built specifically for individuals managing Type 2 Diabetes, Hypertension, and CKD. Continuous eGFR & HbA1c lab telemetry prevents renal toxicity and automated DDI/DCI drug clashes.",
    details: "Automated quarterly lab panels and zero-copay prescription pre-clearance.",
  },
  {
    id: "medicare",
    num: "03",
    title: "Senior Medicare",
    desc: "Geriatric safety safeguards designed around AGS Beers Criteria guidelines. Automatically flags high-risk anticholinergic sedative combinations and deploys in-home fall risk assessments.",
    details: "Continuous wearable fall-detection pendant sync and proactive taper support.",
  },
];

export default function UseCasesMeadow() {
  const [activeTab, setActiveTab] = useState(0);
  const current = USE_CASES[activeTab];

  return (
    <section className="meadow-container use-cases-section" id="use-cases">
      <div className="use-cases-grid">
        {/* Left: Headline & Vertical Selector */}
        <div className="use-cases-left">
          <h3>AegisTwin in Action</h3>
          <h2>Use cases</h2>
          <p>
            AegisTwin coordinates individualized clinical coverage across acute hospital stays, metabolic conditions, and senior care.
          </p>

          <div className="tabs-list">
            {USE_CASES.map((uc, idx) => {
              const isActive = activeTab === idx;
              return (
                <button
                  key={uc.id}
                  className={`tab-item ${isActive ? "active" : ""}`}
                  onClick={() => setActiveTab(idx)}
                >
                  <div className="tab-item-title">
                    <span className="tab-num">{uc.num}</span>
                    <span className="tab-name">{uc.title}</span>
                  </div>
                  <span className="tab-arrow">→</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right: Dynamic White Curved Card with Neoclassical Architecture Artwork */}
        <div className="use-cases-card">
          <div>
            <h3 className="use-cases-card-title">{current.title}</h3>
            <p className="use-cases-card-desc">{current.desc}</p>
            <Link
              href="#simulator"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                fontSize: "14px",
                fontWeight: 600,
                color: "var(--text-dark)",
                textDecoration: "none",
              }}
            >
              <div
                style={{
                  width: "28px",
                  height: "28px",
                  borderRadius: "50%",
                  background: "#f7ebf1",
                  display: "grid",
                  placeContent: "center",
                }}
              >
                <ArrowRight size={14} color="#241622" />
              </div>
              <span>Learn more</span>
            </Link>
          </div>

          {/* Neoclassical Hospital Temple Illustration on Rose Meadow (Matching Template) */}
          <div style={{ width: "100%", height: "200px", marginTop: "20px" }}>
            <svg viewBox="0 0 500 200" fill="none" style={{ width: "100%", height: "100%" }}>
              <defs>
                <linearGradient id="pedimentGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#fdf3f6" />
                  <stop offset="100%" stopColor="#f2cad8" />
                </linearGradient>
                <linearGradient id="columnGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#fdf5f7" />
                  <stop offset="50%" stopColor="#eed0dc" />
                  <stop offset="100%" stopColor="#e3afc2" />
                </linearGradient>
              </defs>

              {/* Rose Meadow at base */}
              <ellipse cx="250" cy="195" rx="220" ry="25" fill="#8e3b5e" />
              <ellipse cx="250" cy="190" rx="190" ry="20" fill="#b94e7c" />

              {/* Temple Base steps */}
              <rect x="140" y="150" width="220" height="12" rx="2" fill="url(#pedimentGrad)" />
              <rect x="150" y="140" width="200" height="10" rx="2" fill="url(#pedimentGrad)" />
              <rect x="160" y="132" width="180" height="8" rx="2" fill="url(#pedimentGrad)" />

              {/* 4 Classical Columns */}
              {[180, 220, 260, 300].map((x) => (
                <g key={x}>
                  {/* Capital */}
                  <rect x={x - 6} y="80" width="20" height="6" rx="2" fill="#eed0dc" />
                  {/* Shaft */}
                  <rect x={x - 4} y="86" width="16" height="46" rx="1" fill="url(#columnGrad)" />
                  {/* Base */}
                  <rect x={x - 6} y="128" width="20" height="4" rx="1" fill="#eed0dc" />
                </g>
              ))}

              {/* Architrave / Entablature */}
              <rect x="160" y="72" width="180" height="8" rx="2" fill="url(#pedimentGrad)" />

              {/* Triangular Pediment / Roof */}
              <polygon points="250,30 150,72 350,72" fill="url(#pedimentGrad)" />
              <polygon points="250,38 165,70 335,70" fill="#fdf7f9" opacity="0.7" />

              {/* Meadow Blossom Dots along base */}
              <g fill="#fdeaf1">
                {[
                  [120, 190, 4], [150, 185, 5], [190, 180, 4], [230, 188, 5],
                  [270, 182, 4], [310, 186, 5], [350, 182, 4], [380, 188, 5]
                ].map(([cx, cy, r], i) => (
                  <circle key={i} cx={cx} cy={cy} r={r} />
                ))}
              </g>
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
}
