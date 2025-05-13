import os
from dotenv import load_dotenv
import pandas as pd
from handlers.stockHandler import AVStockDataHandler  # Import the stock data handler class
from handlers.storageHandler import storageHandler  # Import the storage handler class
from handlers.helperHandler import helperHandler  # Import the helper handler class
from handlers.scrambleHandler import scrambleHandler  # Import the scramble handler class
from handlers.SQLHandler import SQLHandler  # Import the SQL handler class
from handlers.cleaningHandler import cleaningHandler  # Import the cleaning handler class

# Load environment variables from the config file
load_dotenv("config.env")

# Retrieve the API key from the environment variables
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
DB_PATH = os.getenv("DB_PATH")

# Raise an error if the API key is not found
if not API_KEY:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY in config.env.")

if not DB_PATH:
    raise ValueError("Database path not found. Please set the DB_PATH in config.env.")

def main():
    # Stock tickers to track
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    # Date range for the stock data
    start_date = '2020-01-01'
    end_date = '2025-01-01'

    # Initialize the handlers
    stock_handler = AVStockDataHandler(API_KEY)
    storage_handler = storageHandler()
    SQL_handler = SQLHandler(DB_PATH)
    scramble_handler = scrambleHandler()
    helper_handler = helperHandler()
    cleaning_handler = cleaningHandler()

    ticker_data = stock_handler.fetch_multiple_tickers(tickers, start_date, end_date)

    # Save each DataFrame to CSV and JSON
    storage_handler.multiple_dfs_to_csv_and_json(ticker_data)
    # Save data to SQL tables
    SQL_handler.save_dfs_to_table(ticker_data)

    # Define regex patterns for locating AAPL and GOOGL files
    AAPL_pattern = r"^AAPL.*\.csv$"  # Matches any CSV file starting with "AAPL"
    GOOGL_pattern = r"^GOOGL.*\.json$"  # Matches any JSON file starting with "GOOGL"

    # Use the helper handler to locate files matching the patterns
    aapl_file = helper_handler.find_files("raw_data", AAPL_pattern)
    googl_file = helper_handler.find_files("raw_data", GOOGL_pattern)

    # Debug: Print matching files
    print("AAPL files found:", aapl_file)
    print("GOOGL files found:", googl_file)

    # Check if the AAPL file was found and process it
    if aapl_file:
        AAPL_data = storage_handler.df_builder(aapl_file[0])  # Use the first matching file
    else:
        print("AAPL file not found.")
    # Check if the GOOGL file was found and process it
    if googl_file:
        GOOGL_data = storage_handler.df_builder(googl_file[0])  # Use the first matching file
    else:
        print("GOOGL file not found.")

    # Sample data from AAPL CSV file for scrambling
    AAPL_date_scramble = AAPL_data.sample(n=25, random_state=42)

    print("Original AAPL data:")
    print(AAPL_date_scramble)

    if 'date' not in AAPL_date_scramble.columns:
        AAPL_date_scramble = AAPL_date_scramble.reset_index()
    
    scramble_handler.scramble_df(AAPL_date_scramble)

    print("Scrambled AAPL data:")
    print(AAPL_date_scramble)

    cleaning_handler.clean_data(AAPL_date_scramble)
    print("Cleaned AAPL data:")
    print(AAPL_date_scramble)

    # TODO: Implement the StockAnalyzer and StockVisualizer classes for further analysis and visualization
    # analyzer = StockAnalyzer()
    # visualizer = StockVisualizer()

if __name__ == "__main__":
    main()
