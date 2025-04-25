from utils.extract import scrape_product
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgres
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

    load_dotenv()  # Load variables from .env

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # Build the full PostgreSQL connection string
    postgres_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    save_to_postgres(clean_df, "fashion_products", postgres_url)

if __name__ == "__main__":
    main()
