"""Medical Ontologies, Code Mappings, and Comorbidity Calculators."""

from typing import Dict, List, Set, Tuple

# 1. NDC to RxNorm RxCUI Mapping
# RxCUI -> Standardized Drug Details
RXNORM_KNOWLEDGE: Dict[str, Dict[str, str]] = {
    "855332": {"name": "Warfarin Sodium", "class": "Anticoagulant", "route": "Oral"},
    "1191": {"name": "Aspirin", "class": "NSAID_Antiplatelet", "route": "Oral"},
    "5640": {"name": "Ibuprofen", "class": "NSAID", "route": "Oral"},
    "7052": {"name": "Naproxen", "class": "NSAID", "route": "Oral"},
    "32968": {"name": "Clopidogrel", "class": "Antiplatelet", "route": "Oral"},
    "7646": {"name": "Omeprazole", "class": "Proton_Pump_Inhibitor", "route": "Oral"},
    "29046": {"name": "Lisinopril", "class": "ACE_Inhibitor", "route": "Oral"},
    "9997": {"name": "Spironolactone", "class": "Aldosterone_Antagonist", "route": "Oral"},
    "36437": {"name": "Sertraline", "class": "SSRI", "route": "Oral"},
    "10689": {"name": "Tramadol", "class": "Opioid_Analgesic", "route": "Oral"},
    "6809": {"name": "Metformin", "class": "Biguanide", "route": "Oral"},
    "8703": {"name": "Propranolol", "class": "Nonselective_Beta_Blocker", "route": "Oral"},
    "6918": {"name": "Metoprolol", "class": "Selective_Beta_Blocker", "route": "Oral"},
    "3498": {"name": "Diphenhydramine", "class": "FirstGen_Antihistamine", "route": "Oral"},
    "3322": {"name": "Diazepam", "class": "LongActing_Benzodiazepine", "route": "Oral"},
    "704": {"name": "Amitriptyline", "class": "Tricyclic_Antidepressant", "route": "Oral"},
    "161": {"name": "Acetaminophen", "class": "Analgesic_Antipyretic", "route": "Oral"},
    "3616": {"name": "Digoxin", "class": "Cardiac_Glycoside", "route": "Oral"},
    "435": {"name": "Amiodarone", "class": "Antiarrhythmic", "route": "Oral"},
    "6876": {"name": "Methotrexate", "class": "DMARD_Antimetabolite", "route": "Oral"},
    "10759": {"name": "Triamterene", "class": "PotassiumSparing_Diuretic", "route": "Oral"},
    "31565": {"name": "Simvastatin", "class": "Statin", "route": "Oral"},
    "83367": {"name": "Atorvastatin", "class": "Statin", "route": "Oral"},
    "1114195": {"name": "Linagliptin", "class": "DPP4_Inhibitor", "route": "Oral"},
    "1364430": {"name": "Empagliflozin", "class": "SGLT2_Inhibitor", "route": "Oral"},
}

NDC_TO_RXNORM: Dict[str, str] = {
    "00056-0170-70": "855332",   # Warfarin 5mg
    "00093-0150-01": "1191",     # Aspirin 81mg
    "50580-0601-01": "5640",     # Ibuprofen 400mg
    "00378-0018-01": "7052",     # Naproxen 500mg
    "00078-0357-15": "32968",    # Clopidogrel 75mg
    "00093-0043-01": "7646",     # Omeprazole 20mg
    "00006-0511-54": "29046",    # Lisinopril 10mg
    "00025-1011-31": "9997",     # Spironolactone 25mg
    "00049-4960-66": "36437",    # Sertraline 50mg
    "00093-0158-01": "10689",    # Tramadol 50mg
    "00093-1048-01": "6809",     # Metformin 500mg
    "00008-0085-01": "8703",     # Propranolol 40mg
    "00078-0460-05": "6918",     # Metoprolol 50mg
    "50580-0506-01": "3498",     # Diphenhydramine 25mg
    "00140-0004-01": "3322",     # Diazepam 5mg
    "00071-0156-23": "704",      # Amitriptyline 25mg
    "50580-0449-01": "161",      # Acetaminophen 500mg
    "00173-0242-55": "3616",     # Digoxin 0.125mg
    "00008-0118-01": "435",      # Amiodarone 200mg
    "00054-4550-25": "6876",     # Methotrexate 2.5mg
    "00054-0012-25": "1114195",  # Linagliptin 5mg
    "00597-0152-30": "1364430",  # Empagliflozin 10mg
}

# 2. LOINC Code Definitions and Clinical Reference Standards
LOINC_DICTIONARY: Dict[str, Dict[str, str]] = {
    "33914-3": {"name": "eGFR", "unit": "mL/min/1.73m2", "ref_low": "60.0", "ref_high": "120.0"},
    "4548-4": {"name": "HbA1c", "unit": "%", "ref_low": "4.0", "ref_high": "5.6"},
    "2160-0": {"name": "Serum_Creatinine", "unit": "mg/dL", "ref_low": "0.6", "ref_high": "1.2"},
    "2823-3": {"name": "Potassium", "unit": "mmol/L", "ref_low": "3.5", "ref_high": "5.0"},
    "6301-6": {"name": "INR", "unit": "{ratio}", "ref_low": "0.9", "ref_high": "1.2"},
    "33762-6": {"name": "NT-proBNP", "unit": "pg/mL", "ref_low": "0.0", "ref_high": "125.0"},
    "8480-6": {"name": "Systolic_BP", "unit": "mmHg", "ref_low": "90.0", "ref_high": "120.0"},
    "8462-4": {"name": "Diastolic_BP", "unit": "mmHg", "ref_low": "60.0", "ref_high": "80.0"},
}

