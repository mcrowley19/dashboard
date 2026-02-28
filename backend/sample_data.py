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
            "label": "Oscar Wilde",
            "relation": "Father",
            "conditions": ["Heart disease", "Cancer", "plague"],
        }
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
            "label": "Oscar Wilde",
            "relation": "Father",
            "conditions": ["Heart disease", "Cancer", "plague"],
        }
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
            "label": "Oscar Wilde",
            "relation": "Father",
            "conditions": ["Heart disease", "Cancer", "plague"],
        }
    ]
    }

}
