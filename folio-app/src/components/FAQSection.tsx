"use client";

import { useState } from "react";
import { Plus, Minus } from "lucide-react";

interface FAQItem {
  q: string;
  a: string;
}

const FAQS: FAQItem[] = [
  {
    q: "How does the Digital Twin predict acute hospitalization risk?",
    a: "Our machine learning engine continuously analyzes non-invasive wearable telemetry, recent eGFR and HbA1c lab panels, and active diagnosis codes using split-conformal prediction intervals. It identifies adverse biomarker trajectories up to 90 days before an emergency arises.",
  },
  {
    q: "How does cashless hospital discharge work in under 120 seconds?",
    a: "Because your Digital Twin continuously validates active diagnosis codes and prescribed medications with our platform, pre-authorization is already confirmed when you arrive at any of our 14,000+ accredited network hospitals.",
  },
  {
    q: "What happens when an adverse drug tripwire (DDI or DCI) triggers?",
    a: "The system intercepts conflicting medications (such as Metformin with eGFR < 30 mL/min or Warfarin with NSAIDs) at the point of care. A dedicated RN care manager and your prescribing physician receive an immediate notification with evidence-backed deprescribing alternatives.",
  },
  {
    q: "Can my physician override clinical digital twin recommendations?",
    a: "Yes. Clinicians maintain complete autonomous authority. Physicians can formalize overrides directly through our care team portal, which signs the documented clinical justification into the audit log.",
  },
  {
    q: "Which hospitals and pharmacy networks are covered?",
    a: "VALOR Health covers 100% cashless pre-authorization across over 14,000 accredited hospitals nationwide, including leading medical centers such as Mayo Clinic, Johns Hopkins, Cleveland Clinic, Mount Sinai, and Mass General.",
  },
];

export default function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggle = (idx: number) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <section className="meadow-container faq-section" id="faq">
      <div className="faq-grid">
        {/* Left Column: Heading */}
        <div>
          <div className="faq-badge">FAQ</div>
          <h2 className="faq-title">Questions,<br />answered</h2>
          <p className="faq-sub">
            Everything you need to know before securing continuous protection. Still curious? We are one message away.
          </p>
        </div>

        {/* Right Column: Interactive Accordion */}
        <div className="faq-list">
          {FAQS.map((item, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div key={idx} className="faq-item">
                <button
                  className="faq-question"
                  onClick={() => toggle(idx)}
                  aria-expanded={isOpen}
                >
                  <span>{item.q}</span>
                  <div className="faq-icon">
                    {isOpen ? <Minus size={15} /> : <Plus size={15} />}
                  </div>
                </button>
                {isOpen && (
                  <div className="faq-answer">
                    <p>{item.a}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
