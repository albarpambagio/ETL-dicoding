import asyncio
import aiohttp
from datetime import datetime
import argparse
import sys
import ssl
import certifi
from typing import Optional, List, Dict, Any

# Configure SSL context properly
def create_ssl_context() -> ssl.SSLContext:
    """Create and configure SSL context with certifi certificates"""
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    return ssl_context

# Import modules after SSL configuration
from utils.extract import fetch_content, extract_product_data, process_page, scrape_product_async
from utils.transform import transform_data
from utils.load import save_to_csv

async def pipeline(base_url: str, max_pages: int = 50, output_format: str = 'csv') -> Optional[str]:
    """
    Main data pipeline: extract, transform, load.
    Now fully asynchronous with proper error handling.
    """
    print(f"Starting scraping pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Extract data with timeout
        raw_data: List[Dict[str, Any]] = await asyncio.wait_for(
            scrape_product_async(base_url, max_pages),
            timeout=300  # 5 minutes timeout
        )
        print(f"Extracted {len(raw_data)} products")
        
        # Transform data
        transformed_data: List[Dict[str, Any]] = await transform_data(raw_data)
        print(f"Transformed data: {len(transformed_data)} rows")
        
        # Load data
        if output_format.lower() == 'csv':
            result: str = await save_to_csv(transformed_data)
            print(f"Pipeline completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return result
        else:
            print(f"Unsupported output format: {output_format}")
            return None
            
    except asyncio.TimeoutError:
        print("Scraping timed out after 5 minutes")
        return None
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        return None

def parse_args():
    """Parse command line arguments with improved help text"""
    parser = argparse.ArgumentParser(description="Async Fashion Product Scraper")
    parser.add_argument(
        "--pages",
        type=int,
        default=50,
        help="Maximum number of pages to scrape (default: 50)"
    )
    parser.add_argument(
        "--format",
        choices=['csv', 'json'],
        default='csv',
        help="Output format (default: csv)"
    )
    return parser.parse_args()

async def configure_aiohttp_session() -> aiohttp.ClientSession:
    """Configure aiohttp session with SSL context"""
    ssl_context = create_ssl_context()
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    return aiohttp.ClientSession(connector=connector)

def main() -> int:
    args = parse_args()
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    
    try:
        result = asyncio.run(pipeline(BASE_URL, args.pages, args.format))
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        return 130
    except Exception as e:
        print(f"Fatal error in main: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())