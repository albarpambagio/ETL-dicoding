import pandas as pd


def save_to_csv(df, path='output.csv'):
    df.to_csv(path, index=False)
    print(f"Saved to {path}")


