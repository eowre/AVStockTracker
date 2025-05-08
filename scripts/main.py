import os
from dotenv import load_dotenv
import pandas as pd
from handlers.stockHandler import AVStockDataHandler  # Import the stock data handler class
from handlers.storageHandler import storageHandler  # Import the storage handler class
from handlers.helperHandler import helperHandler  # Import the helper handler class

# Load environment variables from the config file
load_dotenv("config.env")

# Retrieve the API key from the environment variables
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Raise an error if the API key is not found
if not API_KEY:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY in config.env.")

def main():
    # Stock tickers to track
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    # Date range for the stock data
    start_date = '2020-01-01'
    end_date = '2025-01-01'

    # Initialize the storage handler
    storage_handler = storageHandler()

    # Initialize the stock handler and fetch data
    # stock_handler = AVStockDataHandler(API_KEY)
    # ticker_data = stock_handler.fetch_multiple_tickers(tickers, start_date, end_date)

    # # Save each DataFrame to CSV and JSON
    # storageHandler.multiple_dfs_to_csv_and_json(ticker_data)

    # Initialize the helper handler
    helper_handler = helperHandler()

    # Define regex patterns for locating AAPL and GOOGL files
    AAPL_pattern = r"../raw_data/AAPL*\.csv$"  # Matches any CSV file starting with "AAPL" in the raw_data folder
    GOOGL_pattern = r"../raw_data/GOOGL*\.json$"  # Matches any JSON file starting with "GOOGL" in the raw_data folder

    # Use the helper handler to locate files matching the patterns
    aapl_file = helper_handler.find_files("../raw_data", AAPL_pattern)
    googl_file = helper_handler.find_files("../raw_data", GOOGL_pattern)

    # Check if the AAPL file was found and process it
    if aapl_file:
        AAPL_data = storage_handler.df_builder(aapl_file)  # Build a DataFrame from the AAPL file
    else:
        print("AAPL file not found.")

    # Check if the GOOGL file was found and process it
    if googl_file:
        GOOGL_data = storage_handler.df_builder(googl_file)  # Build a DataFrame from the GOOGL file
    else:
        print("GOOGL file not found.")

    # TODO: Implement the StockAnalyzer and StockVisualizer classes for further analysis and visualization
    # analyzer = StockAnalyzer()
    # visualizer = StockVisualizer()

if __name__ == "__main__":
    main()
