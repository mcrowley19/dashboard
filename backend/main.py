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
    title="ClearVault API",
    description="Backend API for ClearVault patient dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ────────────────────────────────────────────────

class SummaryRequest(BaseModel):
    patient_name: str
    history: list[dict]
    medications: list[dict]

class DrugInfoRequest(BaseModel):
    drug_name: str


# ─── Patient ──────────────────────────────────────────────────────────────────

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


# ─── Patient History ──────────────────────────────────────────────────────────

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
            "label": "Went to Roscommon",
            "date": "Jan 2025",
            "items": [
                "Can cause you to want to do BESS",
                "Lunacy",
                "Play gracefully with ideas",
            ],
        }
    ]


# ─── Medications ──────────────────────────────────────────────────────────────

@app.get("/patient/{patient_id}/medications")
def get_patient_medications(patient_id: str):
    """
    Returns the patient's current medications.
    Shape matches the MEDICATIONS const the frontend expects.
    """
    # Stub — swap in DB query here
    return [
        {
            "type": "diagnostic",
            "label": "Benzylpiperazine",
            "conflicts": [],
            "items": [
                "Can cause you to want to do BESS",
                "Lunacy",
                "Play gracefully with ideas",
            ],
        }
    ]


# ─── Contraindications ────────────────────────────────────────────────────────

@app.get("/patient/{patient_id}/contraindications")
async def get_contraindications(patient_id: str):
    """
    Pulls the patient's medications, looks up each one in the FDA API,
    and returns potential contraindications with severity.
    Shape matches the INTERACTIONS const the frontend expects.
    """
    # Get this patient's medications (reuse stub above for now)
    medications = get_patient_medications(patient_id)

    results = []
    for med in medications:
        drug_name = med["label"]
        info = await get_drug_info(drug_name)

        if "error" in info:
            # Drug not found in FDA — still return it, no interactions listed
            results.append({
                "type": "diagnostic",
                "label": drug_name,
                "severity": "UNKNOWN",
                "items": ["No FDA data available for this drug."],
            })
            continue

        interactions = info.get("interactions", ["N/A"])
        warnings     = info.get("warnings", ["N/A"])

        # Determine severity based on whether warnings mention key terms
        warning_text = " ".join(warnings).lower()
        if any(w in warning_text for w in ["death", "fatal", "severe", "life-threatening"]):
            severity = "SEVERE"
        elif any(w in warning_text for w in ["caution", "avoid", "risk", "monitor"]):
            severity = "MODERATE"
        else:
            severity = "LOW"

        items = interactions if interactions != ["N/A"] else warnings
        # Truncate each item so the UI doesn't overflow
        items = [i[:200] for i in items]

        results.append({
            "type": "diagnostic",
            "label": drug_name,
            "severity": severity,
            "items": items,
        })

    return results


# ─── AI Summary ───────────────────────────────────────────────────────────────

import asyncio

@app.post("/patient/summary")
async def generate_patient_summary(request: SummaryRequest):
    """
    Sends patient history + medications to Gemini and returns an AI summary.
    Shape matches the SUMMARY const the frontend expects.
    """
    history_text = "\n".join(
        f"- {h['label']} ({h.get('date', '')}): {', '.join(h.get('items', []))}"
        for h in request.history
    )
    meds_text = "\n".join(
        f"- {m['label']}: {', '.join(m.get('items', []))}"
        for m in request.medications
    )

    prompt = f"""You are a clinical assistant. Summarise the following patient data concisely 
in 2-3 sentences for a doctor. Do not add disclaimers.

Patient: {request.patient_name}

History:
{history_text}

Current Medications:
{meds_text}
"""

    try:
        # Run blocking Gemini call in a thread so the event loop stays responsive
        summary = await asyncio.to_thread(generate_text, prompt, 0.3)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")

    return [{"type": "diagnostic", "summary": summary}]


# ─── Drug Search (direct FDA passthrough) ─────────────────────────────────────

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


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "ClearVault API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


# ─── Vercel serverless handler ────────────────────────────────────────────────
from mangum import Mangum
handler = Mangum(app)