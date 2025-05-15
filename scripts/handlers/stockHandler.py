import os
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

class AVStockDataHandler:
    def __init__(self, api_key: str):
        """
        Initializes the AVStockDataFetcher with the provided API key.

        Args:
            api_key (str): The API key for Alpha Vantage.
        """
        self.api_key = api_key
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        """
        Fetches full stock data from Alpha Vantage API for a given symbol.

        Args:
            symbol (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing the full stock data.
            dict: Metadata associated with the stock data.
        """
        # Fetch daily stock data
        data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='full')

        # Convert the index to datetime
        data.index = pd.to_datetime(data.index)
        
        # Sort the data by index
        data = data.sort_index()

        # Rename columns for consistency
        data.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        }, inplace=True)

        return data, meta_data

    def fetch_multiple_tickers(self, tickers: list, date_ranges: list) -> dict:
        """
        Fetches stock data for multiple tickers and slices it based on the provided date ranges.

        Args:
            tickers (list): List of stock ticker symbols.
            date_ranges (list): List of tuples, where each tuple is a date range (start_date, end_date).

        Returns:
            dict: A dictionary where keys are tickers and values are dictionaries of sliced DataFrames for each date range.
        """
        result = {}

        for ticker in tickers:
            try:
                print(f"Fetching full data for {ticker}...")
                # Fetch the full data for the ticker
                full_data, meta_data = self.fetch_data(ticker)

                # Slice the data for each date range
                sliced_data = {}
                for start_date, end_date in date_ranges:
                    try:
                        sliced_data[(start_date, end_date)] = full_data.loc[start_date:end_date]
                    except Exception as e:
                        print(f"Error slicing data for {ticker} in range {start_date} to {end_date}: {e}")
                        sliced_data[(start_date, end_date)] = None

                # Store the sliced data and metadata
                result[ticker] = {
                    "sliced_data": sliced_data,
                    "meta_data": meta_data
                }

            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                result[ticker] = {
                    "sliced_data": None,
                    "meta_data": None
                }

        return result