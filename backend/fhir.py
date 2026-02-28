import requests


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