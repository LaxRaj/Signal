# core/scoring.py
import pandas as pd

# Define the keyword matrix with weights
AI_KEYWORD_MATRIX = {
    'core_ai': (['llm', 'foundational model', 'neural network', 'generative ai', 'computer vision', 'agi', 'transformer architecture'], 1.0),
    'applied_ai': (['ai-powered', 'machine learning', 'intelligent automation', 'predictive analytics', 'nlp'], 0.6),
    'general_ai': (['ai'], 0.3)
}

def calculate_ai_confidence(text: str) -> float:
    """
    Calculates an AI confidence score based on the presence of tiered keywords.
    Returns a score between 0 and 1.
    """
    if not isinstance(text, str):
        return 0.0

    text_lower = text.lower()

    # Check for core AI terms first for highest confidence
    if any(term in text_lower for term in AI_KEYWORD_MATRIX['core_ai'][0]):
        return AI_KEYWORD_MATRIX['core_ai'][1]

    # Then check for applied AI terms
    if any(term in text_lower for term in AI_KEYWORD_MATRIX['applied_ai'][0]):
        return AI_KEYWORD_MATRIX['applied_ai'][1]

    # Finally, check for the general term
    if any(term in text_lower for term in AI_KEYWORD_MATRIX['general_ai'][0]):
        return AI_KEYWORD_MATRIX['general_ai'][1]

    return 0.0

def calculate_signal_score(row: pd.Series) -> float:
    """
    Calculates a holistic "Signal Score" for a company based on multiple factors.
    """
    # 1. AI Confidence Score
    text_to_analyze = f"{row.get('title', '')} {row.get('description', '')}"
    ai_confidence = calculate_ai_confidence(text_to_analyze)

    # 2. Source Score
    source_score = 0.0
    if row.get('source') == 'TechCrunch':
        source_score = 0.8
    elif row.get('source') == 'Product Hunt':
        source_score = 0.5

    # 3. Content Score (simple version)
    content_score = 0.5 # Baseline score
    title_lower = str(row.get('title', '')).lower()
    if 'raises' in title_lower or 'funding' in title_lower or 'series' in title_lower:
        content_score = 1.0 # Funding news is a very strong signal
    elif 'launches' in title_lower:
        content_score = 0.7

    # Calculate weighted final score (out of 100)
    final_score = (ai_confidence * 40) + (source_score * 30) + (content_score * 30)

    return round(final_score, 1) 