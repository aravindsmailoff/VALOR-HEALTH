export interface MemberProfile {
  id: string;
  name: string;
  age: number;
  gender: "Female" | "Male" | "Other";
  planType: string;
  riskTier: "CRITICAL" | "HIGH" | "MODERATE" | "LOW";
  risk90d: number; // 0.0 - 1.0
  risk90dLower: number;
  risk90dUpper: number;
  readmit30d: number;
  progression12m: number;
  upliftITE: number; // Causal outreach impact
  annualSpend: number;
  adi: number; // Area Deprivation Index (1-100)
  sdohFlags: string[];
  conditions: {
    code: string;
    description: string;
    ccsr: string;
    onsetDate: string;
    severity: "Mild" | "Moderate" | "Severe";
  }[];
  medications: {
    rxnorm: string;
    name: string;
    class: string;
    dose: string;
    pdc90d: number;
    fills90d: number;
    status: "Active" | "Refill Due" | "Overdue";
  }[];
  labs: {
    test: string;
    value: string;
    unit: string;
    status: "Normal" | "Elevated" | "Low" | "Critical";
    date: string;
    history: { date: string; value: number }[];
  }[];
  wearables: {
    avgDailySteps: number;
    restingHR: number;
    sleepHours: number;
    batteryDays: number;
    telemetryHistory: { day: string; steps: number; hr: number }[];
  };
  safetyFindings: {
    id: string;
    type: "DDI" | "DCI" | "BEERS";
    severity: "CRITICAL" | "WARNING";
    title: string;
    mechanism: string;
    recommendedAction: string;
    drugsInvolved: string[];
    evidence: string;
    cleared?: boolean;
  }[];
  shapFeatures: {
    feature: string;
    label: string;
    impact: number; // Positive increases risk, negative decreases
    clinicalInterpretation: string;
  }[];
  laymanNarrative: {
    summary: string;
    whyItMatters: string;
    nextSteps: string[];
    payerSavings: number;
  };
}