# 3. ICD-10 to CCSR (Clinical Classifications Software Refined) Mapping
ICD10_TO_CCSR: Dict[str, Tuple[str, str]] = {
    "I10": ("CIR007", "Essential hypertension"),
    "I50.9": ("CIR019", "Heart failure"),
    "E11.9": ("END002", "Type 2 diabetes without complications"),
    "E11.22": ("END003", "Type 2 diabetes with diabetic chronic kidney disease"),
    "N18.3": ("GEN003", "Chronic kidney disease, stage 3"),
    "N18.4": ("GEN003", "Chronic kidney disease, stage 4"),
    "N18.5": ("GEN003", "Chronic kidney disease, stage 5"),
    "J44.9": ("RSP008", "Chronic obstructive pulmonary disease, unspecified"),
    "J45.909": ("RSP009", "Unspecified asthma, uncomplicated"),
    "J45.40": ("RSP009", "Moderate persistent asthma, uncomplicated"),
    "I48.91": ("CIR017", "Unspecified atrial fibrillation"),
    "I25.10": ("CIR011", "Atherosclerotic heart disease of native coronary artery"),
    "F32.9": ("MBD002", "Major depressive disorder, single episode, unspecified"),
    "M17.9": ("MUS010", "Osteoarthritis of knee, unspecified"),
    "R29.6": ("SYM015", "Repeated falls / Fall history"),
    "K21.9": ("DIG004", "Gastro-esophageal reflux disease without esophagitis"),
}

# 4. Charlson Comorbidity Index (CCI) Scoring Weights
CHARLSON_WEIGHTS: Dict[str, Tuple[int, str]] = {
    "I21": (1, "Myocardial infarction"),
    "I25": (1, "Coronary artery disease"),
    "I50": (1, "Congestive heart failure"),
    "I73": (1, "Peripheral vascular disease"),
    "I63": (1, "Cerebrovascular disease"),
    "F03": (1, "Dementia"),
    "J44": (1, "Chronic pulmonary disease"),
    "M05": (1, "Connective tissue disease"),
    "K25": (1, "Peptic ulcer disease"),
    "E11.9": (1, "Mild diabetes without end-organ damage"),
    "E11.2": (2, "Diabetes with chronic complications"),
    "G81": (2, "Hemiplegia or paraplegia"),
    "N18": (2, "Moderate or severe renal disease"),
    "C80": (2, "Any malignancy"),
    "K72": (3, "Moderate or severe liver disease"),
    "C79": (6, "Metastatic solid tumor"),
    "B20": (6, "AIDS/HIV"),
}

# 5. Elixhauser Comorbidity Map (Flag presence)
ELIXHAUSER_CATEGORIES = {
    "CHF": ["I50"],
    "ARRHYTHMIA": ["I48", "I49"],
    "HYPERTENSION": ["I10", "I11"],
    "DIABETES_UNCOMP": ["E11.9"],
    "DIABETES_COMP": ["E11.2", "E11.3", "E11.4"],
    "RENAL_FAILURE": ["N18.3", "N18.4", "N18.5", "N19"],
    "COPD": ["J44"],
    "ASTHMA": ["J45"],
    "DEPRESSION": ["F32", "F33"],
    "OBESITY": ["E66"],
    "LIVER_DISEASE": ["K70", "K72", "K74"],
}

# 6. AGS Beers Criteria (Geriatric Potentially Inappropriate Medications, Age >= 65)
BEERS_CRITERIA_RXCUI: Dict[str, Dict[str, str]] = {
    "3498": {  # Diphenhydramine
        "drug": "Diphenhydramine",
        "category": "Anticholinergic",
        "rationale": "High anticholinergic risk: delirium, urinary retention, cognitive decline, falls.",
        "severity": "CRITICAL"
    },
    "3322": {  # Diazepam
        "drug": "Diazepam",
        "category": "Benzodiazepine",
        "rationale": "Long half-life benzodiazepine: increased risk of falls, motor vehicle accidents, hip fractures.",
        "severity": "CRITICAL"
    },
    "704": {  # Amitriptyline
        "drug": "Amitriptyline",
        "category": "Tricyclic_Antidepressant",
        "rationale": "Highly anticholinergic and sedating, orthostatic hypotension and cardiac arrhythmias.",
        "severity": "MODERATE"
    },
    "5640": {  # Ibuprofen (Chronic use in elderly)
        "drug": "Ibuprofen",
        "category": "Oral_NSAID",
        "rationale": "Increased risk of GI bleeding, peptic ulcer disease, acute kidney injury, exacerbation of heart failure.",
        "severity": "MODERATE"
    }
}

def calculate_charlson_score(icd10_codes: List[str]) -> int:
    """Calculates weighted Charlson Comorbidity Index score."""
    score = 0
    matched_prefixes: Set[str] = set()
    for code in icd10_codes:
        for prefix, (weight, _) in CHARLSON_WEIGHTS.items():
            if code.startswith(prefix) and prefix not in matched_prefixes:
                score += weight
                matched_prefixes.add(prefix)
    return score

def calculate_elixhauser_flags(icd10_codes: List[str]) -> Dict[str, int]:
    """Computes binary flags for Elixhauser Comorbidity domains."""
    flags: Dict[str, int] = {cat: 0 for cat in ELIXHAUSER_CATEGORIES}
    for code in icd10_codes:
        for cat, prefixes in ELIXHAUSER_CATEGORIES.items():
            if any(code.startswith(p) for p in prefixes):
                flags[cat] = 1
    return flags
