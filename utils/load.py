import pandas as pd
from datetime import datetime
import os
import asyncio
import aiofiles

async def save_to_csv(df, filename=None):
    """
    Save DataFrame to CSV file asynchronously.
    """
    if df.empty:
        print("No data to save")
        return None
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fashion_products_{timestamp}.csv"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Save to CSV (pandas to_csv isn't async, but we can run it in a thread)
    await asyncio.to_thread(df.to_csv, filename, index=False)
    print(f"Data saved to {filename}")
    return filename