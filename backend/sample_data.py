sample_data = {
    "BIO-20231205":{
        "name": "John Doe",
        "patientid": "BIO-20231205",
        "patientDOB": "May 21, 1989",
        "patient_history": [
        {
            "type": "diagnostic",
            "label": "Annual physical",
            "date": "Jan 2025",
            "items": [
                "Routine exam, vitals WNL",
                "CBC and metabolic panel ordered",
                "Patient advised to continue diet and exercise",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Hypertension follow-up",
            "date": "Nov 2024",
            "items": [
                "BP 132/82 on current regimen",
                "Lisinopril dose maintained",
                "Next check in 3 months",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Lab results",
            "date": "Oct 2024",
            "items": [
                "HbA1c 5.8% (prediabetic range)",
                "LDL 118 mg/dL",
                "TSH 2.1 mIU/L",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Cardiology consult",
            "date": "Aug 2024",
            "items": [
                "Echo showed mild LVH, EF 58%",
                "Stress test negative for ischemia",
                "Continue current cardiac meds",
            ],
        },
    ],
        "current_medications": [
        {
            "type": "diagnostic",
            "label": "Lisinopril",
            "conflicts": [],
            "items": ["10 mg once daily", "For hypertension"],
            # TODO(OpenFDA): description = openfda.get_drug_description(label)  # e.g. purpose/indications
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Atorvastatin",
            "conflicts": [],
            "items": ["20 mg once daily at bedtime", "For LDL cholesterol"],
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Aspirin",
            "conflicts": [],
            "items": ["81 mg once daily", "Cardioprotective"],
            "description": None,
        },
    ],
        "family_history": [
        {
            "type": "diagnostic",
            "label": "Robert Doe",
            "relation": "Father",
            "conditions": ["Hypertension", "Type 2 diabetes", "Myocardial infarction (age 58)"],
        },
        {
            "type": "diagnostic",
            "label": "Mary Doe",
            "relation": "Mother",
            "conditions": ["Hypothyroidism", "Osteoporosis"],
        },
        {
            "type": "diagnostic",
            "label": "William Doe",
            "relation": "Paternal grandfather",
            "conditions": ["Stroke", "Atrial fibrillation"],
        },
    ]
    },
    "BIO-20240308":{
        "name": "Emily Watson",
        "patientid": "BIO-20240308",
        "patientDOB": "May 21, 1989",
        "patient_history": [
        {
            "type": "diagnostic",
            "label": "Annual physical",
            "date": "Jan 2025",
            "items": [
                "Routine exam, vitals WNL",
                "CBC and metabolic panel ordered",
                "Patient advised to continue diet and exercise",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Hypertension follow-up",
            "date": "Nov 2024",
            "items": [
                "BP 132/82 on current regimen",
                "Lisinopril dose maintained",
                "Next check in 3 months",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Lab results",
            "date": "Oct 2024",
            "items": [
                "HbA1c 5.8% (prediabetic range)",
                "LDL 118 mg/dL",
                "TSH 2.1 mIU/L",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Cardiology consult",
            "date": "Aug 2024",
            "items": [
                "Echo showed mild LVH, EF 58%",
                "Stress test negative for ischemia",
                "Continue current cardiac meds",
            ],
        },
    ],
        "current_medications": [
        {
            "type": "diagnostic",
            "label": "Lisinopril",
            "conflicts": [],
            "items": ["10 mg once daily", "For hypertension"],
            # TODO(OpenFDA): description = openfda.get_drug_description(label)  # e.g. purpose/indications
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Atorvastatin",
            "conflicts": [],
            "items": ["20 mg once daily at bedtime", "For LDL cholesterol"],
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Aspirin",
            "conflicts": [],
            "items": ["81 mg once daily", "Cardioprotective"],
            "description": None,
        },
    ],
        "family_history": [
        {
            "type": "diagnostic",
            "label": "Patricia Watson",
            "relation": "Mother",
            "conditions": ["Breast cancer (age 52)", "Hypertension"],
        },
        {
            "type": "diagnostic",
            "label": "James Watson",
            "relation": "Father",
            "conditions": ["Type 2 diabetes", "Hyperlipidemia"],
        },
        {
            "type": "diagnostic",
            "label": "Helen Mitchell",
            "relation": "Maternal grandmother",
            "conditions": ["Osteoporosis", "Rheumatoid arthritis"],
        },
    ]
    },
    "BIO-20240521":{
        "name": "John Johnson",
        "patientid": "BIO-20240521",
        "patientDOB": "May 21, 1989",
        "patient_history": [
        {
            "type": "diagnostic",
            "label": "Annual physical",
            "date": "Jan 2025",
            "items": [
                "Routine exam, vitals WNL",
                "CBC and metabolic panel ordered",
                "Patient advised to continue diet and exercise",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Hypertension follow-up",
            "date": "Nov 2024",
            "items": [
                "BP 132/82 on current regimen",
                "Lisinopril dose maintained",
                "Next check in 3 months",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Lab results",
            "date": "Oct 2024",
            "items": [
                "HbA1c 5.8% (prediabetic range)",
                "LDL 118 mg/dL",
                "TSH 2.1 mIU/L",
            ],
        },
        {
            "type": "diagnostic",
            "label": "Cardiology consult",
            "date": "Aug 2024",
            "items": [
                "Echo showed mild LVH, EF 58%",
                "Stress test negative for ischemia",
                "Continue current cardiac meds",
            ],
        },
    ],
        "current_medications": [
        {
            "type": "diagnostic",
            "label": "Lisinopril",
            "conflicts": [],
            "items": ["10 mg once daily", "For hypertension"],
            # TODO(OpenFDA): description = openfda.get_drug_description(label)  # e.g. purpose/indications
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Atorvastatin",
            "conflicts": [],
            "items": ["20 mg once daily at bedtime", "For LDL cholesterol"],
            "description": None,
        },
        {
            "type": "diagnostic",
            "label": "Aspirin",
            "conflicts": [],
            "items": ["81 mg once daily", "Cardioprotective"],
            "description": None,
        },
    ],
        "family_history": [
        {
            "type": "diagnostic",
            "label": "David Johnson",
            "relation": "Father",
            "conditions": ["Coronary artery disease", "Hypertension", "Stroke (age 62)"],
        },
        {
            "type": "diagnostic",
            "label": "Susan Johnson",
            "relation": "Mother",
            "conditions": ["Type 2 diabetes", "Chronic kidney disease stage 3"],
        },
        {
            "type": "diagnostic",
            "label": "Michael Johnson",
            "relation": "Brother",
            "conditions": ["Hypertension", "Hyperlipidemia"],
        },
    ]
    },
    "BIO-20240601": {
        "name": "Yuki Tanaka",
        "patientid": "BIO-20240601",
        "patientDOB": "March 14, 1995",
        "patient_history": [
            {"type": "diagnostic", "label": "Asthma follow-up", "date": "Feb 2025", "items": ["PEF improved on current regimen", "Continue Symbicort", "Annual flu shot given"]},
            {"type": "diagnostic", "label": "Allergy testing", "date": "Dec 2024", "items": ["Environmental allergies confirmed", "Pollen, dust mite positive", "Started nasal steroid"]},
            {"type": "diagnostic", "label": "Urgent care", "date": "Oct 2024", "items": ["Acute bronchitis", "Course of azithromycin", "Resolved"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Fluticasone/Salmeterol", "conflicts": [], "items": ["1 inhalation twice daily", "Asthma control"], "description": None},
            {"type": "diagnostic", "label": "Albuterol", "conflicts": [], "items": ["2 puffs PRN", "Rescue inhaler"], "description": None},
            {"type": "diagnostic", "label": "Cetirizine", "conflicts": [], "items": ["10 mg daily", "Allergies"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "Kenji Tanaka", "relation": "Father", "conditions": ["Asthma", "Hypertension"]},
            {"type": "diagnostic", "label": "Mei Tanaka", "relation": "Mother", "conditions": ["Seasonal allergies", "Migraine"]},
        ]
    },
    "BIO-20240715": {
        "name": "Priya Sharma",
        "patientid": "BIO-20240715",
        "patientDOB": "July 22, 1988",
        "patient_history": [
            {"type": "diagnostic", "label": "Prenatal visit", "date": "Feb 2025", "items": ["28 weeks gestation", "GDM screening ordered", "Fetal heart rate 145 bpm"]},
            {"type": "diagnostic", "label": "OB follow-up", "date": "Jan 2025", "items": ["Anatomy scan normal", "Prenatal vitamins continued", "Next visit 2 weeks"]},
            {"type": "diagnostic", "label": "Hypothyroidism check", "date": "Nov 2024", "items": ["TSH 2.4 mIU/L", "Levothyroxine dose unchanged"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Levothyroxine", "conflicts": [], "items": ["75 mcg daily", "Hypothyroidism"], "description": None},
            {"type": "diagnostic", "label": "Prenatal vitamin", "conflicts": [], "items": ["Once daily", "Folic acid, iron"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "Raj Sharma", "relation": "Father", "conditions": ["Type 2 diabetes", "CAD"]},
            {"type": "diagnostic", "label": "Anita Sharma", "relation": "Mother", "conditions": ["Hypothyroidism", "Osteoporosis"]},
            {"type": "diagnostic", "label": "Lakshmi Patel", "relation": "Maternal grandmother", "conditions": ["Type 2 diabetes"]},
        ]
    },
    "BIO-20240820": {
        "name": "Marcus Williams",
        "patientid": "BIO-20240820",
        "patientDOB": "November 8, 1972",
        "patient_history": [
            {"type": "diagnostic", "label": "Diabetes follow-up", "date": "Jan 2025", "items": ["HbA1c 7.2%", "Metformin increased", "Foot exam normal"]},
            {"type": "diagnostic", "label": "Nephrology referral", "date": "Dec 2024", "items": ["CKD stage 3a", "eGFR 52", "Low-protein diet discussed"]},
            {"type": "diagnostic", "label": "Retinal exam", "date": "Oct 2024", "items": ["No diabetic retinopathy", "Annual follow-up"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Metformin", "conflicts": [], "items": ["1000 mg twice daily", "Type 2 diabetes"], "description": None},
            {"type": "diagnostic", "label": "Lisinopril", "conflicts": [], "items": ["20 mg daily", "Hypertension, kidney protection"], "description": None},
            {"type": "diagnostic", "label": "Atorvastatin", "conflicts": [], "items": ["40 mg nightly", "Hyperlipidemia"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "James Williams", "relation": "Father", "conditions": ["Type 2 diabetes", "Amputation (diabetic)"]},
            {"type": "diagnostic", "label": "Dorothy Williams", "relation": "Mother", "conditions": ["Hypertension", "Stroke (age 68)"]},
            {"type": "diagnostic", "label": "Anthony Williams", "relation": "Brother", "conditions": ["Prediabetes"]},
        ]
    },
    "BIO-20240910": {
        "name": "Fatima Hassan",
        "patientid": "BIO-20240910",
        "patientDOB": "January 3, 2001",
        "patient_history": [
            {"type": "diagnostic", "label": "Depression follow-up", "date": "Feb 2025", "items": ["PHQ-9 score 8", "Mood improved on current dose", "Continue therapy"]},
            {"type": "diagnostic", "label": "Anxiety screening", "date": "Dec 2024", "items": ["GAD-7 moderate", "CBT referral", "Sertraline started"]},
            {"type": "diagnostic", "label": "Annual physical", "date": "Sep 2024", "items": ["Vitals WNL", "Depression screen positive", "Referred to PCP"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Sertraline", "conflicts": [], "items": ["50 mg daily", "Depression, anxiety"], "description": None},
            {"type": "diagnostic", "label": "Vitamin D3", "conflicts": [], "items": ["2000 IU daily", "Deficiency"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "Omar Hassan", "relation": "Father", "conditions": ["Hypertension"]},
            {"type": "diagnostic", "label": "Layla Hassan", "relation": "Mother", "conditions": ["Depression", "Hypothyroidism"]},
        ]
    },
    "BIO-20241005": {
        "name": "Carlos Mendez",
        "patientid": "BIO-20241005",
        "patientDOB": "September 19, 1985",
        "patient_history": [
            {"type": "diagnostic", "label": "Knee pain evaluation", "date": "Jan 2025", "items": ["Patellofemoral syndrome", "PT prescribed", "NSAIDs as needed"]},
            {"type": "diagnostic", "label": "Sports physical", "date": "Aug 2024", "items": ["Cleared for soccer", "BP 118/76", "No restrictions"]},
            {"type": "diagnostic", "label": "Laceration repair", "date": "Jun 2024", "items": ["Right forearm", "5 sutures", "Tdap current"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Ibuprofen", "conflicts": [], "items": ["400 mg PRN", "Knee pain"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "Jose Mendez", "relation": "Father", "conditions": ["Hypertension", "GERD"]},
            {"type": "diagnostic", "label": "Rosa Mendez", "relation": "Mother", "conditions": ["Type 2 diabetes"]},
            {"type": "diagnostic", "label": "Elena Mendez", "relation": "Sister", "conditions": ["Asthma"]},
        ]
    },
    "BIO-20241112": {
        "name": "Aaliyah Jackson",
        "patientid": "BIO-20241112",
        "patientDOB": "April 7, 1990",
        "patient_history": [
            {"type": "diagnostic", "label": "Dermatology", "date": "Feb 2025", "items": ["Psoriasis stable on topical", "No joint symptoms", "Follow-up 6 months"]},
            {"type": "diagnostic", "label": "Rheumatology screening", "date": "Nov 2024", "items": ["No psoriatic arthritis", "CRP normal"]},
            {"type": "diagnostic", "label": "Annual physical", "date": "Apr 2024", "items": ["Routine labs normal", "Skin condition noted"]},
        ],
        "current_medications": [
            {"type": "diagnostic", "label": "Calcipotriene/Betamethasone", "conflicts": [], "items": ["Topical daily", "Plaque psoriasis"], "description": None},
            {"type": "diagnostic", "label": "Cetirizine", "conflicts": [], "items": ["10 mg PRN", "Seasonal allergies"], "description": None},
        ],
        "family_history": [
            {"type": "diagnostic", "label": "Derek Jackson", "relation": "Father", "conditions": ["Psoriasis", "Hypertension"]},
            {"type": "diagnostic", "label": "Michelle Jackson", "relation": "Mother", "conditions": ["Lupus", "Raynaud's"]},
        ]
    },
}

