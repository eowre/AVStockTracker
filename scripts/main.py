import os
from dotenv import load_dotenv
import pandas as pd
from stockFetcher import AVStockDataFetcher  # Import the required class
from scripts.helpers.storageHandler import helperJsonCsv  # Import the helper class

load_dotenv("config.env")

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY in config.env.")

def main():
    # Stock tickers to track
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    # Date range for the data
    start_date = '2020-01-01'
    end_date = '2025-01-01'

    # Initialize the fetcher and fetch data
    fetcher = AVStockDataFetcher(API_KEY)
    ticker_data = fetcher.fetch_multiple_tickers(tickers, start_date, end_date)

    # for ticker, data in ticker_data.items():
    #     print(f"\nData for {ticker}:")
    #     if data is not None:
    #         print(data.head())  # Print the first few rows of the DataFrame
    #     else:
    #         print("No data available for this ticker.")

    # Save the data to CSV and JSON
    storageHandler = helperJsonCsv()

    # Save each DataFrame to CSV and JSON
    storageHandler.multiple_dfs_to_csv_and_json(ticker_data)

    # TODO: Implement the StockAnalyzer and StockVisualizer classes
    # analyzer = StockAnalyzer()
    # visualizer = StockVisualizer()


if __name__ == "__main__":
    main()
