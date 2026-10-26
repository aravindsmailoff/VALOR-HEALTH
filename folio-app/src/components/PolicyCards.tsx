"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, X } from "lucide-react";

interface PolicyItem {
  id: string;
  title: string;
  desc: string;
  rate: number;
  perks: string[];
}

const POLICIES: PolicyItem[] = [
  {
    id: "health",
    title: "Health",
    desc: "Hospital stays, day care, prescriptions, and routine check-ups with cashless network hospitals nearby.",
    rate: 124,
    perks: [
      "Point-of-care adverse drug tripwire interceptor",
      "Cashless pre-authorizations under 120 seconds",
      "Continuous digital twin biometric tracking",
    ],
  },
  {
    id: "home",
    title: "Home",
    desc: "Structure and contents, covered against fire, burst pipes, flood, and theft with guaranteed replacement value.",
    rate: 68,
    perks: [
      "Inflation-adjusted full reconstruction guarantee",
      "Temporary accommodation living expenses",
      "Smart moisture and leak sensor deductible waivers",
    ],
  },
  {
    id: "auto",
    title: "Auto",
    desc: "Own damage, comprehensive collision, and third-party liability, renewed in a few taps with instant smartphone claims.",
    rate: 82,
    perks: [
      "Zero deductible on glass and windshield repair",
      "OEM manufacturer replacement parts guarantee",
      "Immediate roadside assistance and towing credit",
    ],
  },
  {
    id: "life",
    title: "Life",
    desc: "A fixed payout providing long-term financial security and debt relief for the people who depend on you.",
    rate: 45,
    perks: [
      "Accelerated benefit for critical or terminal illness",
      "Level term premium locked in for up to 30 years",
      "Zero medical exam required for eligible applicants",
    ],
  },
];

export default function PolicyCards() {
  const [activeItem, setActiveItem] = useState<PolicyItem | null>(null);

  return (
    <section className="page" id="cover">
      <h2>Cover that fits on a single page.</h2>
      <div className="cov">
        {POLICIES.map((p) => (
          <div key={p.id}>
            <div>
              <h3>{p.title}</h3>
              <p>{p.desc}</p>
            </div>
            <div>
              <div className="price-tag">
                ${p.rate}
                <span> / month</span>
              </div>
              <button
                onClick={() => setActiveItem(p)}
                style={{
                  marginTop: "12px",
                  fontSize: "14px",
                  fontWeight: 600,
                  color: "var(--oak)",
                  textDecoration: "underline",
                }}
              >
                View policy schedule
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal Dialog */}
      {activeItem && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(22, 32, 43, 0.65)",
            backdropFilter: "blur(6px)",
            zIndex: 100,
            display: "grid",
            placeItems: "center",
            padding: "20px",
          }}
          onClick={() => setActiveItem(null)}
        >
          <div
            style={{
              background: "var(--white)",
              borderRadius: "16px",
              maxWidth: "520px",
              width: "100%",
              padding: "36px",
              boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
              position: "relative",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setActiveItem(null)}
              style={{
                position: "absolute",
                top: "20px",
                right: "20px",
                color: "#6b7280",
              }}
            >
              <X size={20} />
            </button>

            <h3 style={{ margin: "0 0 10px", fontSize: "28px" }}>{activeItem.title} Insurance</h3>
            <p style={{ color: "#4b5563", fontSize: "16px", marginBottom: "20px" }}>{activeItem.desc}</p>

            <div style={{ marginBottom: "24px" }}>
              <div style={{ font: "700 13px 'Bricolage Grotesque', sans-serif", color: "#6b7280", textTransform: "uppercase", marginBottom: "8px" }}>
                Included Cover Highlights:
              </div>
              <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "8px" }}>
                {activeItem.perks.map((perk, idx) => (
                  <li key={idx} style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "15px" }}>
                    <Check size={16} color="var(--forest)" />
                    <span>{perk}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div style={{ display: "flex", gap: "12px" }}>
              <Link
                href="#quotes"
                onClick={() => setActiveItem(null)}
                className="btn"
                style={{ flex: 1, textAlign: "center", margin: 0 }}
              >
                Customize Quote
              </Link>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
