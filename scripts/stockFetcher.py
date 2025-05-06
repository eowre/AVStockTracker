import os
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

load_dotenv("config.env")

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY in config.env.")

class AVStockDataFetcher:
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
            data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='full')
            data.index = pd.to_datetime(data.index)
            filtered_data = data.loc[start_date:end_date]

            return filtered_data

if __name__ == "__main__":
    fetcher = AVStockDataFetcher(API_KEY)
    symbol = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    data = fetcher.fetch_data(symbol, start_date, end_date)
    print(data)