from dotenv import load_dotenv
import os

# Load backend/.env before any module that uses GEMINI_API_KEY (e.g. gemini)
_load_env = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(_load_env)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openfda import search_drugs, get_drug_info
from gemini import generate_text

app = FastAPI(
    title="Metricare API",
    description="Backend API for Metricare patient dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class SummaryRequest(BaseModel):
    patient_name: str
    history: list[dict]
    medications: list[dict]
    family_history: list[dict] = []
    contraindications: list[dict] = []



@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    """
    Returns basic patient info.
    In production, replace this with a real DB lookup.
    """
    # Stub — swap in DB query here
    return {
        "name": "John Doe",
        "patientid": f"BIO-{patient_id}",
        "patientDOB": "Jan 12, 1984",
    }



@app.get("/patient/{patient_id}/history")
def get_patient_history(patient_id: str):
    """
    Returns the patient's clinical history entries.
    Shape matches the HISTORY const the frontend expects.
    """
    # Stub — swap in DB query here
    return [
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
    ]



@app.get("/patient/{patient_id}/medications")
def get_patient_medications(patient_id: str):
    """
    Returns the patient's current medications.
    Shape matches the MEDICATIONS const the frontend expects.
    Uses drug names that exist in OpenFDA for lookups (e.g. contraindications).
    TODO: Populate `description` from OpenFDA drug label (purpose/indications) when implemented.
    """
    # Stub — swap in DB query here. Labels use OpenFDA-recognized names (brand or generic).
    return [
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
    ]




@app.get("/patient/{patient_id}/family_history")
def get_patient_family_history(patient_id: str):
    """
    Returns the patient's family history (relatives and conditions).
    Shape matches the FAMILY_HISTORY const the frontend expects.
    """
    # Stub — swap in DB query here
    return [
        {
            "type": "diagnostic",
            "label": "Oscar Wilde",
            "relation": "Father",
            "conditions": ["Heart disease", "Cancer", "plague"],
        }
    ]




@app.get("/patient/{patient_id}/contraindications")
async def get_contraindications(patient_id: str):
    """
    Pulls the patient's medications, looks up each one in the OpenFDA API,
    and returns potential contraindications with severity.
    Shape matches the INTERACTIONS const the frontend expects.
    TODO: Populate `description` per drug from OpenFDA (e.g. warnings summary) when implemented.
    """
    medications = get_patient_medications(patient_id)

    results = []
    for med in medications:
        drug_name = med["label"]
        info = await get_drug_info(drug_name)

        if "error" in info:
            results.append({
                "type": "diagnostic",
                "label": drug_name,
                "severity": "UNKNOWN",
                "items": ["No FDA data available for this drug."],
                # TODO(OpenFDA): description = openfda.get_contraindication_description(drug_name)
                "description": None,
            })
            continue

        interactions = info.get("interactions", ["N/A"])
        warnings     = info.get("warnings", ["N/A"])

        warning_text = " ".join(warnings).lower()
        if any(w in warning_text for w in ["death", "fatal", "severe", "life-threatening"]):
            severity = "SEVERE"
        elif any(w in warning_text for w in ["caution", "avoid", "risk", "monitor"]):
            severity = "MODERATE"
        else:
            severity = "LOW"

        items = interactions if interactions != ["N/A"] else warnings
        items = [i[:200] for i in items]

        results.append({
            "type": "diagnostic",
            "label": drug_name,
            "severity": severity,
            "items": items,
            # TODO(OpenFDA): description = brief summary from warnings/interactions for this drug
            "description": None,
        })

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