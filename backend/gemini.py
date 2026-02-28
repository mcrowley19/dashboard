import os
import google.generativeai as genai
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configure Gemini API
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
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    if not response.text:
        return "No summary generated."
    return response.text

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
