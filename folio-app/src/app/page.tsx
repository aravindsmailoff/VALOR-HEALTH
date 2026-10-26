"use client";

import Navbar from "@/components/Navbar";
import HeroScrollStage from "@/components/HeroScrollStage";
import WhatIsAegisTwin from "@/components/WhatIsAegisTwin";
import UseCasesMeadow from "@/components/UseCasesMeadow";
import IntegratedDigitalTwin from "@/components/IntegratedDigitalTwin";
import DigitalTwinSimulator from "@/components/DigitalTwinSimulator";
import HealthPlansMeadow from "@/components/HealthPlansMeadow";
import CashlessClaimsMeadow from "@/components/CashlessClaimsMeadow";
import FAQSection from "@/components/FAQSection";
import FooterMeadow from "@/components/FooterMeadow";

export default function Home() {
  return (
    <main style={{ minHeight: "100vh", backgroundColor: "var(--bg-main)" }}>
      {/* 1. Sticky Navigation */}
      <Navbar />

      {/* 2. Scroll-Driven Hero Stage (Zero Watermarks, Cinematic Push, Stabilized Faces) */}
      <HeroScrollStage />

      {/* 3. What is AegisTwin? Split Header + 3-Card Grid + Network Ticker */}
      <WhatIsAegisTwin />

      {/* 4. Use Cases with Interactive Tab Switching & Neoclassical Illustration */}
      <UseCasesMeadow />

      {/* 5. Complete AegisTwin Clinical Cockpit (Member Personas, Live Sliders, Tripwires, Deprescribing Sandbox) */}
      <IntegratedDigitalTwin />

      {/* 6. 'Let Care Blossom' Dark Interactive Biomarker & Risk Simulator */}
      <DigitalTwinSimulator />

      {/* 7. Health Insurance Plans & Coverage Safeguards (Health Only) */}
      <HealthPlansMeadow />

      {/* 8. Frictionless Cashless Hospital Pre-Authorization & Discharge Settlement */}
      <CashlessClaimsMeadow />

      {/* 9. Questions, Answered (Interactive Accordion FAQ) */}
      <FAQSection />

      {/* 10. Comprehensive Footer with Large Watermark */}
      <FooterMeadow />
    </main>
  );
}
