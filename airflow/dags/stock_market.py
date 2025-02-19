from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import yfinance as yf
from datetime import datetime
import pandas as pd

@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["stock_market"],
)

def fetch_and_store_stock_data():

    @task()
    def ensure_table_exists():
        hook = PostgresHook(postgres_conn_id="postgres_default")
        conn = hook.get_conn()
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(10),
            date DATE NOT NULL,
            close FLOAT,
            CONSTRAINT unique_date_ticker UNIQUE (date, ticker)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()

    @task()
    def fetch_data():
        ticker = "^OMXC25"
        stock = yf.Ticker(ticker)
        hist = stock.history(start="2025-01-01", end=datetime.today())
        
        if hist.empty:
            return [] 

        hist.reset_index(inplace=True)
        hist = hist[['Date', 'Close']]
        hist['ticker'] = ticker
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        hist.columns = hist.columns.str.lower()

        print(hist)

        return hist.to_dict(orient="records")

    @task()
    def store_data(stock_data):
        if not stock_data:
            return

        hook = PostgresHook(postgres_conn_id="postgres_default")
        conn = hook.get_conn()
        cursor = conn.cursor()

        insert_query = """
        insert into stock_prices (date, ticker, close)
        VALUES (%s, %s, %s)
        ON CONFLICT (date,ticker) DO UPDATE
        SET close = EXCLUDED.close
        """

        for row in stock_data:
            cursor.execute(insert_query, (row['date'], row['ticker'], row['close']))

        
        conn.commit()
        cursor.close()
        conn.close()

    ensure_table_exists()
    stock_data = fetch_data()
    store_data(stock_data)

fetch_and_store_stock_data()