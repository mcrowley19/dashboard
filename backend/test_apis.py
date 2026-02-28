#!/usr/bin/env python3
"""
Test script for FDA API
Run with: python test_apis.py
"""

import asyncio
import json
from dotenv import load_dotenv
from openfda import search_drugs, get_drug_info

load_dotenv()


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_field(label: str, value, max_chars: int = 400):
    """Pretty print a single drug info field."""
    print(f"\n  {'─'*56}")
    print(f"  {label.upper()}")
    print(f"  {'─'*56}")
    if isinstance(value, list):
        for item in value:
            text = str(item).strip()
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            print(f"  {text}")
    else:
        text = str(value).strip()
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        print(f"  {text}")


async def test_fda_search():
    """Test FDA drug search"""
    print_header("Testing FDA Drug Search")

    try:
        query = "aspirin"
        print(f"Searching for: {query}\n")
        response = await search_drugs(query)

        if "error" in response:
            print(f"FDA API error: {json.dumps(response['error'], indent=2)}")
            return False

        results = response.get("results", [])
        if not results:
            print("No results returned.")
            return False

        print(f"Found {len(results)} results:\n")
        for i, result in enumerate(results[:3], 1):
            brand   = result.get("openfda", {}).get("brand_name", ["N/A"])[0]
            generic = result.get("openfda", {}).get("generic_name", ["N/A"])[0]
            print(f"  {i}. Brand: {brand}  |  Generic: {generic}")

        print("\n✓ FDA drug search test passed!")
        return True

    except Exception as e:
        print(f"✗ FDA drug search test failed: {type(e).__name__}: {e}")
        return False


async def test_fda_drug_info():
    """Test FDA drug info retrieval"""
    print_header("Testing FDA Drug Info")

    try:
        drug = "ibuprofen"
        print(f"Getting info for: {drug}\n")
        info = await get_drug_info(drug)

        if "error" in info:
            print(f"Error: {info['error']}")
            return False

        # ── Identity ──────────────────────────────────────────────
        print(f"  Brand Name:   {info['name']['brand']}")
        print(f"  Generic Name: {info['name']['generic']}")
        print(f"  Manufacturer: {info['manufacturer']}")

        # ── Full fields ───────────────────────────────────────────
        print_field("Purpose / Indications", info['purpose'])
        print_field("Warnings",              info['warnings'])
        print_field("Dosage & Administration", info['dosage'])
        print_field("Side Effects / Adverse Reactions", info['side_effects'])
        print_field("Drug Interactions",     info['interactions'])
        print_field("Indications & Usage",   info['indications'])

        print("\n✓ FDA drug info test passed!")
        return True

    except Exception as e:
        import traceback
        print(f"✗ FDA drug info test failed: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False


async def run_all_tests():
    print("\n" + "=" * 60)
    print("  API Test Suite")
    print("=" * 60)

    results = []
    results.append(("FDA Drug Search", await test_fda_search()))
    results.append(("FDA Drug Info",   await test_fda_drug_info()))

    print_header("Test Summary")
    passed = sum(1 for _, r in results if r)
    total  = len(results)

    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    asyncio.run(run_all_tests())