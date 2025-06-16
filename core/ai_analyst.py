# core/ai_analyst.py
import streamlit as st
import google.generativeai as genai

async def get_analyst_take(title: str, description: str):
    """
    Uses the Gemini API to generate a qualitative analysis of a startup.
    """
    # The API key is now fetched and validated in the main app.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
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
        # The error will be displayed in the main app UI
        st.error(f"An error occurred with the Gemini API: {e}")
        return "Error: Could not generate AI analysis." 