import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import pandas as pd
from utils.transform import transform_data


# --- Test Data ---
RAW_DATA = [
    {
        "Title": "Product 1",
        "Price": "$10.99",
        "Rating": "Rating: 4.5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Men",
        "Timestamp": "2023-01-01 00:00:00"
    },
    {
        "Title": "Unknown Product",
        "Price": "$0.00",
        "Rating": "Invalid",
        "Colors": "None",
        "Size": "Size: XL",
        "Gender": "Gender: Women",
        "Timestamp": "2023-01-01 00:00:00"
    }
]

# --- Tests ---
@pytest.mark.asyncio
async def test_transform_data():
    transformed = await transform_data(RAW_DATA)
    assert isinstance(transformed, pd.DataFrame)
    assert len(transformed) == 1
    
    # Validate transformations
    assert transformed.iloc[0]["Title"] == "Product 1"
    assert transformed.iloc[0]["Price"] == 10.99 * 16000  # IDR conversion
    assert transformed.iloc[0]["Rating"] == 4.5
    assert transformed.iloc[0]["Colors"] == 3
    assert transformed.iloc[0]["Size"] == "M"
    assert transformed.iloc[0]["Gender"] == "Men"

@pytest.mark.asyncio
async def test_transform_empty_data():
    # Test with properly structured but empty data
    empty_data = [{
        "Title": "",
        "Price": "",
        "Rating": "",
        "Colors": "",
        "Size": "",
        "Gender": "",
        "Timestamp": ""
    }]
    transformed = await transform_data(empty_data)
    assert transformed.empty