import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define headers to mimic a real browser request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """
    Sends a GET request to the provided URL and returns the response content if successful.
    """
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return None

def extract_product_data(product_card):
    """
    Extracts product information from a collection card element.
    """
    try:
        product_title = product_card.find('h3', class_='product-title').text.strip()
    except AttributeError:
        product_title = "N/A"
    
    try:
        price_element = product_card.find('span', class_='price')
        if price_element:
            price = price_element.text.strip()
        else:
            price_paragraph = product_card.find('p', class_='price')
            price = price_paragraph.text.strip() if price_paragraph else "N/A"
    except AttributeError:
        price = "N/A"
    
    # Finding all detail paragraphs
    detail_paragraphs = product_card.find_all('p', style="font-size: 14px; color: #777;")
    
    rating = colors = size = gender = "N/A"
    
    if detail_paragraphs:
        for p in detail_paragraphs:
            text = p.text.strip()
            if "Rating:" in text:
                rating = text
            elif "Colors" in text:
                colors = text
            elif "Size:" in text:
                size = text
            elif "Gender:" in text:
                gender = text
    
    product = {
        "Title": product_title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
    }
    return product

def scrape_product(base_url, start_page=1, delay=2):
    """
    Scrapes product data from the paginated product pages of the given base URL.
    Args:
        base_url (str): Base URL with a placeholder for page number (used from page 2 onward).
        start_page (int): Page number to start scraping from.
        delay (int): Delay in seconds between page requests.
    Returns:
        list: List of dictionaries containing product data.
    """
    data = []
    page_number = start_page
    
    while page_number < 5:  # for experimentation, will be changed to True, when code is working
        if page_number == 1:
            url = 'https://fashion-studio.dicoding.dev/'  # First page
        else:
            url = base_url.format(page_number)  # Subsequent pages
            
        print(f"Scraping page: {url}")
        content = fetching_content(url)
        
        if content:
            soup = BeautifulSoup(content, "html.parser")
            collection_grid = soup.find('div', class_='collection-grid', id='collectionList')
            
            if collection_grid:
                product_cards = collection_grid.find_all('div', class_='collection-card')
                
                for card in product_cards:
                    product = extract_product_data(card)
                    data.append(product)
                
                next_button = soup.find('li', class_='page-item next')
                if next_button and next_button.find('a'):
                    page_number += 1
                    time.sleep(delay)
                else:
                    break
            else:
                print("No collection grid found on the page")
                break
        else:
            break
            
    return data

def main():
    """
    Main function to execute the entire scraping process and display the results as a DataFrame.
    """
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_products = scrape_product(BASE_URL)
    
    if all_products:
        df = pd.DataFrame(all_products)
        print(df)
    else:
        print("No products were scraped.")

if __name__ == '__main__':
    main()