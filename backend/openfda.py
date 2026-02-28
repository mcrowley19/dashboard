import httpx
import os
from urllib.parse import quote

API_KEY = os.getenv("FDA_API_KEY", "HBemGDPxGZhBuGSVayX6c9dCSUfcv6INh0C71ETM")
BASE_URL = "https://api.fda.gov/drug/label.json"


def _build_url(search: str, limit: int = 5) -> str:
    """
    Build FDA API URL manually to avoid httpx percent-encoding the + boolean operators.
    httpx encodes '+' as '%2B' when passed via params=, which breaks FDA's +OR+ / +AND+ syntax.
    We quote only the search value (keeping + safe), then append everything as a raw query string.
    """
    encoded_search = quote(search, safe="+:()")
    return f"{BASE_URL}?search={encoded_search}&limit={limit}&api_key={API_KEY}"


async def search_drugs(q: str) -> dict:
    """
    Search for drugs by brand name using OpenFDA API.
    """
    url = _build_url(f"openfda.brand_name:{q}", limit=5)
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
    return response.json()


async def get_drug_info(drug_name: str) -> dict:
    """
    Get detailed information about a specific drug by brand or generic name.

    FDA harmonizes generic names as UPPERCASE. We search both openfda fields
    and the raw active_ingredient field as a fallback.

    Note: URL is built manually — httpx encodes '+' as '%2B' in params dicts,
    which breaks FDA's boolean +OR+ operator.
    """
    name_upper = drug_name.upper()
    search = (
        f'openfda.brand_name:"{drug_name}"'
        f'+OR+openfda.generic_name:"{name_upper}"'
        f'+OR+active_ingredient:"{name_upper}"'
    )

    url = _build_url(search, limit=1)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    data = response.json()

    if "error" in data or not data.get("results"):
        return {"error": f"No information found for '{drug_name}'"}

    result = data["results"][0]
    openfda = result.get("openfda", {})

    return {
        "name": {
            "brand": openfda.get("brand_name", ["N/A"]),
            "generic": openfda.get("generic_name", ["N/A"]),
        },
        "manufacturer": openfda.get("manufacturer_name", ["N/A"]),
        "purpose": result.get("purpose", ["N/A"]),
        "warnings": result.get("warnings", ["N/A"]),
        "dosage": result.get("dosage_and_administration", ["N/A"]),
        "side_effects": result.get("adverse_reactions", ["N/A"]),
        "interactions": result.get("drug_interactions", ["N/A"]),
        "indications": result.get("indications_and_usage", ["N/A"]),
    }