export const MEMBER_PROFILES: MemberProfile[] = [
  {
    id: "PT-001",
    name: "Eleanor Vance",
    age: 72,
    gender: "Female",
    planType: "Medicare Advantage (Senior Gold HMO)",
    riskTier: "CRITICAL",
    risk90d: 0.74,
    risk90dLower: 0.64,
    risk90dUpper: 0.83,
    readmit30d: 0.42,
    progression12m: 0.68,
    upliftITE: 0.18,
    annualSpend: 38400,
    adi: 78,
    sdohFlags: ["High Deprivation Area (ADI 78)", "Limited Medical Transit Access"],
    conditions: [
      {
        code: "E11.22",
        description: "Type 2 Diabetes with Diabetic Chronic Kidney Disease",
        ccsr: "END003 - Diabetes Mellitus",
        onsetDate: "2021-04-12",
        severity: "Severe",
      },
      {
        code: "N18.32",
        description: "Chronic Kidney Disease, Stage 3b (Moderate-to-Severe)",
        ccsr: "GEN003 - Chronic Kidney Disease",
        onsetDate: "2023-01-18",
        severity: "Severe",
      },
      {
        code: "I10",
        description: "Essential (Primary) Hypertension",
        ccsr: "CIR007 - Hypertension",
        onsetDate: "2018-09-02",
        severity: "Moderate",
      },
    ],
    medications: [
      {
        rxnorm: "6809",
        name: "Metformin Hydrochloride",
        class: "Biguanide Antidiabetic",
        dose: "1,000 mg BID",
        pdc90d: 0.94,
        fills90d: 3,
        status: "Active",
      },
      {
        rxnorm: "314164",
        name: "Empagliflozin (Jardiance)",
        class: "SGLT2 Inhibitor",
        dose: "10 mg Daily",
        pdc90d: 0.88,
        fills90d: 3,
        status: "Active",
      },
      {
        rxnorm: "6581",
        name: "Lisinopril",
        class: "ACE Inhibitor",
        dose: "20 mg Daily",
        pdc90d: 0.92,
        fills90d: 3,
        status: "Active",
      },
    ],
    labs: [
      {
        test: "eGFR (Estimated Glomerular Filtration Rate)",
        value: "27.4",
        unit: "mL/min/1.73m²",
        status: "Critical",
        date: "2026-10-15",
        history: [
          { date: "6m ago", value: 42.0 },
          { date: "4m ago", value: 36.2 },
          { date: "2m ago", value: 31.0 },
          { date: "Current", value: 27.4 },
        ],
      },
      {
        test: "HbA1c (Glycated Hemoglobin)",
        value: "8.6",
        unit: "%",
        status: "Elevated",
        date: "2026-10-15",
        history: [
          { date: "6m ago", value: 8.9 },
          { date: "4m ago", value: 8.7 },
          { date: "2m ago", value: 8.8 },
          { date: "Current", value: 8.6 },
        ],
      },
      {
        test: "Serum Creatinine",
        value: "2.1",
        unit: "mg/dL",
        status: "Elevated",
        date: "2026-10-15",
        history: [
          { date: "6m ago", value: 1.5 },
          { date: "4m ago", value: 1.8 },
          { date: "2m ago", value: 1.95 },
          { date: "Current", value: 2.1 },
        ],
      },
    ],
    wearables: {
      avgDailySteps: 2840,
      restingHR: 76,
      sleepHours: 5.8,
      batteryDays: 14,
      telemetryHistory: [
        { day: "Mon", steps: 3100, hr: 75 },
        { day: "Tue", steps: 2700, hr: 77 },
        { day: "Wed", steps: 2900, hr: 76 },
        { day: "Thu", steps: 2400, hr: 78 },
        { day: "Fri", steps: 3200, hr: 74 },
        { day: "Sat", steps: 2800, hr: 76 },
        { day: "Sun", steps: 2780, hr: 77 },
      ],
    },
    safetyFindings: [
      {
        id: "FINDING-DCI-01",
        type: "DCI",
        severity: "CRITICAL",
        title: "Metformin in Severe Renal Impairment (eGFR < 30)",
        mechanism: "FDA Black Box Contraindication: Metformin accumulation under eGFR < 30 mL/min carries a life-threatening risk of lactic acidosis.",
        recommendedAction: "Immediately discontinue Metformin. Transition to renal-sparing DPP-4 inhibitor (Linagliptin) or adjust insulin regimen.",
        drugsInvolved: ["Metformin HCl 1000mg"],
        evidence: "FDA Guidance & KDIGO 2024 Clinical Practice Guideline for Diabetes Management in CKD",
      },
    ],
    shapFeatures: [
      {
        feature: "egfr_current_value",
        label: "Low eGFR (<30 mL/min)",
        impact: +0.31,
        clinicalInterpretation: "Pre-dialysis renal dysfunction accelerates hospitalization probability by 3.2x.",
      },
      {
        feature: "dci_safety_alert_flag",
        label: "Active DCI Metformin Tripwire",
        impact: +0.22,
        clinicalInterpretation: "Unresolved contraindication is the primary preventable admission trigger.",
      },
      {
        feature: "area_deprivation_index",
        label: "High Area Deprivation (ADI 78)",
        impact: +0.12,
        clinicalInterpretation: "Neighborhood transit barriers delay clinical follow-ups.",
      },
      {
        feature: "med_adherence_pdc",
        label: "Consistent Fill Adherence",
        impact: -0.09,
        clinicalInterpretation: "Regular fills protect against acute glycemic crisis.",
      },
    ],
    laymanNarrative: {
      summary: "Eleanor is taking a diabetes medicine (Metformin) that is no longer safe because her recent kidney lab test dropped below the healthy threshold.",
      whyItMatters: "Continuing this medication with her current kidney function can cause severe medication build-up leading to an emergency hospital visit.",
      nextSteps: [
        "Clinical nurse care manager outreach scheduled within 24 hours.",
        "Coordinate with Dr. Kaplan to swap Metformin to a kidney-friendly alternative.",
        "Provide complimentary medical transport for next month's repeat lab check.",
      ],
      payerSavings: 14200,
    },
  },
  {
    id: "PT-002",
    name: "Marcus Chen",
    age: 54,
    gender: "Male",
    planType: "Commercial Comprehensive PPO",
    riskTier: "HIGH",
    risk90d: 0.58,
    risk90dLower: 0.49,
    risk90dUpper: 0.67,
    readmit30d: 0.28,
    progression12m: 0.44,
    upliftITE: 0.22,
    annualSpend: 24500,
    adi: 32,
    sdohFlags: ["High Occupational Stress"],
    conditions: [
      {
        code: "I25.10",
        description: "Atherosclerotic Heart Disease of Native Coronary Artery (Post-PCI)",
        ccsr: "CIR011 - Coronary Atherosclerosis",
        onsetDate: "2024-03-10",
        severity: "Severe",
      },
      {
        code: "M17.11",
        description: "Unilateral Primary Osteoarthritis, Right Knee",
        ccsr: "MUS001 - Osteoarthritis",
        onsetDate: "2022-11-05",
        severity: "Moderate",
      },
    ],
    medications: [
      {
        rxnorm: "11289",
        name: "Warfarin Sodium (Coumadin)",
        class: "Vitamin K Antagonist Anticoagulant",
        dose: "5 mg Daily",
        pdc90d: 0.82,
        fills90d: 3,
        status: "Active",
      },
      {
        rxnorm: "5640",
        name: "Ibuprofen (Advil / Motrin)",
        class: "NSAID Analgesic",
        dose: "800 mg TID PRN",
        pdc90d: 0.65,
        fills90d: 2,
        status: "Active",
      },
      {
        rxnorm: "83367",
        name: "Atorvastatin Calcium",
        class: "HMG-CoA Reductase Inhibitor",
        dose: "80 mg Daily",
        pdc90d: 0.90,
        fills90d: 3,
        status: "Active",
      },
    ],
    labs: [
      {
        test: "INR (Prothrombin Time)",
        value: "2.8",
        unit: "Ratio",
        status: "Normal",
        date: "2026-10-18",
        history: [
          { date: "6m ago", value: 2.3 },
          { date: "4m ago", value: 2.5 },
          { date: "2m ago", value: 2.6 },
          { date: "Current", value: 2.8 },
        ],
      },
      {
        test: "Hemoglobin",
        value: "13.4",
        unit: "g/dL",
        status: "Normal",
        date: "2026-10-18",
        history: [
          { date: "6m ago", value: 14.8 },
          { date: "4m ago", value: 14.2 },
          { date: "2m ago", value: 13.9 },
          { date: "Current", value: 13.4 },
        ],
      },
    ],
    wearables: {
      avgDailySteps: 6400,
      restingHR: 68,
      sleepHours: 6.9,
      batteryDays: 12,
      telemetryHistory: [
        { day: "Mon", steps: 6800, hr: 67 },
        { day: "Tue", steps: 6200, hr: 68 },
        { day: "Wed", steps: 7100, hr: 66 },
        { day: "Thu", steps: 5900, hr: 70 },
        { day: "Fri", steps: 6500, hr: 68 },
        { day: "Sat", steps: 7400, hr: 65 },
        { day: "Sun", steps: 6100, hr: 69 },
      ],
    },
    safetyFindings: [
      {
        id: "FINDING-DDI-02",
        type: "DDI",
        severity: "CRITICAL",
        title: "Major Bleeding Risk: Warfarin + High-Dose NSAID (Ibuprofen)",
        mechanism: "Concurrent systemic NSAIDs inhibit platelet aggregation and cause gastric mucosal erosions while Warfarin impairs clotting factor synthesis, raising severe GI hemorrhage risk 4.5-fold.",
        recommendedAction: "Deprescribe systemic NSAID. Substitute with topical Voltaren gel or Acetaminophen, with gastroprotective PPI coverage if needed.",
        drugsInvolved: ["Warfarin 5mg", "Ibuprofen 800mg"],
        evidence: "American College of Cardiology (ACC) & CHEST Guidelines on Antithrombotic Therapy",
      },
    ],
    shapFeatures: [
      {
        feature: "ddi_warfarin_nsaid_interaction",
        label: "Warfarin + NSAID Clash",
        impact: +0.28,
        clinicalInterpretation: "Severe gastrointestinal bleeding tripwire active.",
      },
      {
        feature: "post_pci_coronary_history",
        label: "Coronary Stent within 12 Months",
        impact: +0.16,
        clinicalInterpretation: "Cardiac readmission susceptibility remains elevated.",
      },
      {
        feature: "cardio_fitness_steps",
        label: "Good Physical Activity (>6k Steps)",
        impact: -0.11,
        clinicalInterpretation: "Cardiovascular endurance mitigates acute cardiac decompensation.",
      },
    ],
    laymanNarrative: {
      summary: "Marcus is taking Ibuprofen for knee soreness while on the blood thinner Warfarin, creating an unsafe internal bleeding risk.",
      whyItMatters: "Combining these two everyday medications dramatically thins the stomach lining and blood at the same time, leading to preventable ER visits.",
      nextSteps: [
        "Replace oral Ibuprofen with a doctor-approved topical pain relief gel.",
        "Pharmacist call to verify over-the-counter medication safety.",
        "Physical therapy enrollment for knee rehabilitation without heavy pills.",
      ],
      payerSavings: 11800,
    },
  },
  {
    id: "PT-003",
    name: "Sarah Jenkins",
    age: 38,
    gender: "Female",
    planType: "High Deductible Health Plan (HDHP + HSA)",
    riskTier: "LOW",
    risk90d: 0.12,
    risk90dLower: 0.08,
    risk90dUpper: 0.18,
    readmit30d: 0.04,
    progression12m: 0.09,
    upliftITE: 0.03,
    annualSpend: 3200,
    adi: 18,
    sdohFlags: ["Affluent Area", "Zero Transportation Barriers"],
    conditions: [
      {
        code: "Z00.00",
        description: "Encounter for General Adult Medical Examination Without Abnormal Findings",
        ccsr: "FAC001 - Routine Examination",
        onsetDate: "2026-08-14",
        severity: "Mild",
      },
    ],
    medications: [
      {
        rxnorm: "105267",
        name: "Cholecalciferol (Vitamin D3)",
        class: "Nutritional Supplement",
        dose: "2,000 IU Daily",
        pdc90d: 0.96,
        fills90d: 3,
        status: "Active",
      },
    ],
    labs: [
      {
        test: "Total Cholesterol",
        value: "178",
        unit: "mg/dL",
        status: "Normal",
        date: "2026-08-14",
        history: [
          { date: "12m ago", value: 182 },
          { date: "Current", value: 178 },
        ],
      },
      {
        test: "Fasting Plasma Glucose",
        value: "88",
        unit: "mg/dL",
        status: "Normal",
        date: "2026-08-14",
        history: [
          { date: "12m ago", value: 90 },
          { date: "Current", value: 88 },
        ],
      },
    ],
    wearables: {
      avgDailySteps: 10450,
      restingHR: 58,
      sleepHours: 7.8,
      batteryDays: 20,
      telemetryHistory: [
        { day: "Mon", steps: 11200, hr: 58 },
        { day: "Tue", steps: 9800, hr: 59 },
        { day: "Wed", steps: 12400, hr: 57 },
        { day: "Thu", steps: 10100, hr: 58 },
        { day: "Fri", steps: 10900, hr: 57 },
        { day: "Sat", steps: 11800, hr: 56 },
        { day: "Sun", steps: 9400, hr: 58 },
      ],
    },
    safetyFindings: [],
    shapFeatures: [
      {
        feature: "high_physical_activity",
        label: "Active Lifestyle (>10k steps)",
        impact: -0.24,
        clinicalInterpretation: "Cardiorespiratory fitness strongly buffers all-cause acute event risk.",
      },
      {
        feature: "zero_chronic_diagnoses",
        label: "No Chronic Morbidities",
        impact: -0.19,
        clinicalInterpretation: "Absence of metabolic or cardiovascular disease.",
      },
    ],
    laymanNarrative: {
      summary: "Sarah has a clean bill of health with optimal biomarker levels, excellent physical activity, and zero medication contraindications.",
      whyItMatters: "Preventative checkups and wellness engagement keep her out-of-pocket costs low while maximizing insurance premium credits.",
      nextSteps: [
        "Earn $200 VALOR annual wellness dividend by logging preventive dental exam.",
        "Maintain current healthy biometric benchmarks.",
      ],
      payerSavings: 1400,
    },
  },
  {
    id: "PT-004",
    name: "Arthur Pendelton",
    age: 81,
    gender: "Male",
    planType: "Dual Eligible Special Needs Plan (D-SNP)",
    riskTier: "CRITICAL",
    risk90d: 0.82,
    risk90dLower: 0.72,
    risk90dUpper: 0.89,
    readmit30d: 0.48,
    progression12m: 0.76,
    upliftITE: 0.26,
    annualSpend: 46200,
    adi: 84,
    sdohFlags: ["High Social Deprivation", "Fall Risk Home Environment", "Lives Alone"],
    conditions: [
      {
        code: "J44.1",
        description: "Chronic Obstructive Pulmonary Disease with (Acute) Exacerbation",
        ccsr: "RSP008 - Chronic Obstructive Pulmonary Disease",
        onsetDate: "2020-02-14",
        severity: "Severe",
      },
      {
        code: "R29.6",
        description: "Repeated Falls / Gait Instability",
        ccsr: "SYM014 - Gait Abnormalities",
        onsetDate: "2024-06-20",
        severity: "Severe",
      },
    ],
    medications: [
      {
        rxnorm: "704",
        name: "Amitriptyline Hydrochloride",
        class: "Tricyclic Antidepressant / Neuropathic Agent",
        dose: "50 mg QHS",
        pdc90d: 0.78,
        fills90d: 2,
        status: "Active",
      },
      {
        rxnorm: "135677",
        name: "Tiotropium Bromide (Spiriva)",
        class: "Long-Acting Anticholinergic Bronchodilator",
        dose: "1 Inhalation Daily",
        pdc90d: 0.85,
        fills90d: 3,
        status: "Active",
      },
    ],
    labs: [
      {
        test: "Pulse Oximetry (SpO2)",
        value: "91",
        unit: "%",
        status: "Low",
        date: "2026-10-21",
        history: [
          { date: "6m ago", value: 94 },
          { date: "4m ago", value: 93 },
          { date: "2m ago", value: 92 },
          { date: "Current", value: 91 },
        ],
      },
    ],
    wearables: {
      avgDailySteps: 1100,
      restingHR: 84,
      sleepHours: 5.2,
      batteryDays: 8,
      telemetryHistory: [
        { day: "Mon", steps: 1200, hr: 83 },
        { day: "Tue", steps: 950, hr: 85 },
        { day: "Wed", steps: 1100, hr: 84 },
        { day: "Thu", steps: 890, hr: 86 },
        { day: "Fri", steps: 1300, hr: 82 },
        { day: "Sat", steps: 1050, hr: 84 },
        { day: "Sun", steps: 1120, hr: 83 },
      ],
    },
    safetyFindings: [
      {
        id: "FINDING-BEERS-03",
        type: "BEERS",
        severity: "CRITICAL",
        title: "AGS Beers Criteria: High Anticholinergic Sedation & Fall Risk (Amitriptyline in ≥65yo)",
        mechanism: "Potent anticholinergic and alpha-adrenergic blockade induces orthostatic hypotension, confusion, and ataxia in elderly members with history of repeated falls.",
        recommendedAction: "Deprescribe Amitriptyline. Taper off and transition to safe non-anticholinergic alternatives (Duloxetine or Gabapentin). Order home safety evaluation.",
        drugsInvolved: ["Amitriptyline 50mg"],
        evidence: "American Geriatrics Society (AGS) 2023 Beers Criteria for Potentially Inappropriate Medication Use in Older Adults",
      },
    ],
    shapFeatures: [
      {
        feature: "beers_anticholinergic_fall_hazard",
        label: "Beers Criteria Fall Tripwire",
        impact: +0.34,
        clinicalInterpretation: "Strongest predictor of acute hip fracture / traumatic injury.",
      },
      {
        feature: "copd_exacerbation_history",
        label: "Frequent Respiratory Exacerbations",
        impact: +0.26,
        clinicalInterpretation: "High baseline vulnerability for ICU respiratory admission.",
      },
      {
        feature: "extreme_sedentary_behavior",
        label: "Severe Immobility (<1.5k Steps)",
        impact: +0.15,
        clinicalInterpretation: "Reflects frail functional status and sarcopenia.",
      },
    ],
    laymanNarrative: {
      summary: "Arthur is taking a strong nerve/sleep medication (Amitriptyline) that is classified as hazardous for seniors with balance problems.",
      whyItMatters: "This medication causes sudden dizziness upon standing, dramatically increasing the risk of a severe fall or hip fracture.",
      nextSteps: [
        "In-home nurse visit to evaluate rugs, grab bars, and bathroom lighting.",
        "Physician consultation to safely taper off Amitriptyline.",
        "Dispatch wearable fall-detection medical pendant.",
      ],
      payerSavings: 22600,
    },
  },
];
