import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(df, path='output.csv'):
    df.to_csv(path, index=False)
    print(f"Saved to {path}")

def save_to_postgres(df, table_name, db_url):
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Saved to PostgreSQL table: {table_name}")
