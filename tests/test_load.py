import pandas as pd
import os
from utils.load import save_to_csv # save_to_postgresql

def test_save_to_csv(tmp_path):
    df = pd.DataFrame({
        "Title": ["Test"],
        "Price": [10000],
        "Rating": [4.5],
        "Colors": [3],
        "Size": ["M"],
        "Gender": ["Unisex"],
        "ScrapedAt": ["2025-04-25 12:00:00"]
    })
    
    output_file = tmp_path / "test_output.csv"
    save_to_csv(df, output_file)
    
    assert os.path.exists(output_file)
    df_loaded = pd.read_csv(output_file)
    assert df_loaded.shape[0] == 1

# PostgreSQL test requires connection details; comment out unless using test DB
# def test_save_to_postgresql():
#     df = pd.DataFrame({...})
#     save_to_postgresql(df)
#     # Assert logic depending on test environment
