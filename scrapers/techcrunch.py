# scrapers/techcrunch.py
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape():
    """
    Scrapes the TechCrunch "Startups" category page for the latest articles.
    
    Returns:
        pd.DataFrame: A DataFrame containing the scraped data with columns
                      ['source', 'title', 'description']. Returns an empty
                      DataFrame if scraping fails.
    """
    url = "https://techcrunch.com/category/startups/"
    headers = {
        'User-Agent': 'ProjectSignalBot/1.0'
    }
    
    print("Scraping TechCrunch Startups...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error during request to {url}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    
    # Find all article containers. The class name is dynamically generated in part,
    # so we look for a class that starts with 'wp-block-post'.
    article_elements = soup.find_all('li', class_=lambda x: x and x.startswith('wp-block-post'))
    
    if not article_elements:
        print("No article elements found. The page structure may have changed.")
        return pd.DataFrame()

    for article in article_elements:
        try:
            # The title is within an <h3> tag with class 'loop-card__title'
            title_element = article.find('h3', class_='loop-card__title')
            
            if title_element and title_element.find('a'):
                title = title_element.get_text(strip=True)
                # Description is not consistently available, using title as a placeholder
                description = title
                
                articles.append({
                    'source': 'TechCrunch',
                    'title': title,
                    'description': description
                })
        except Exception as e:
            print(f"Error parsing an article element: {e}")
            continue # Move to the next article

    return pd.DataFrame(articles)
