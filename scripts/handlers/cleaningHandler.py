import pandas as pd
import re

class cleaningHandler:
    """
    Helper class to clean and process stock data.
    """

    def __init__(self):
        """
        Initializes the cleaningHandler class.
        """
        pass

    def clean_data(self, df):
        """
            Detect and handle missing values, remove duplicates, standardize formats
        """
        # Check for missing values
        if df.isnull().values.any():
            print("Missing values detected. Filling with forward fill method.")
            df.fillna(method='ffill', inplace=True)

        # Remove duplicates
        df.drop_duplicates(inplace=True)

        # Standardize date format
        self.clean_date_column(df, 'date')
        # Standardize currency formats
        self.clean_currency_data(df, 'open')
        self.clean_currency_data(df, 'high')
        self.clean_currency_data(df, 'low')
        self.clean_currency_data(df, 'close')
        return df
    
    def clean_date_column(self, df, column_name):
        """
        Cleans and normalizes the specified date column to the format 'YYYY-MM-DD'.

        :param df: DataFrame containing the date column.
        :param column_name: Name of the column to clean.
        :return: DataFrame with the cleaned date column.
        """
        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"DataFrame does not contain a '{column_name}' column.")

        # Define the supported date formats
        date_formats = [
            "%Y-%m-%d",  # Example: 2025-05-07
            "%d-%m-%Y",  # Example: 07-05-2025
            "%m/%d/%Y",  # Example: 05/07/2025
            "%B %d, %Y", # Example: May 7, 2025
            "%d %b %Y"   # Example: 07 May 2025
        ]

        # Function to parse and normalize dates
        def parse_date(value):
            for date_format in date_formats:
                try:
                    # Try parsing the date with the current format
                    return pd.to_datetime(value, format=date_format).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            # If no format matches, return NaT (Not a Time)
            return pd.NaT

        # Apply the parsing function to the column
        df[column_name] = df[column_name].apply(parse_date)

        # Handle any remaining invalid dates
        invalid_dates = df[column_name].isna().sum()
        if invalid_dates > 0:
            print(f"Warning: {invalid_dates} invalid dates found in column '{column_name}'.")

        return df

    def clean_currency_data(self, df, column_name):
        """
        Cleans the specified currency column by standardizing known formats to '121.000'.
        Outputs unknown formats along with a guess of their structure.

        :param df: DataFrame containing the currency column.
        :param column_name: Name of the column to clean.
        :return: List of detected unknown formats.
        """
        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"DataFrame does not contain a '{column_name}' column.")

        # List to store unknown formats
        unknown_formats = []

        # Define known currency formats and their regex patterns
        currency_patterns = {
            r'^\$\d+(\.\d{2})?$': lambda x: x.replace('$', ''),  # Example: $100.00 -> 100.00
            r'^USD\s\d+(\.\d{2})?$': lambda x: x.replace('USD ', ''),  # Example: USD 100.00 -> 100.00
            r'^\d+(\.\d{2})?\sUSD$': lambda x: x.replace(' USD', ''),  # Example: 100.00 USD -> 100.00
            r'^\d+(\.\d{2})?\$$': lambda x: x.replace('$', ''),  # Example: 100.00$ -> 100.00
            r'^USD\s\d{1,3}(\.\d{3})*,\d{2}$': lambda x: x.replace('USD ', '').replace('.', '').replace(',', '.'),  # Example: USD 1.234,56 -> 1234.56
        }

        # Regex pattern for the target format (e.g., 121.000)
        target_format_pattern = r'^\d+(\.\d{3})$'

        # Iterate through the column and clean the data
        for index, value in df[column_name].items():
            cleaned = False

            # Always normalize numeric values to three decimal places
            if pd.notnull(value):
                try:
                    # Attempt to convert directly to float and format to three decimals
                    df.at[index, column_name] = f"{float(value):.3f}"
                    continue
                except ValueError:
                    pass

            for pattern, cleaner in currency_patterns.items():
                if pd.notnull(value) and re.match(pattern, str(value)):
                    # Apply the cleaning function for the matched pattern
                    df.at[index, column_name] = f"{float(cleaner(str(value))):.3f}"
                    cleaned = True
                    break

            # Handle unknown formats
            if not cleaned and pd.notnull(value):
                print(f"Unknown format detected: {value}")
                unknown_formats.append(value)

        return unknown_formats
