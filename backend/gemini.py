import os
import json
import re
import google.generativeai as genai
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configure only when key is set (avoids crashes in serverless when env is missing)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 2.5 Flash (override with GEMINI_MODEL env if needed)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def generate_text(prompt: str, temperature: float = 0.7) -> str:
    """
    Generate text using Gemini API

    Args:
        prompt: The input prompt for text generation
        temperature: Controls randomness (0.0 to 1.0)

    Returns:
        Generated text response
    """
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Set GEMINI_API_KEY in environment."
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    if not response.text:
        return "No summary generated."
    return response.text


def filter_contraindications(
    patient_name: str,
    medication_names: list[str],
    history_text: str,
    family_text: str,
    raw_results: list[dict],
) -> list[dict]:
    """
    Uses Gemini to filter raw FDA contraindication results to only those relevant
    for this patient (e.g. drug–drug only if they take both; condition/pregnancy
    only if context suggests). Returns the filtered list; on failure returns raw_results.
    """
    if not raw_results or not GEMINI_API_KEY:
        return raw_results

    entries_text = "\n".join(
        f"[{i}] {r.get('label', '')} ({r.get('severity', '')}): "
        + "; ".join((r.get("items") or [])[:2])
        for i, r in enumerate(raw_results)
    )

    prompt = f"""You are a clinical assistant. Given this patient context and a list of potential contraindications/warnings from FDA labels, output ONLY the zero-based indices of entries that are RELEVANT for this patient. Omit entries that do not apply (e.g. drug-drug interaction when the patient does not take both drugs; pregnancy warning when not relevant; unrelated conditions).

Patient: {patient_name}
Medications they take: {", ".join(medication_names)}

Clinical history (summary):
{history_text or "(none)"}

Family history:
{family_text or "(none)"}

FDA contraindication/warning entries (each line is [index] drug (severity): summary):
{entries_text}

Reply with a JSON array of indices to KEEP, e.g. [0, 2, 4]. If none are relevant, reply []. No other text."""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        json_match = re.search(r"\[[\d,\s]*\]", text)
        if json_match:
            indices = json.loads(json_match.group())
            if isinstance(indices, list) and all(isinstance(i, int) for i in indices):
                return [raw_results[i] for i in indices if 0 <= i < len(raw_results)]
    except Exception:
        pass
    return raw_results


def summarize_contraindications_for_display(
    patient_name: str,
    medication_names: list[str],
    history_text: str,
    family_text: str,
    filtered_results: list[dict],
) -> list[dict]:
    """
    Uses Gemini to turn raw FDA contraindication text into short, doctor-friendly
    summaries per drug: either one sentence saying no significant risks, or a clear
    outline of the actual risks that apply to this patient.
    """
    if not filtered_results or not GEMINI_API_KEY:
        return filtered_results

    # Build context for each entry
    entries_desc = []
    for i, r in enumerate(filtered_results):
        raw_items = r.get("items") or []
        raw_blob = " ".join(raw_items)[:1500]
        entries_desc.append(f"[{i}] {r.get('label', '')} (severity: {r.get('severity', '')})\nRaw FDA text: {raw_blob}")

    prompt = f"""You are a clinical assistant. For each drug below, based on the patient's medications and the raw FDA text, output a doctor-friendly summary AND a severity level.

Patient: {patient_name}
Medications: {", ".join(medication_names)}

Clinical history:
{history_text or "(none)"}

Family history:
{family_text or "(none)"}

Drug entries (index, label, raw FDA text):
{chr(10).join(entries_desc)}

Rules:
- If there are NO relevant interaction or contraindication risks for this patient, output for that drug a single sentence: "No significant drug interaction risks for this patient." and set severity to "LOW".
- If there ARE relevant risks, output 1–4 short, clear bullet points outlining them (e.g. "Grapefruit juice may increase drug levels; avoid or limit." "Monitor for muscle pain if taken with gemfibrozil."). Do NOT repeat the FDA boilerplate like "7 DRUG INTERACTIONS See full prescribing information"; only state the actual risks in plain language.
- Severity must be one of: "SEVERE" (life-threatening, fatal, or contraindicated risks), "MODERATE" (risks requiring monitoring or dose adjustment), "LOW" (minor or no relevant risks).

Reply with a JSON object keyed by index (e.g. "0", "1") where each value has "severity" (string) and "items" (array of 1–4 strings). Example:
{{"0": {{"severity": "LOW", "items": ["No significant drug interaction risks for this patient."]}}, "1": {{"severity": "MODERATE", "items": ["Avoid grapefruit juice (increases drug levels).", "Monitor for myopathy if taken with gemfibrozil."]}}}}
No other text."""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        if "```" in text:
            for part in text.split("```"):
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    text = part
                    break
        parsed = json.loads(text)
        valid_severities = {"SEVERE", "MODERATE", "LOW"}
        if isinstance(parsed, dict):
            out = []
            for i, r in enumerate(filtered_results):
                key = str(i)
                entry = parsed.get(key)
                if isinstance(entry, dict):
                    new_items = entry.get("items")
                    new_severity = entry.get("severity", "").upper()
                    if not isinstance(new_items, list) or not all(isinstance(s, str) for s in new_items):
                        new_items = ["No significant drug interaction risks for this patient."]
                    if new_severity not in valid_severities:
                        new_severity = r.get("severity", "LOW")
                    out.append({**r, "items": new_items, "severity": new_severity})
                else:
                    out.append({**r, "items": ["No significant drug interaction risks for this patient."], "severity": new_severity})
            return out
    except (json.JSONDecodeError, Exception):
        pass
    # Fallback: replace items with a single generic line so we don't show raw FDA boilerplate
    return [
        {
            **r,
            "items": ["Review full prescribing information for details."]
            if (r.get("items") and len(" ".join(r.get("items", []))) > 100)
            else (r.get("items") or ["No summary available."]),
        }
        for r in filtered_results
    ]


async def chat(message: str, conversation_history: Optional[list] = None) -> str:
    """
    Chat with Gemini API

    Args:
        message: User message
        conversation_history: Optional list of previous messages

    Returns:
        Gemini's response
    """
    model = genai.GenerativeModel(GEMINI_MODEL)
    chat_session = model.start_chat(history=conversation_history or [])
    response = chat_session.send_message(message)
    return response.text or ""
