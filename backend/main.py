from dotenv import load_dotenv
import os
import requests

# Load backend/.env before any module that uses GEMINI_API_KEY e.g. gemini
_load_env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(_load_env):
    load_dotenv(_load_env)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openfda import search_drugs, get_drug_info
from gemini import generate_text, filter_contraindications, summarize_contraindications_for_display
from sample_data import sample_data
from fhir import (
    FHIR_PATIENT_IDS,
    get_fhir_patient_list,
    get_patient_info as fhir_get_patient_info,
)




app = FastAPI(
    title="Metricare API",
    description="Backend API for Metricare patient dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class SummaryRequest(BaseModel):
    patient_name: str
    history: list[dict]
    medications: list[dict]
    family_history: list[dict] = []
    contraindications: list[dict] = []


def _initials(name: str) -> str:
    parts = (name or "").strip().split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return (parts[0][:2] or "?").upper()
    return (parts[0][0] + parts[-1][0]).upper()


@app.get("/patients")
def list_patients():
    """Returns patients from sample_data and from FHIR (fhir.py) for the frontend."""
    out = []
    for pid, p in sample_data.items():
        name = p.get("name") or "Unknown"
        dob = p.get("patientDOB") or ""
        out.append({"id": pid, "name": name, "dob": dob, "initials": _initials(name)})
    out.extend(get_fhir_patient_list())
    def _sort_key(item):
        i = item["id"]
        if i.isdigit():
            return (0, int(i))
        return (1, i)
    out.sort(key=_sort_key)
    return out


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    """Returns basic patient info from sample_data or FHIR when available; otherwise stub."""
    if patient_id in FHIR_PATIENT_IDS:
        try:
            p = fhir_get_patient_info(patient_id)
            return {
                "name": p.get("name", "Unknown"),
                "patientid": p.get("patientid", patient_id),
                "patientDOB": p.get("patientDOB", ""),
            }
        except Exception:
            return {"name": "Unknown", "patientid": patient_id, "patientDOB": ""}
    if patient_id in sample_data:
        p = sample_data[patient_id]
        return {
            "name": p.get("name", "Unknown"),
            "patientid": p.get("patientid", patient_id),
            "patientDOB": p.get("patientDOB", ""),
        }
    return {"name": "Unknown", "patientid": patient_id, "patientDOB": ""}



@app.get("/patient/{patient_id}/history")
def get_patient_history(patient_id: str):
    """Returns the patient's clinical history from sample_data or FHIR when available."""
    if patient_id in FHIR_PATIENT_IDS:
        try:
            p = fhir_get_patient_info(patient_id)
            return p.get("patient_history", [])
        except Exception:
            return []
    if patient_id in sample_data:
        return sample_data[patient_id].get("patient_history", [])
    return []



@app.get("/patient/{patient_id}/medications")
def get_patient_medications(patient_id: str):
    """Returns the patient's current medications from sample_data or FHIR when available."""
    if patient_id in FHIR_PATIENT_IDS:
        try:
            p = fhir_get_patient_info(patient_id)
            return p.get("current_medications", [])
        except Exception:
            return []
    if patient_id in sample_data:
        return sample_data[patient_id].get("current_medications", [])
    return []




@app.get("/patient/{patient_id}/family_history")
def get_patient_family_history(patient_id: str):
    """Returns the patient's family history from sample_data or FHIR when available."""
    if patient_id in FHIR_PATIENT_IDS:
        try:
            p = fhir_get_patient_info(patient_id)
            return p.get("family_history", [])
        except Exception:
            return []
    if patient_id in sample_data:
        return sample_data[patient_id].get("family_history", [])
    return []




@app.get("/patient/{patient_id}/contraindications")
async def get_contraindications(patient_id: str):
    """
    Pulls the patient's medications, looks up each one in the OpenFDA API,
    then uses Gemini to return only contraindications relevant for this patient.
    Shape matches the INTERACTIONS const the frontend expects.
    """
    patient = get_patient(patient_id)
    medications = get_patient_medications(patient_id)
    history = get_patient_history(patient_id)
    family = get_patient_family_history(patient_id)

    history_text = "\n".join(
        f"- {h.get('label', '')} ({h.get('date', '')}): {', '.join(h.get('items', []))}"
        for h in history
    )
    family_text = "\n".join(
        f"- {f.get('label', '')} ({f.get('relation', '')}): {', '.join(f.get('conditions', []))}"
        for f in family
    )
    medication_names = [m["label"] for m in medications]

    raw_results = []
    for med in medications:
        drug_name = med["label"]
        info = await get_drug_info(drug_name)

        if "error" in info:
            raw_results.append({
                "type": "diagnostic",
                "label": drug_name,
                "severity": "UNKNOWN",
                "items": ["No FDA data available for this drug."],
                "description": None,
            })
            continue

        interactions = info.get("interactions", ["N/A"])
        warnings = info.get("warnings", ["N/A"])

        warning_text = " ".join(warnings).lower()
        if any(w in warning_text for w in ["death", "fatal", "severe", "life-threatening"]):
            severity = "SEVERE"
        elif any(w in warning_text for w in ["caution", "avoid", "risk", "monitor"]):
            severity = "MODERATE"
        else:
            severity = "LOW"

        items = interactions if interactions != ["N/A"] else warnings
        items = [i[:200] for i in items]

        raw_results.append({
            "type": "diagnostic",
            "label": drug_name,
            "severity": severity,
            "items": items,
            "description": None,
        })

    try:
        results = await asyncio.to_thread(
            filter_contraindications,
            patient["name"],
            medication_names,
            history_text,
            family_text,
            raw_results,
        )
        results = await asyncio.to_thread(
            summarize_contraindications_for_display,
            patient["name"],
            medication_names,
            history_text,
            family_text,
            results,
        )
    except Exception:
        results = raw_results

    return results




import asyncio
from datetime import datetime, timezone

@app.post("/patient/summary")
async def generate_patient_summary(request: SummaryRequest):
    """
    Sends patient history, medications, family history, and contraindications
    to Gemini and returns an AI summary that considers all of these.
    Identifies follow-ups/visits due now and returns them bolded (**text**) in the summary.
    Shape matches the SUMMARY const the frontend expects.
    """
    now = datetime.now(timezone.utc)
    current_date_time = now.strftime("%B %d, %Y")  # e.g. February 28, 2025
    current_date_iso = now.strftime("%Y-%m-%d")    # for unambiguous parsing

    history_text = "\n".join(
        f"- {h['label']} ({h.get('date', '')}): {', '.join(h.get('items', []))}"
        for h in request.history
    )
    meds_text = "\n".join(
        f"- {m['label']}: {', '.join(m.get('items', []))}"
        for m in request.medications
    )
    family_text = "\n".join(
        f"- {f.get('label', '')} ({f.get('relation', '')}): {', '.join(f.get('conditions', []))}"
        for f in request.family_history
    )
    contra_text = "\n".join(
        f"- {c.get('label', '')} [{c.get('severity', '')}]: {', '.join(c.get('items', []))}"
        for c in request.contraindications
    )

    prompt = f"""You are a clinical assistant. Today's date and time (use this to decide what is "due now"): {current_date_time} (ISO {current_date_iso}).

Summarise the following patient data in 2-4 sentences for a doctor. Take into account their clinical history, current medications, family history, and any potential contraindications or drug interactions. Highlight anything that may need attention (e.g. family risk factors, severe/moderate contraindications).

IMPORTANT - Due/overdue follow-ups: From the clinical history, identify any follow-up, check-up, or next visit that is DUE NOW or OVERDUE based on today's date. Always state how much time overdue when relevant (e.g. "1 week overdue", "2 months overdue").
- For items that are due now or only slightly overdue (e.g. under 1 month), wrap the phrase in double asterisks: **Hypertension follow-up is due now** or **Annual physical is 2 weeks overdue**.
- For items that are SEVERELY overdue (e.g. more than 1 month past due), wrap the phrase in TRIPLE asterisks and include how overdue: ***Cardiology follow-up is 3 months overdue***. Use *** only for severely overdue items so they appear red and bold.
Use ** or *** only for these due/overdue items. Do not add disclaimers.

Patient: {request.patient_name}

Clinical History:
{history_text or "(none)"}

Current Medications:
{meds_text or "(none)"}

Family History:
{family_text or "(none)"}

Potential Contraindications / Interactions:
{contra_text or "(none)"}
"""

    try:
        # Run blocking Gemini call in a thread so the event loop stays responsive
        summary = await asyncio.to_thread(generate_text, prompt, 0.3)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")

    return [{"type": "diagnostic", "summary": summary}]




@app.get("/drugs/search")
async def drugs_search(q: str):
    """Search FDA for drugs by brand name."""
    return await search_drugs(q)


@app.get("/drugs/{drug_name}")
async def drug_info(drug_name: str):
    """Get full FDA info for a specific drug."""
    info = await get_drug_info(drug_name)
    if "error" in info:
        raise HTTPException(status_code=404, detail=info["error"])
    return info




@app.get("/")
def root():
    return {"message": "Metricare API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}



from mangum import Mangum
handler = Mangum(app)