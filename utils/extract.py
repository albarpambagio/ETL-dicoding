import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Define headers to mimic a real browser request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

async def fetch_content(session, url):
    """
    Asynchronously sends a GET request to the provided URL and returns the response content if successful.
    """
    try:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error fetching {url}: HTTP {response.status}")
                return None
    except Exception as e:
        print(f"Exception while fetching {url}: {e}")
        return None

def extract_product_data(product_card, timestamp):
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
        "Timestamp": timestamp
    }
    return product

async def process_page(session, url):
    """
    Process a single page: fetch HTML content and extract product data.
    """
    page_start_time = datetime.now()
    print(f"Fetching page at: {page_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {url}")
    
    content = await fetch_content(session, url)
    page_products = []
    next_page_exists = False
    
    if content:
        soup = BeautifulSoup(content, "html.parser")
        collection_grid = soup.find('div', class_='collection-grid', id='collectionList')
        
        if collection_grid:
            product_cards = collection_grid.find_all('div', class_='collection-card')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Found {len(product_cards)} products")
            
            for card in product_cards:
                product = extract_product_data(card, timestamp)
                page_products.append(product)
            
            next_button = soup.find('li', class_='page-item next')
            if next_button and next_button.find('a'):
                next_page_exists = True
        else:
            print("No collection grid found on the page")
    else:
        print(f"Failed to fetch content from {url}")
    
    return page_products, next_page_exists

async def scrape_product_async(base_url, max_pages=50):
    """
    Asynchronously scrapes product data from the paginated product pages.
    """
    all_products = []
    scraping_start_time = datetime.now()
    print(f"Scraping started at: {scraping_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with aiohttp.ClientSession() as session:
        page_number = 1
        has_next = True
        
        while has_next and page_number <= max_pages:
            if page_number == 1:
                url = 'https://fashion-studio.dicoding.dev/'  # First page
            else:
                url = base_url.format(page_number)  # Subsequent pages
            
            products, has_next = await process_page(session, url)
            all_products.extend(products)
            
            if has_next:
                page_number += 1
            else:
                print(f"No next page found after page {page_number}")
    
    scraping_end_time = datetime.now()
    print(f"Scraping finished at: {scraping_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total scraping time: {scraping_end_time - scraping_start_time}")
    
    return all_products

async def main_async():
    """
    Asynchronous main function to execute the scraping process.
    """
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_products = await scrape_product_async(BASE_URL, max_pages=50)
    
    if all_products:
        df = pd.DataFrame(all_products)
        print("\nScraping Results:")
        print(f"Total products scraped: {len(df)}")
        print(df.head())  # Show just the first few rows to keep output manageable
        
        # Save to CSV with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"fashion_products_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nResults saved to {csv_filename}")
    else:
        print("No products were scraped.")

def main():
    """
    Entry point that runs the async main function.
    """
    asyncio.run(main_async())

if __name__ == '__main__':
    main()