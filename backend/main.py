from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openfda import search_drugs

load_dotenv()

app = FastAPI(
    title="Dashboard API",
    description="Backend API for dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Dashboard API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/drugs/search")
async def search_drugs_endpoint(q: str):
    """
    Search for drugs by brand name using OpenFDA API
    
    Query Parameters:
        q: Drug brand name to search for
    
    Returns:
        Drug information from FDA
    """
    return await search_drugs(q)
