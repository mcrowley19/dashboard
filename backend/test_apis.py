#!/usr/bin/env python3
"""
Integration test suite for BioSync API.
Tests both the FastAPI endpoints and underlying FDA / Gemini clients.

Run locally:   python test_apis.py
Run vs Vercel: BASE_URL=https://your-app.vercel.app python test_apis.py
"""

import asyncio
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL    = os.getenv("BASE_URL", "http://localhost:8000")
PATIENT_ID  = "20240112"
DRUG_NAME   = "ibuprofen"
TIMEOUT     = 15.0

# ── Helpers ───────────────────────────────────────────────────────────────────

def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_json(data):
    print(json.dumps(data, indent=2)[:1200])

def ok(msg):  print(f"  ✓ {msg}")
def fail(msg): print(f"  ✗ {msg}")


# ── Tests ─────────────────────────────────────────────────────────────────────

async def test_health(client: httpx.AsyncClient) -> bool:
    print_header("Health Check")
    try:
        r = await client.get(f"{BASE_URL}/health")
        r.raise_for_status()
        ok(f"Status {r.status_code} — {r.json()}")
        return True
    except Exception as e:
        fail(f"Health check failed: {e}")
        return False


async def test_patient_info(client: httpx.AsyncClient) -> bool:
    print_header("Patient Info")
    try:
        r = await client.get(f"{BASE_URL}/patient/{PATIENT_ID}")
        r.raise_for_status()
        data = r.json()
        print_json(data)
        assert "name"       in data, "missing 'name'"
        assert "patientid"  in data, "missing 'patientid'"
        assert "patientDOB" in data, "missing 'patientDOB'"
        ok("Patient info shape is correct")
        return True
    except Exception as e:
        fail(f"Patient info failed: {e}")
        return False


async def test_patient_history(client: httpx.AsyncClient) -> bool:
    print_header("Patient History")
    try:
        r = await client.get(f"{BASE_URL}/patient/{PATIENT_ID}/history")
        r.raise_for_status()
        data = r.json()
        print_json(data)
        assert isinstance(data, list),    "expected a list"
        assert len(data) > 0,             "empty history"
        assert "label" in data[0],        "missing 'label'"
        assert "items" in data[0],        "missing 'items'"
        ok(f"Got {len(data)} history entry/entries")
        return True
    except Exception as e:
        fail(f"Patient history failed: {e}")
        return False


async def test_patient_medications(client: httpx.AsyncClient) -> bool:
    print_header("Current Medications")
    try:
        r = await client.get(f"{BASE_URL}/patient/{PATIENT_ID}/medications")
        r.raise_for_status()
        data = r.json()
        print_json(data)
        assert isinstance(data, list), "expected a list"
        assert "label" in data[0],     "missing 'label'"
        ok(f"Got {len(data)} medication(s): {[m['label'] for m in data]}")
        return True
    except Exception as e:
        fail(f"Medications failed: {e}")
        return False


async def test_contraindications(client: httpx.AsyncClient) -> bool:
    print_header("Potential Contraindications (FDA lookup)")
    try:
        r = await client.get(f"{BASE_URL}/patient/{PATIENT_ID}/contraindications", timeout=20.0)
        r.raise_for_status()
        data = r.json()
        print_json(data)
        assert isinstance(data, list), "expected a list"
        assert "label"    in data[0],  "missing 'label'"
        assert "severity" in data[0],  "missing 'severity'"
        assert "items"    in data[0],  "missing 'items'"
        ok(f"Got contraindications for: {[d['label'] for d in data]}")
        ok(f"Severities: {[d['severity'] for d in data]}")
        return True
    except Exception as e:
        fail(f"Contraindications failed: {e}")
        return False


async def test_ai_summary(client: httpx.AsyncClient) -> bool:
    print_header("AI Summary (Gemini)")
    payload = {
        "patient_name": "John Doe",
        "history": [
            {
                "label": "Went to Roscommon",
                "date": "Jan 2025",
                "items": ["Can cause you to want to do BESS", "Lunacy"],
            }
        ],
        "medications": [
            {
                "label": "Benzylpiperazine",
                "items": ["Lunacy", "Play gracefully with ideas"],
            }
        ],
    }
    try:
        r = await client.post(f"{BASE_URL}/patient/summary", json=payload, timeout=20.0)
        r.raise_for_status()
        data = r.json()
        print_json(data)
        assert isinstance(data, list),      "expected a list"
        assert "summary" in data[0],         "missing 'summary'"
        assert len(data[0]["summary"]) > 10, "summary too short"
        ok("AI summary generated successfully")
        print(f"\n  Summary: {data[0]['summary']}")
        return True
    except Exception as e:
        fail(f"AI summary failed: {e}")
        return False


async def test_drug_search(client: httpx.AsyncClient) -> bool:
    print_header("Drug Search (FDA passthrough)")
    try:
        r = await client.get(f"{BASE_URL}/drugs/search", params={"q": "aspirin"})
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        assert len(results) > 0, "no results"
        ok(f"Found {len(results)} result(s)")
        for res in results[:3]:
            brand = res.get("openfda", {}).get("brand_name", ["N/A"])[0]
            print(f"    • {brand}")
        return True
    except Exception as e:
        fail(f"Drug search failed: {e}")
        return False


async def test_drug_info(client: httpx.AsyncClient) -> bool:
    print_header(f"Drug Info — {DRUG_NAME}")
    try:
        r = await client.get(f"{BASE_URL}/drugs/{DRUG_NAME}", timeout=15.0)
        r.raise_for_status()
        data = r.json()

        print(f"  Brand:        {data['name']['brand']}")
        print(f"  Generic:      {data['name']['generic']}")
        print(f"  Manufacturer: {data['manufacturer']}")

        for field, label in [
            ("purpose",      "Purpose"),
            ("warnings",     "Warnings"),
            ("dosage",       "Dosage"),
            ("side_effects", "Side Effects"),
            ("interactions", "Interactions"),
            ("indications",  "Indications"),
        ]:
            value = data.get(field, ["N/A"])
            text  = value[0][:300] if value != ["N/A"] else "N/A"
            print(f"\n  ── {label} ──")
            print(f"  {text}...")

        ok("Drug info retrieved successfully")
        return True
    except Exception as e:
        fail(f"Drug info failed: {e}")
        return False


# ── Runner ────────────────────────────────────────────────────────────────────

async def run_all_tests():
    print(f"\n{'='*60}")
    print(f"  BioSync API Test Suite")
    print(f"  Target: {BASE_URL}")
    print(f"{'='*60}")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        tests = [
            ("Health Check",           test_health(client)),
            ("Patient Info",           test_patient_info(client)),
            ("Patient History",        test_patient_history(client)),
            ("Current Medications",    test_patient_medications(client)),
            ("Contraindications",      test_contraindications(client)),
            ("AI Summary",             test_ai_summary(client)),
            ("Drug Search",            test_drug_search(client)),
            ("Drug Info",              test_drug_info(client)),
        ]

        results = []
        for name, coro in tests:
            passed = await coro
            results.append((name, passed))

    print_header("Test Summary")
    passed_count = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {name}: {status}")

    print(f"\n  Total: {passed_count}/{total} tests passed")
    if passed_count == total:
        print("\n  🎉 All tests passed!")
    else:
        print(f"\n  ⚠️  {total - passed_count} test(s) failed")


if __name__ == "__main__":
    asyncio.run(run_all_tests())