import pandas as pd
import re

def transform_data(raw_data, exchange_rate=16000):
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
            return price_number * 16000
        except:
            return None

    df['Price'] = df['Price'].apply(convert_price)
    df = df[df['Price'].notnull()]

    # Clean 'Size' and 'Gender'
    df['Size'] = df['Size'].str.replace("Size:", "").str.strip()
    df['Gender'] = df['Gender'].str.replace("Gender:", "").str.strip()

    return df
