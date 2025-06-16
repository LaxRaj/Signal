import pandas as pd

def analyze_trends(df: pd.DataFrame, keywords: list) -> pd.DataFrame:
    """
    Analyzes the frequency of keywords in the titles and descriptions of articles.
    Returns a DataFrame with keywords and their mention counts.
    """
    if df.empty or 'description' not in df.columns or 'title' not in df.columns:
        return pd.DataFrame(columns=['keyword', 'count'])

    keyword_counts = {keyword: 0 for keyword in keywords}
    text_corpus = (df['title'].fillna('') + ' ' + df['description'].fillna('')).str.lower()

    for keyword in keywords:
        keyword_counts[keyword] = text_corpus.str.contains(keyword.lower()).sum()

    trends_df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Mentions'])
    return trends_df