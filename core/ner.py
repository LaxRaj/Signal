# core/ner.py
import spacy

# Load the pre-trained English model. This is best done once when the module is loaded.
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...\n"
          "This is a one-time download.")
    from spacy.cli import download
    download("en_core_web_sm")
    NLP = spacy.load("en_core_web_sm")


def extract_company_names(text: str) -> list[str]:
    """
    Extracts company names (entities labeled as 'ORG') from a given text.
    It prioritizes shorter, more specific names.

    Args:
        text: The input string (e.g., an article title or description).

    Returns:
        A list of unique company names found in the text.
    """
    if not isinstance(text, str) or not text:
        return []

    doc = NLP(text)

    company_names = []
    # Iterate over the identified entities
    for entity in doc.ents:
        # Check if the entity is labeled as an ORGANIZATION
        if entity.label_ == "ORG":
            # Simple filter to avoid overly long, likely incorrect entities
            if len(entity.text.split()) < 5:
                company_names.append(entity.text.strip())

    # Return a list of unique company names to avoid duplicates
    return list(set(company_names)) 