from utils.extract import scrape_product
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgres

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'

    # Extract
    raw_data = scrape_product(BASE_URL)

    # Transform
    clean_df = transform_data(raw_data)

    # Load
    save_to_csv(clean_df, "fashion_products.csv")
    
    # Replace with your actual database URL
    # postgres_url = "postgresql://username:password@localhost:5432/dbname"
    # save_to_postgres(clean_df, "fashion_products", postgres_url)

if __name__ == "__main__":
    main()
