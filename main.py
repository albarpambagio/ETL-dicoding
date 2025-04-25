from utils.extract import scrape_product
from utils.transform import transform_data
from utils.load import save_to_csv
from dotenv import load_dotenv
import os

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'

    # Extract
    raw_data = scrape_product(BASE_URL)

    # Transform
    clean_df = transform_data(raw_data)

    # Load
    save_to_csv(clean_df, "fashion_products.csv")

if __name__ == "__main__":
    main()
