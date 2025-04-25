import asyncio
import aiohttp
from datetime import datetime
import argparse
import sys

# Import modules
from utils.extract import fetch_content, extract_product_data, process_page, scrape_product_async
from utils.transform import transform_data
from utils.load import save_to_csv

async def pipeline(base_url, max_pages=50, output_format='csv'):
    """
    Main data pipeline: extract, transform, load.
    Now fully asynchronous.
    """
    print(f"Starting scraping pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Extract data
    raw_data = await scrape_product_async(base_url, max_pages)
    print(f"Extracted {len(raw_data)} products")
    
    # Transform data
    transformed_data = await transform_data(raw_data)
    print(f"Transformed data: {len(transformed_data)} rows")
    
    # Load data
    if output_format.lower() == 'csv':
        result = await save_to_csv(transformed_data)
    else:
        print(f"Unsupported output format: {output_format}")
        result = None
        
    print(f"Pipeline completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return result

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Fashion product scraper")
    parser.add_argument("--pages", type=int, default=50, help="Maximum number of pages to scrape")
    parser.add_argument("--format", choices=['csv', 'json'], default='csv', help="Output format")
    return parser.parse_args()

def main():
    args = parse_args()
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    
    # Run the async pipeline
    try:
        result = asyncio.run(pipeline(BASE_URL, args.pages, args.format))
        if result:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Error
    except KeyboardInterrupt:
        print("Scraping interrupted by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        print(f"Error in scraping pipeline: {e}")
        sys.exit(1)  # Error

if __name__ == '__main__':
    main()