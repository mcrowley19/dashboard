import requests

# Known FHIR patient IDs (from iehr.ai); used for patient list and to decide when to call FHIR.
FHIR_PATIENT_IDS = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]

# Static list for GET /patients dropdown (names/DOB from API docs). IDs must match FHIR server.
FHIR_PATIENT_LIST = [
    {"id": "001", "name": "Sean O'Brien", "dob": "1980-05-12"},
    {"id": "002", "name": "Mary Murphy", "dob": "1965-11-23"},
    {"id": "003", "name": "Conor Walsh", "dob": "1992-03-07"},
    {"id": "004", "name": "Margaret Kelly", "dob": "1955-08-19"},
    {"id": "005", "name": "Aoife Ryan", "dob": "2001-06-14"},
    {"id": "006", "name": "Declan Byrne", "dob": "1978-01-30"},
    {"id": "007", "name": "Sinead Doyle", "dob": "1988-09-05"},
    {"id": "008", "name": "Patrick Fitzgerald", "dob": "1945-12-02"},
    {"id": "009", "name": "Ciara Brennan", "dob": "1999-04-22"},
    {"id": "010", "name": "Brian O'Connor", "dob": "1970-07-16"},
]


def get_fhir_patient_list():
    """Returns the list of FHIR patients for the frontend (id, name, dob, initials)."""
    out = []
    for p in FHIR_PATIENT_LIST:
        name = p["name"]
        parts = name.strip().split()
        if len(parts) >= 2:
            initials = (parts[0][0] + parts[-1][0]).upper()
        else:
            initials = (parts[0][:2] if parts else "?").upper()
        out.append({"id": p["id"], "name": name, "dob": p["dob"], "initials": initials})
    return out


