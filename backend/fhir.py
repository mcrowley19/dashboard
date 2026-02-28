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