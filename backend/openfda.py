import httpx
import os

API_KEY = os.getenv("FDA_API_KEY", "")

async def search_drugs(q: str):
    """
    Search for drugs by brand name using OpenFDA API
    
    Args:
        q: Search query (drug brand name)
    
    Returns:
        Dict containing drug information from FDA
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.fda.gov/drug/label.json",
            params={
                "search": f"openfda.brand_name:{q}",
                "limit": 5,
                "api_key": API_KEY
            }
        )
    return response.json()
