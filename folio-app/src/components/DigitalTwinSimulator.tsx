"use client";

import { useState, useMemo } from "react";
import { CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";

export default function DigitalTwinSimulator() {
  const [sliderVal, setSliderVal] = useState<number>(68); // 15 to 90 eGFR / intervention intensity
  const [timeHorizon, setTimeHorizon] = useState<string>("1Y");
  const [autoPreauth, setAutoPreauth] = useState<boolean>(true);

  // Calculate live health statistics and actuarial savings
  const metrics = useMemo(() => {
    // Risk formula: as sliderVal increases (healthy biomarker/deprescribing), risk drops
    const baseRisk = Math.max(0.08, Math.min(0.92, (95 - sliderVal) / 80));
    const timeMultiplier = timeHorizon === "30D" ? 0.3 : timeHorizon === "90D" ? 0.5 : timeHorizon === "1Y" ? 1.0 : 1.8;
    const savings = Math.round((sliderVal / 90) * 16800 * timeMultiplier);
    const riskPercentage = (baseRisk * 100).toFixed(1);

    return {
      risk: baseRisk,
      riskPercentage,
      savings: savings.toLocaleString(),
      isContraindicated: sliderVal < 30,
    };
  }, [sliderVal, timeHorizon]);

  return (
    <section className="meadow-container" id="simulator">
      <div className="simulator-card">
        <div className="sim-grid">
          {/* Left Column: Sliders, Controls, and Metrics */}
          <div>
            <div className="sim-badge">AegisTwin Clinical Simulator</div>
            <h2 className="sim-title">Let care blossom</h2>
            <p className="sim-desc">
              Drag to see how continuous biomarker tracking and prescription deprescribing shrink acute inpatient risk and compound actuarial savings.
            </p>

            {/* Slider Header */}
            <div className="sim-metric-row">
              <span className="sim-metric-label">Kidney Function (eGFR Telemetry):</span>
              <span className="sim-metric-value">
                {sliderVal} <span style={{ fontSize: "18px", fontWeight: 500, color: "#d69db3" }}>mL/min</span>
              </span>
            </div>

            {/* Slider */}
            <input
              type="range"
              min="15"
              max="90"
              step="1"
              value={sliderVal}
              onChange={(e) => setSliderVal(Number(e.target.value))}
              className="sim-slider"
            />

            <div className="sim-slider-stops">
              <span>15 (Renal Crisis)</span>
              <span>30 (FDA Threshold)</span>
              <span>90+ (Healthy)</span>
            </div>

            {/* Contraindication Alert if < 30 */}
            {metrics.isContraindicated && (
              <div
                style={{
                  background: "rgba(224, 86, 60, 0.15)",
                  border: "1px solid #e0563c",
                  borderRadius: "12px",
                  padding: "12px 16px",
                  marginBottom: "20px",
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  fontSize: "13px",
                  color: "#ffd4cc",
                }}
              >
                <AlertTriangle size={18} color="#e0563c" />
                <span>
                  <strong>FDA Tripwire:</strong> eGFR &lt; 30 mL/min triggers Metformin lactic acidosis contraindication. Deprescribe recommended.
                </span>
              </div>
            )}

            {/* Time Horizon Pills & Auto-preauth Toggle */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px", marginBottom: "32px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <span style={{ fontSize: "13px", color: "rgba(255,255,255,0.7)" }}>Time in meadow:</span>
                <div className="sim-time-pills">
                  {["30D", "90D", "1Y", "3Y"].map((t) => (
                    <button
                      key={t}
                      className={`sim-pill ${timeHorizon === t ? "active" : ""}`}
                      onClick={() => setTimeHorizon(t)}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>

              {/* Toggle */}
              <div
                style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}
                onClick={() => setAutoPreauth(!autoPreauth)}
              >
                <div
                  style={{
                    width: "36px",
                    height: "20px",
                    background: autoPreauth ? "#d26a94" : "#554350",
                    borderRadius: "999px",
                    padding: "2px",
                    transition: "background 0.2s ease",
                  }}
                >
                  <div
                    style={{
                      width: "16px",
                      height: "16px",
                      background: "#fff",
                      borderRadius: "50%",
                      marginLeft: autoPreauth ? "16px" : "0",
                      transition: "margin 0.2s ease",
                    }}
                  />
                </div>
                <span style={{ fontSize: "13px", color: "rgba(255,255,255,0.8)" }}>Auto-preauth</span>
              </div>
            </div>

            {/* 2 Stat Boxes */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div className="sim-stat-box">
                <div className="sim-stat-title">Predicted 90d Inpatient Risk</div>
                <div className="sim-stat-number" style={{ color: metrics.risk > 0.5 ? "#f87171" : "#86efac" }}>
                  {metrics.riskPercentage}%
                </div>
              </div>

              <div className="sim-stat-box">
                <div className="sim-stat-title">Avoidable Hospital Spend Saved</div>
                <div className="sim-stat-number" style={{ color: "#f2a6c4" }}>
                  +${metrics.savings}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Comparative Trajectory Graph */}
          <div className="sim-graph-box">
            {/* Legend */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "12px", color: "rgba(255,255,255,0.7)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "16px", height: "3px", background: "#f2a6c4", borderRadius: "2px" }} />
                <span>AegisTwin Proactive Care</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ width: "16px", height: "2px", borderTop: "2px dashed rgba(255,255,255,0.4)" }} />
                <span>Standard Reactive Cover</span>
              </div>
            </div>

            {/* Dynamic Graph Curves */}
            <div style={{ height: "240px", margin: "20px 0", position: "relative" }}>
              <svg viewBox="0 0 360 220" fill="none" style={{ width: "100%", height: "100%" }}>
                {/* Horizontal reference grid lines */}
                <line x1="10" y1="30" x2="350" y2="30" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />
                <line x1="10" y1="90" x2="350" y2="90" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />
                <line x1="10" y1="150" x2="350" y2="150" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />

                {/* Shaded Area under AegisTwin Curve */}
                <path
                  d={`M 10 180 Q 180 ${180 - (sliderVal / 90) * 110} 350 ${190 - (sliderVal / 90) * 160} L 350 210 L 10 210 Z`}
                  fill="rgba(242, 166, 196, 0.12)"
                />

                {/* Standard Reactive claims (dotted line) */}
                <line
                  x1="10"
                  y1="180"
                  x2="350"
                  y2="165"
                  stroke="rgba(255,255,255,0.4)"
                  strokeWidth="2"
                  strokeDasharray="4 4"
                />

                {/* AegisTwin Trajectory (Solid glowing pink line) */}
                <path
                  d={`M 10 180 Q 180 ${180 - (sliderVal / 90) * 110} 350 ${190 - (sliderVal / 90) * 160}`}
                  stroke="#f2a6c4"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                />

                {/* Endpoint circle */}
                <circle cx="350" cy={190 - (sliderVal / 90) * 160} r="5" fill="#f2a6c4" />
                <circle cx="350" cy={190 - (sliderVal / 90) * 160} r="10" fill="#f2a6c4" opacity="0.3" />
              </svg>
            </div>

            {/* Graph X-Axis Labels */}
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "rgba(255,255,255,0.4)" }}>
              <span>Day 0 (Baseline)</span>
              <span>Quarter 2 (Telemetry)</span>
              <span>{timeHorizon} (Continuous Protection)</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
