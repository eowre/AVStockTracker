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

    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches stock data from Alpha Vantage API.

        Args:
            symbol (str): The stock ticker symbol.
            start_date (str): The start date for the data in 'YYYY-MM-DD' format.
            end_date (str): The end date for the data in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: A DataFrame containing the stock data.
        """
        # Fetch daily stock data
        data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='full')

        # Convert the index to datetime
        data.index = pd.to_datetime(data.index)
        
        # Sort the data by index
        data = data.sort_index()

        # Filter the data based on the provided date range
        filtered_data = data.loc[start_date:end_date]

        filter.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume"
        }, inplace=True)

        return filtered_data, meta_data

    def fetch_multiple_tickers(self, tickers: list, start_date: str, end_date: str) -> dict:
        """
        Fetches stock data for multiple tickers.

        Args:
            tickers (list): List of stock ticker symbols.
            start_date (str): The start date for the data in 'YYYY-MM-DD' format.
            end_date (str): The end date for the data in 'YYYY-MM-DD' format.

        Returns:
            dict: A dictionary containing DataFrames for each ticker.
        """
        data_dict = {}
        for ticker in tickers:
            try:
                print(f"Fetching data for {ticker}...")
                data, meta_data  = self.fetch_data(ticker, start_date, end_date)
                data_dict[ticker] = data, meta_data  
                # Store both data and metadata
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                data_dict[ticker] = (None, None)  # Store None if fetching fails for a ticker
        return data_dict