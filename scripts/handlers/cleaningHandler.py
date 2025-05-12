import pandas as pd

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
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        return df
    def clean_currency_data(self, df):
        """
        Write a formula determine the format of the currency column 
        I want to perfom the operations inplace on the dataframe
        I want to return a list of currenct formats that were detected
        """
        # Check if 'currency' column exists
        if 'currency' not in df.columns:
            raise ValueError("DataFrame does not contain a 'currency' column.")

        # Define a list to store detected formats
        detected_formats = []

        # Define currency formats
        currency_formats = [
            r'^\$\d+(\.\d{2})?$',  # Example: $123.45
            r'^\d+(\.\d{2})?€$',    # Example: 123.45€
            r'^\£\d+(\.\d{2})?$',   # Example: £123.45
            r'^\d+\s*¥\d+(\.\d{2})?$',  # Example: 123 ¥456.78
            r'^\d+\s*INR\d+(\.\d{2})?$'  # Example: 123 INR456.78
        ]

        # Iterate through each currency format and check for matches
        for fmt in currency_formats:
            if df['currency'].str.match(fmt).any():
                detected_formats.append(fmt)

        return detected_formats
