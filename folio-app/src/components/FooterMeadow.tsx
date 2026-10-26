"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";

export default function FooterMeadow() {
  return (
    <footer className="meadow-footer">
      <div className="meadow-container">
        {/* Top Navigation Grid */}
        <div className="footer-top">
          {/* Brand Info */}
          <div className="footer-brand">
            <Link href="#top" className="brand-logo" style={{ textDecoration: "none" }}>
              <Sparkles size={18} className="brand-star" />
              <span>VALOR Health</span>
            </Link>
            <p>
              A predictive health plan paired with an intelligent clinical digital twin. Continuous protection, cashless hospital clearance.
            </p>

            {/* Social icons pills */}
            <div style={{ display: "flex", gap: "10px" }}>
              {["𝕏", "Discord", "Telegram", "GitHub"].map((s) => (
                <span
                  key={s}
                  style={{
                    display: "inline-grid",
                    placeContent: "center",
                    padding: "6px 12px",
                    borderRadius: "999px",
                    background: "rgba(36, 22, 34, 0.05)",
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "var(--text-dark)",
                    cursor: "pointer",
                  }}
                >
                  {s}
                </span>
              ))}
            </div>
          </div>

          {/* Column 1 */}
          <div className="footer-col">
            <h4>Continuous Care</h4>
            <ul>
              <li><Link href="#what-is-twin">How it works</Link></li>
              <li><Link href="#use-cases">Inpatient Hospitalization</Link></li>
              <li><Link href="#use-cases">Metabolic Care</Link></li>
              <li><Link href="#use-cases">Senior Medicare</Link></li>
              <li><Link href="#simulator">Risk Calculator</Link></li>
            </ul>
          </div>

          {/* Column 2 */}
          <div className="footer-col">
            <h4>Clinical Twin</h4>
            <ul>
              <li><Link href="#simulator">Biomarker Tuning</Link></li>
              <li><Link href="#what-is-twin">Tripwire Interceptor</Link></li>
              <li><Link href="#what-is-twin">FDA Black-Box Safety</Link></li>
              <li><Link href="#faq">Clinician Overrides</Link></li>
              <li><Link href="#faq">Audit Log Signatures</Link></li>
            </ul>
          </div>

          {/* Column 3 */}
          <div className="footer-col">
            <h4>Network & Support</h4>
            <ul>
              <li><Link href="#what-is-twin">14,000+ Hospitals</Link></li>
              <li><Link href="#faq">Cashless Approvals</Link></li>
              <li><Link href="#faq">Documentation</Link></li>
              <li><Link href="#faq">Contact Care Team</Link></li>
            </ul>
          </div>
        </div>

        {/* Large Decorative Watermark (Matching Template) */}
        <div className="footer-watermark">
          VALOR HEALTH
        </div>

        {/* Bottom Bar */}
        <div className="footer-bottom">
          <div>© 2026 VALOR Health & AegisTwin. All rights reserved.</div>
          <div style={{ display: "flex", gap: "24px" }}>
            <Link href="#top" style={{ color: "inherit", textDecoration: "none" }}>Privacy Policy</Link>
            <Link href="#top" style={{ color: "inherit", textDecoration: "none" }}>Terms of Service</Link>
            <Link href="#top" style={{ color: "inherit", textDecoration: "none" }}>Regulatory Disclosures</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
