import pandas as pd
from utils.transform import transform_data
import numpy as np

def test_transform_data():
    raw_data = [
        {
            "Title": "Cool T-Shirt",
            "Price": "$102.15",
            "Rating": "Rating: 4.8/5",
            "Colors": "Colors: 3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Unisex",
            "ScrapedAt": "2025-04-25 12:00:00"
        },
        {
            "Title": "Unknown Product",
            "Price": "$50",
            "Rating": "Not Rated",
            "Colors": "Colors: 2 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Male",
            "ScrapedAt": "2025-04-25 12:00:00"
        }
    ]
    
    df = pd.DataFrame(raw_data)
    cleaned = transform_data(df)

    # Should remove invalid product
    assert cleaned.shape[0] == 1
    assert cleaned.iloc[0]["Title"] == "Cool T-Shirt"
    assert isinstance(cleaned.iloc[0]["Price"], float)
    assert isinstance(cleaned.iloc[0]["Rating"], float)
    assert isinstance(cleaned.iloc[0]["Colors"], (int, np.integer)) 
    assert cleaned.iloc[0]["Colors"] == 3  # Additional value check
    assert "Size:" not in cleaned.iloc[0]["Size"]
    assert "Gender:" not in cleaned.iloc[0]["Gender"]
