from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openfda import search_drugs
from gemini import generate_text, chat

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

# Pydantic models
class GenerateRequest(BaseModel):
    prompt: str
    temperature: float = 0.7

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

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

@app.post("/gemini/generate")
async def gemini_generate(request: GenerateRequest):
    """
    Generate text using Gemini API
    
    Request Body:
        prompt: The input prompt
        temperature: Temperature for generation (0.0-1.0)
    
    Returns:
        Generated text response
    """
    response = generate_text(request.prompt, request.temperature)
    return {"response": response}

@app.post("/gemini/chat")
async def gemini_chat(request: ChatRequest):
    """
    Chat with Gemini API
    
    Request Body:
        message: User message
        conversation_history: Optional list of previous messages for context

    Returns:
        Chat response from Gemini
    """
    response = await chat(request.message, request.conversation_history)
    return {"response": response}
