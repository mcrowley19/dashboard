import requests

BASE_URL = "https://www.iehr.ai/fhir/ie/core"
PATIENT_ID = "example-patient-id"

headers = {
    "Accept": "application/fhir+json"
}

url = f"{BASE_URL}/Patient/{PATIENT_ID}/$everything"
resp = requests.get(url, headers=headers)

if resp.status_code != 200:
    raise Exception(f"Failed to retrieve data: {resp.status_code}\n{resp.text}")

bundle = resp.json()

name = None
patientid = None
patientDOB = None
patient_history = []
current_medications = []
family_history = []


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
            # Use text if available
            med_text = med.get("text")
            if med_text:
                current_medications.append(med_text)
            else:
                # Try the first coding display
                for coding in med.get("coding", []):
                    if coding.get("display"):
                        current_medications.append(coding["display"])

    elif rtype == "FamilyMemberHistory":
        for cond in resource.get("condition", []):
            cond_code = cond.get("code", {})
            cond_text = cond_code.get("text")
            if cond_text:
                family_history.append(cond_text)
            else:
                for coding in cond_code.get("coding", []):
                    if coding.get("display"):
                        family_history.append(coding["display"])

print(resource)