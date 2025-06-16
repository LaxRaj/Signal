# core/ai_analyst.py
import streamlit as st
import json
import google.generativeai as genai

# --- IMPORTANT ---
# For demonstration purposes, the API key is hardcoded here.
# In a production environment, this should be stored securely (e.g., as an environment variable or in a secrets manager).
GEMINI_API_KEY = "AIzaSyB7uLQsvn3wwfPRo8aAFlWXmaWzLnNspDU"

async def get_analyst_take(title: str, description: str):
    """
    Uses the Gemini API to generate a qualitative analysis of a startup.
    """
    if not GEMINI_API_KEY:
        return "Error: The Gemini API key is missing from `core/ai_analyst.py`."

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    As a Venture Capital Analyst, provide a brief, insightful analysis of the following startup based on the provided news item.
    Structure your response in markdown with the following sections:
    - **The Signal:** What is the key takeaway from this news?
    - **Potential:** What is the potential upside or market opportunity?
    - **Risks:** What are the immediate risks or challenges?
    
    **News Item:**
    - Title: "{title}"
    - Description: "{description}"
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return "Error: Could not generate AI analysis." 