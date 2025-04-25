import pandas as pd
import re
import asyncio

async def transform_data(raw_data, exchange_rate=16000):
    """
    Transform the raw scraped data asynchronously.
    Keeps the same transformation logic but runs in an async context.
    """
    # Wrap the CPU-intensive transformation in a thread to not block the event loop
    return await asyncio.to_thread(_transform_data_sync, raw_data, exchange_rate)

def _transform_data_sync(raw_data, exchange_rate=16000):
    """
    The synchronous part of the transformation that will run in a thread.
    Contains your original transformation logic.
    """
    df = pd.DataFrame(raw_data)
    
    # Remove null and duplicate
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    
    # Remove invalid titles
    df = df[df['Title'] != 'Unknown Product']
    
    # Clean 'Rating'
    def clean_rating(val):
        try:
            return float(re.search(r"\d+(\.\d+)?", val).group())
        except:
            return None
    
    df['Rating'] = df['Rating'].apply(clean_rating)
    df = df[df['Rating'].notnull()]
    
    # Clean 'Colors'
    def extract_colors(val):
        try:
            return int(re.search(r"\d+", val).group())
        except:
            return None
    
    df['Colors'] = df['Colors'].apply(extract_colors)
    
    # Clean 'Price' and convert to IDR
    def convert_price(price_text):
        try:
            # Extract numeric value including decimals
            price_number = float(re.sub(r"[^\d.]", "", price_text))
            return price_number * exchange_rate
        except:
            return None
    
    df['Price'] = df['Price'].apply(convert_price)
    df = df[df['Price'].notnull()]
    
    # Clean 'Size' and 'Gender'
    df['Size'] = df['Size'].str.replace("Size:", "").str.strip()
    df['Gender'] = df['Gender'].str.replace("Gender:", "").str.strip()
    
    return df