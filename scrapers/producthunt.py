# scrapers/producthunt.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def scrape():
    """
    Scrapes the Product Hunt homepage for the top daily products.
    
    Returns:
        pd.DataFrame: A DataFrame containing the scraped data with columns
                      ['source', 'title', 'description']. Returns an empty
                      DataFrame if scraping fails.
    """
    url = "https://www.producthunt.com/"
    headers = {
        'User-Agent': 'ProjectSignalBot/1.0'
    }

    print("Scraping Product Hunt...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during request to {url}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    
    # Find all product containers using the data-test attribute.
    product_elements = soup.find_all('section', attrs={'data-test': re.compile(r'post-item-\d+')})

    if not product_elements:
        print("No product elements found. The page structure may have changed.")
        return pd.DataFrame()

    for product in product_elements:
        try:
            title_element = product.find('a', attrs={'data-test': re.compile(r'post-name-\d+')})
            
            # The description is the second 'a' tag within the product's div
            description_element = title_element.find_next_sibling('a')
            
            if title_element and description_element:
                title = title_element.get_text(strip=True)
                # The title often contains a number, which we can remove
                title = re.sub(r'^\d+\.\s*', '', title)
                description = description_element.get_text(strip=True)
                
                products.append({
                    'source': 'Product Hunt',
                    'title': title,
                    'description': description
                })
        except Exception as e:
            print(f"Error parsing a product element: {e}")
            continue

    return pd.DataFrame(products)