def get_patient_info(patient_id):
    BASE_URL = "https://www.iehr.ai/fhir/ie/core"

    headers = {
        "Accept": "application/fhir+json"
    }

    url = f"{BASE_URL}/Patient/{patient_id}/$everything"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise Exception(f"Failed to retrieve data: {resp.status_code}\n{resp.text}")

    bundle = resp.json()

    name = None
    patientid = None
    patientDOB = None
    patient_history = []
    current_medications = []
    family_history = []  # list of {relation, conditions} per FamilyMemberHistory resource

    for entry in bundle.get("entry", []):
        resource = entry.get("resource")
        if not resource:
            continue

        rtype = resource.get("resourceType")

        if rtype == "Patient":
            patientid = resource.get("id")
            patientDOB = resource.get("birthDate")
            if "name" in resource:
                name_data = resource["name"][0]
                given = " ".join(name_data.get("given", []))
                family = name_data.get("family", "")
                name = f"{given} {family}".strip()

        elif rtype == "Condition":
            code = resource.get("code", {})
            text_val = code.get("text")
            if text_val:
                patient_history.append(text_val)
            else:
                for coding in code.get("coding", []):
                    if coding.get("display"):
                        patient_history.append(coding["display"])

        elif rtype == "MedicationStatement":
            med = resource.get("medicationCodeableConcept")
            if med:
                med_text = med.get("text")
                if med_text:
                    current_medications.append(med_text)
                else:
                    for coding in med.get("coding", []):
                        if coding.get("display"):
                            current_medications.append(coding["display"])
                            break

        elif rtype == "FamilyMemberHistory":
            rel_coding = resource.get("relationship", {}).get("coding", [])
            relation = rel_coding[0].get("display", "Family member") if rel_coding else "Family member"
            conds = []
            for cond in resource.get("condition", []):
                cond_code = cond.get("code", {})
                cond_text = cond_code.get("text")
                if cond_text:
                    conds.append(cond_text)
                else:
                    for coding in cond_code.get("coding", []):
                        if coding.get("display"):
                            conds.append(coding["display"])
                            break
            family_history.append({"relation": relation, "conditions": conds})

    # Format for dashboard: same shape as sample_data / frontend expectations
    history_formatted = [
        {"type": "diagnostic", "label": c, "date": "", "items": []}
        for c in patient_history
    ]
    meds_formatted = [
        {"type": "diagnostic", "label": m, "conflicts": [], "items": [], "description": None}
        for m in current_medications
    ]
    family_formatted = [
        {"type": "diagnostic", "label": f["relation"], "relation": f["relation"], "conditions": f["conditions"]}
        for f in family_history
    ]

    return {
        "name": name or "Unknown",
        "patientid": patientid or patient_id,
        "patientDOB": patientDOB or "",
        "patient_history": history_formatted,
        "current_medications": meds_formatted,
        "family_history": family_formatted,
    }

    """"
    Sample responses from this API (10 patients)

    --- Patient 001: Sean O'Brien ---
    {
    "resourceType": "Bundle", "id": "bundle-001", "type": "searchset", "total": 5,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "001", "name": [{"use": "official", "family": "O'Brien", "given": ["Sean", "Patrick"]}], "gender": "male", "birthDate": "1980-05-12"}},
        {"resource": {"resourceType": "Condition", "id": "c001a", "subject": {"reference": "Patient/001"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Diabetes mellitus type 2"}], "text": "Type 2 Diabetes"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c001b", "subject": {"reference": "Patient/001"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}], "text": "Hypertension"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m001a", "subject": {"reference": "Patient/001"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 500mg Tablet"}], "text": "Metformin 500mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m001b", "subject": {"reference": "Patient/001"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "29046", "display": "Lisinopril 10mg Tablet"}], "text": "Lisinopril 10mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh001", "patient": {"reference": "Patient/001"}, "relationship": {"coding": [{"code": "FTH", "display": "Father"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "22298006", "display": "Myocardial infarction"}], "text": "Heart attack"}}]}}
    ]}

    --- Patient 002: Mary Murphy ---
    {
    "resourceType": "Bundle", "id": "bundle-002", "type": "searchset", "total": 7,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "002", "name": [{"use": "official", "family": "Murphy", "given": ["Mary"]}], "gender": "female", "birthDate": "1965-11-23"}},
        {"resource": {"resourceType": "Condition", "id": "c002a", "subject": {"reference": "Patient/002"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "40930008", "display": "Hypothyroidism"}], "text": "Hypothyroidism"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c002b", "subject": {"reference": "Patient/002"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "64859006", "display": "Osteoporosis"}], "text": "Osteoporosis"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c002c", "subject": {"reference": "Patient/002"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "197480006", "display": "Anxiety disorder"}], "text": "Generalised Anxiety Disorder"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m002a", "subject": {"reference": "Patient/002"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "10582", "display": "Levothyroxine 50mcg Tablet"}], "text": "Levothyroxine 50mcg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m002b", "subject": {"reference": "Patient/002"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "77492", "display": "Alendronate 70mg Tablet"}], "text": "Alendronate 70mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m002c", "subject": {"reference": "Patient/002"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "36437", "display": "Sertraline 50mg Tablet"}], "text": "Sertraline 50mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh002", "patient": {"reference": "Patient/002"}, "relationship": {"coding": [{"code": "MTH", "display": "Mother"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "254837009", "display": "Breast cancer"}], "text": "Breast cancer"}}]}}
    ]}

    --- Patient 003: Conor Walsh ---
    {
    "resourceType": "Bundle", "id": "bundle-003", "type": "searchset", "total": 4,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "003", "name": [{"use": "official", "family": "Walsh", "given": ["Conor"]}], "gender": "male", "birthDate": "1992-03-07"}},
        {"resource": {"resourceType": "Condition", "id": "c003a", "subject": {"reference": "Patient/003"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "195967001", "display": "Asthma"}], "text": "Asthma"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m003a", "subject": {"reference": "Patient/003"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "745679", "display": "Salbutamol 100mcg Inhaler"}], "text": "Salbutamol 100mcg Inhaler"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m003b", "subject": {"reference": "Patient/003"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "746763", "display": "Fluticasone 250mcg Inhaler"}], "text": "Fluticasone 250mcg Inhaler"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh003", "patient": {"reference": "Patient/003"}, "relationship": {"coding": [{"code": "MTH", "display": "Mother"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "195967001", "display": "Asthma"}], "text": "Asthma"}}]}}
    ]}

    --- Patient 004: Margaret Kelly ---
    {
    "resourceType": "Bundle", "id": "bundle-004", "type": "searchset", "total": 9,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "004", "name": [{"use": "official", "family": "Kelly", "given": ["Margaret", "Anne"]}], "gender": "female", "birthDate": "1955-08-19"}},
        {"resource": {"resourceType": "Condition", "id": "c004a", "subject": {"reference": "Patient/004"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "49436004", "display": "Atrial fibrillation"}], "text": "Atrial Fibrillation"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c004b", "subject": {"reference": "Patient/004"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "433144002", "display": "Chronic kidney disease stage 3"}], "text": "Chronic Kidney Disease Stage 3"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c004c", "subject": {"reference": "Patient/004"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Diabetes mellitus type 2"}], "text": "Type 2 Diabetes"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c004d", "subject": {"reference": "Patient/004"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "84114007", "display": "Heart failure"}], "text": "Heart Failure"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m004a", "subject": {"reference": "Patient/004"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1364430", "display": "Apixaban 5mg Tablet"}], "text": "Apixaban 5mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m004b", "subject": {"reference": "Patient/004"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "854901", "display": "Bisoprolol 2.5mg Tablet"}], "text": "Bisoprolol 2.5mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m004c", "subject": {"reference": "Patient/004"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "4603", "display": "Furosemide 40mg Tablet"}], "text": "Furosemide 40mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m004d", "subject": {"reference": "Patient/004"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 500mg Tablet"}], "text": "Metformin 500mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh004", "patient": {"reference": "Patient/004"}, "relationship": {"coding": [{"code": "FTH", "display": "Father"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "230690007", "display": "Stroke"}], "text": "Stroke"}}, {"code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Diabetes mellitus type 2"}], "text": "Type 2 Diabetes"}}]}}
    ]}

    --- Patient 005: Aoife Ryan ---
    {
    "resourceType": "Bundle", "id": "bundle-005", "type": "searchset", "total": 5,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "005", "name": [{"use": "official", "family": "Ryan", "given": ["Aoife"]}], "gender": "female", "birthDate": "2001-06-14"}},
        {"resource": {"resourceType": "Condition", "id": "c005a", "subject": {"reference": "Patient/005"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "34000006", "display": "Crohn's disease"}], "text": "Crohn's Disease"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c005b", "subject": {"reference": "Patient/005"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "87522002", "display": "Iron deficiency anaemia"}], "text": "Iron Deficiency Anaemia"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m005a", "subject": {"reference": "Patient/005"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1311", "display": "Azathioprine 50mg Tablet"}], "text": "Azathioprine 50mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m005b", "subject": {"reference": "Patient/005"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "4495", "display": "Ferrous Sulphate 200mg Tablet"}], "text": "Ferrous Sulphate 200mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m005c", "subject": {"reference": "Patient/005"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "41493", "display": "Mesalazine 800mg Tablet"}], "text": "Mesalazine 800mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh005", "patient": {"reference": "Patient/005"}, "relationship": {"coding": [{"code": "MTH", "display": "Mother"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "363346000", "display": "Colorectal cancer"}], "text": "Colorectal cancer"}}]}}
    ]}

    --- Patient 006: Declan Byrne ---
    {
    "resourceType": "Bundle", "id": "bundle-006", "type": "searchset", "total": 6,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "006", "name": [{"use": "official", "family": "Byrne", "given": ["Declan"]}], "gender": "male", "birthDate": "1978-01-30"}},
        {"resource": {"resourceType": "Condition", "id": "c006a", "subject": {"reference": "Patient/006"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}], "text": "Hypertension"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c006b", "subject": {"reference": "Patient/006"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "13644009", "display": "Hypercholesterolaemia"}], "text": "Hypercholesterolaemia"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c006c", "subject": {"reference": "Patient/006"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "414916001", "display": "Obesity"}], "text": "Obesity"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m006a", "subject": {"reference": "Patient/006"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "17767", "display": "Amlodipine 5mg Tablet"}], "text": "Amlodipine 5mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m006b", "subject": {"reference": "Patient/006"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "83367", "display": "Atorvastatin 40mg Tablet"}], "text": "Atorvastatin 40mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh006", "patient": {"reference": "Patient/006"}, "relationship": {"coding": [{"code": "FTH", "display": "Father"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "22298006", "display": "Myocardial infarction"}], "text": "Myocardial Infarction"}}, {"code": {"coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}], "text": "Hypertension"}}]}}
    ]}

    --- Patient 007: Sinead Doyle ---
    {
    "resourceType": "Bundle", "id": "bundle-007", "type": "searchset", "total": 6,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "007", "name": [{"use": "official", "family": "Doyle", "given": ["Sinead"]}], "gender": "female", "birthDate": "1988-09-05"}},
        {"resource": {"resourceType": "Condition", "id": "c007a", "subject": {"reference": "Patient/007"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "69896004", "display": "Rheumatoid arthritis"}], "text": "Rheumatoid Arthritis"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c007b", "subject": {"reference": "Patient/007"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "35489007", "display": "Depression"}], "text": "Depression"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m007a", "subject": {"reference": "Patient/007"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "8542", "display": "Methotrexate 10mg Tablet"}], "text": "Methotrexate 10mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m007b", "subject": {"reference": "Patient/007"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "4481", "display": "Folic Acid 5mg Tablet"}], "text": "Folic Acid 5mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m007c", "subject": {"reference": "Patient/007"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "321988", "display": "Escitalopram 10mg Tablet"}], "text": "Escitalopram 10mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh007", "patient": {"reference": "Patient/007"}, "relationship": {"coding": [{"code": "MTH", "display": "Mother"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "69896004", "display": "Rheumatoid arthritis"}], "text": "Rheumatoid Arthritis"}}]}}
    ]}

    --- Patient 008: Patrick Fitzgerald ---
    {
    "resourceType": "Bundle", "id": "bundle-008", "type": "searchset", "total": 9,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "008", "name": [{"use": "official", "family": "Fitzgerald", "given": ["Patrick", "Joseph"]}], "gender": "male", "birthDate": "1945-12-02"}},
        {"resource": {"resourceType": "Condition", "id": "c008a", "subject": {"reference": "Patient/008"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "13645005", "display": "Chronic obstructive pulmonary disease"}], "text": "Chronic Obstructive Pulmonary Disease"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c008b", "subject": {"reference": "Patient/008"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "414545008", "display": "Ischaemic heart disease"}], "text": "Ischaemic Heart Disease"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c008c", "subject": {"reference": "Patient/008"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Diabetes mellitus type 2"}], "text": "Type 2 Diabetes"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c008d", "subject": {"reference": "Patient/008"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "399957001", "display": "Peripheral arterial disease"}], "text": "Peripheral Arterial Disease"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m008a", "subject": {"reference": "Patient/008"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "237661", "display": "Tiotropium 18mcg Inhaler"}], "text": "Tiotropium 18mcg Inhaler"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m008b", "subject": {"reference": "Patient/008"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1191", "display": "Aspirin 75mg Tablet"}], "text": "Aspirin 75mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m008c", "subject": {"reference": "Patient/008"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "83367", "display": "Atorvastatin 80mg Tablet"}], "text": "Atorvastatin 80mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m008d", "subject": {"reference": "Patient/008"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "274783", "display": "Insulin Glargine 100units/ml Injection"}], "text": "Insulin Glargine 100units/ml Injection"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh008", "patient": {"reference": "Patient/008"}, "relationship": {"coding": [{"code": "FTH", "display": "Father"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "363358000", "display": "Lung cancer"}], "text": "Lung cancer"}}, {"code": {"coding": [{"system": "http://snomed.info/sct", "code": "230690007", "display": "Stroke"}], "text": "Stroke"}}]}}
    ]}

    --- Patient 009: Ciara Brennan ---
    {
    "resourceType": "Bundle", "id": "bundle-009", "type": "searchset", "total": 5,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "009", "name": [{"use": "official", "family": "Brennan", "given": ["Ciara"]}], "gender": "female", "birthDate": "1999-04-22"}},
        {"resource": {"resourceType": "Condition", "id": "c009a", "subject": {"reference": "Patient/009"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "46635009", "display": "Diabetes mellitus type 1"}], "text": "Type 1 Diabetes"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c009b", "subject": {"reference": "Patient/009"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "396331005", "display": "Coeliac disease"}], "text": "Coeliac Disease"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m009a", "subject": {"reference": "Patient/009"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "1157459", "display": "Insulin Aspart 100units/ml Injection"}], "text": "Insulin Aspart 100units/ml Injection"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m009b", "subject": {"reference": "Patient/009"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "274783", "display": "Insulin Glargine 100units/ml Injection"}], "text": "Insulin Glargine 100units/ml Injection"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh009", "patient": {"reference": "Patient/009"}, "relationship": {"coding": [{"code": "MTH", "display": "Mother"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "46635009", "display": "Diabetes mellitus type 1"}], "text": "Type 1 Diabetes"}}]}}
    ]}

    --- Patient 010: Brian O'Connor ---
    {
    "resourceType": "Bundle", "id": "bundle-010", "type": "searchset", "total": 7,
    "entry": [
        {"resource": {"resourceType": "Patient", "id": "010", "name": [{"use": "official", "family": "O'Connor", "given": ["Brian"]}], "gender": "male", "birthDate": "1970-07-16"}},
        {"resource": {"resourceType": "Condition", "id": "c010a", "subject": {"reference": "Patient/010"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "84757009", "display": "Epilepsy"}], "text": "Epilepsy"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c010b", "subject": {"reference": "Patient/010"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "37796009", "display": "Migraine"}], "text": "Migraine"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "Condition", "id": "c010c", "subject": {"reference": "Patient/010"}, "code": {"coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}], "text": "Hypertension"}, "clinicalStatus": {"coding": [{"code": "active"}]}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m010a", "subject": {"reference": "Patient/010"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "357222", "display": "Levetiracetam 500mg Tablet"}], "text": "Levetiracetam 500mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m010b", "subject": {"reference": "Patient/010"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "38404", "display": "Topiramate 25mg Tablet"}], "text": "Topiramate 25mg Tablet"}}},
        {"resource": {"resourceType": "MedicationStatement", "id": "m010c", "subject": {"reference": "Patient/010"}, "status": "active", "medicationCodeableConcept": {"coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "35296", "display": "Ramipril 5mg Tablet"}], "text": "Ramipril 5mg Tablet"}}},
        {"resource": {"resourceType": "FamilyMemberHistory", "id": "fh010", "patient": {"reference": "Patient/010"}, "relationship": {"coding": [{"code": "FTH", "display": "Father"}]}, "condition": [{"code": {"coding": [{"system": "http://snomed.info/sct", "code": "84757009", "display": "Epilepsy"}], "text": "Epilepsy"}}, {"code": {"coding": [{"system": "http://snomed.info/sct", "code": "38341003", "display": "Hypertension"}], "text": "Hypertension"}}]}}
    ]}
    """