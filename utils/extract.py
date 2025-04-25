import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

# Define headers to mimic a real browser request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Maximum number of concurrent requests
MAX_CONCURRENT_REQUESTS = 3

# Maximum number of retries for a failed request
MAX_RETRIES = 3

# Delay between requests (in seconds)
MIN_DELAY = 1
MAX_DELAY = 3

async def fetch_content(session, url, semaphore, retry=0):
    """
    Asynchronously sends a GET request with rate limiting and retry logic.
    """
    async with semaphore:  # Limit concurrent requests
        # Random delay to avoid detection
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        await asyncio.sleep(delay)
        
        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 429:  # Too Many Requests
                    if retry < MAX_RETRIES:
                        # Exponential backoff
                        wait_time = (2 ** retry) + random.random()
                        print(f"Rate limited. Waiting {wait_time:.2f}s before retry #{retry+1} for {url}")
                        await asyncio.sleep(wait_time)
                        return await fetch_content(session, url, semaphore, retry + 1)
                    else:
                        print(f"Failed after {MAX_RETRIES} retries: {url}")
                        return None
                else:
                    print(f"Error fetching {url}: HTTP {response.status}")
                    if retry < MAX_RETRIES:
                        # Linear backoff for other errors
                        wait_time = 1 + retry + random.random()
                        print(f"Waiting {wait_time:.2f}s before retry #{retry+1}")
                        await asyncio.sleep(wait_time)
                        return await fetch_content(session, url, semaphore, retry + 1)
                    return None
        except Exception as e:
            print(f"Exception while fetching {url}: {e}")
            if retry < MAX_RETRIES:
                wait_time = 1 + retry + random.random()
                print(f"Waiting {wait_time:.2f}s before retry #{retry+1}")
                await asyncio.sleep(wait_time)
                return await fetch_content(session, url, semaphore, retry + 1)
            return None

def extract_product_data(product_card, timestamp):
    """
    Extracts product information from a collection card element.
    """
    # [Keep your existing extraction logic]
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
        "Scraped_At": timestamp
    }
    return product

async def process_page(session, url, semaphore, page_num, total_pages):
    """
    Process a single page: fetch HTML content and extract product data.
    """
    page_start_time = datetime.now()
    print(f"[{page_num}/{total_pages}] Fetching page at: {page_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {url}")
    
    content = await fetch_content(session, url, semaphore)
    page_products = []
    next_page_exists = False
    
    if content:
        soup = BeautifulSoup(content, "html.parser")
        collection_grid = soup.find('div', class_='collection-grid', id='collectionList')
        
        if collection_grid:
            product_cards = collection_grid.find_all('div', class_='collection-card')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Found {len(product_cards)} products on page {page_num}")
            
            for card in product_cards:
                product = extract_product_data(card, timestamp)
                page_products.append(product)
            
            next_button = soup.find('li', class_='page-item next')
            if next_button and next_button.find('a'):
                next_page_exists = True
        else:
            print(f"No collection grid found on page {page_num}")
    else:
        print(f"Failed to fetch content from {url} (page {page_num})")
    
    return page_products, next_page_exists

async def scrape_pages_batch(session, base_url, semaphore, start_page, end_page):
    """
    Scrape a batch of pages and return their products.
    """
    tasks = []
    total_pages = end_page - start_page + 1
    
    for page_num in range(start_page, end_page + 1):
        if page_num == 1:
            url = 'https://fashion-studio.dicoding.dev/'  # First page
        else:
            url = base_url.format(page_num)  # Subsequent pages
        
        task = process_page(session, url, semaphore, page_num, total_pages)
        tasks.append(task)
    
    # Process pages in parallel, respecting the semaphore limit
    results = await asyncio.gather(*tasks)
    
    # Flatten the list of products
    all_products = []
    for products, _ in results:
        all_products.extend(products)
    
    return all_products

async def scrape_product_async(base_url, max_pages=50, batch_size=10):
    """
    Asynchronously scrapes product data from paginated pages with batching.
    """
    all_products = []
    scraping_start_time = datetime.now()
    print(f"Scraping started at: {scraping_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Will scrape up to {max_pages} pages in batches of {batch_size}")
    
    # Create a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    # Use a longer timeout and more aggressive connection pooling for many requests
    conn = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=30*60, connect=30, sock_read=30)
    
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        # Process pages in batches to avoid creating too many tasks at once
        for batch_start in range(1, max_pages + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, max_pages)
            print(f"\n--- Processing batch of pages {batch_start}-{batch_end} ---")
            
            batch_products = await scrape_pages_batch(
                session, base_url, semaphore, batch_start, batch_end
            )
            
            all_products.extend(batch_products)
            print(f"Total products scraped so far: {len(all_products)}")
            
            # Short pause between batches
            if batch_end < max_pages:
                print(f"Pausing between batches...")
                await asyncio.sleep(random.uniform(2, 5))
    
    scraping_end_time = datetime.now()
    print(f"\nScraping finished at: {scraping_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total scraping time: {scraping_end_time - scraping_start_time}")
    print(f"Total products scraped: {len(all_products)}")
    
    return all_products

# Keep your existing main_async and main functions

async def main_async():
    """
    Asynchronous main function to execute the scraping process.
    """
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_products = await scrape_product_async(BASE_URL, max_pages=50, batch_size=5)
    
    if all_products:
        df = pd.DataFrame(all_products)
        print("\nScraping Results:")
        print(f"Total products scraped: {len(df)}")
        print(f"Products from {df['Scraped_At'].min()} to {df['Scraped_At'].max()}")
        
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