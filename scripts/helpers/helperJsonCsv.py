import os
import pandas as pd
import json

class helperJsonCsv:
    """
    Helper class to save data frames in csv and json format.
    """
    def __init__(self):
        """
        Initializes the helperJsonCsv class.
        """
        pass

    def df_to_csv(self, df, csv_file_path):
        """
        Save DataFrame to CSV file.

        :param df: DataFrame to save.
        :param csv_file_path: Path to save the CSV file.
        """
        df_with_index = df.reset_index()
        df_with_index.to_csv(csv_file_path, index=False)

    def df_to_json(self, df, meta_data, json_file_path):
        """
        Save DataFrame and metadata to a JSON file.

        :param df: DataFrame to save.
        :param meta_data: Metadata to save.
        :param json_file_path: Path to save the JSON file.
        """
        # Reset index to include it in the JSON output
        df_with_index = df.reset_index()

        # Convert date from Timestamp to string
        df_with_index['date'] = df_with_index['date'].astype(str)

        # Convert DataFrame to JSON
        df_json = df_with_index.to_dict(orient='records')
        # Combine metadata and stock data
        combined_data = {
            "meta_data": meta_data,
            "data": df_json
        }

        # Save the combined data to a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(combined_data, json_file, indent=4)

    def multiple_dfs_to_csv_and_json(self, dfs):
        """
        Save multiple DataFrames to unique CSV and JSON files.

        :param dfs: Dictionary where keys are tickers and values are tuples (DataFrame, metadata).
        """
        # Ensure the raw_data directory exists
        output_dir = os.path.join(os.path.dirname(__file__), "../../raw_data")
        os.makedirs(output_dir, exist_ok=True)

        for ticker, (data, meta_data) in dfs.items():
            if data is not None and meta_data is not None:

                latest_date = data.index[-1].strftime("%Y-%m-%d")
                # Save stock data to CSV
                csv_file_path = os.path.join(output_dir, f"{ticker}_data_{latest_date}.csv")
                self.df_to_csv(data, csv_file_path)

                # Save stock data and metadata to JSON
                json_file_path = os.path.join(output_dir, f"{ticker}_data_{latest_date}.json")
                self.df_to_json(data, meta_data, json_file_path)
            else:
                print(f"No data or metadata available for {ticker}. Skipping save.")
        self.save_metadata_to_master_csv(dfs, os.path.join(output_dir, "master_metadata.csv"))

    def save_metadata_to_master_csv(self, dfs, metadata_csv_path):
        """
        Save metadata for all tickers to a single master CSV file. If metadata already exists, skip it.
        Otherwise, append new metadata to the file.

        :param dfs: Dictionary where keys are tickers and values are tuples (DataFrame, metadata).
        :param metadata_csv_path: Path to save the master metadata CSV file.
        """
        # Prepare a list to hold metadata for all tickers
        metadata_list = []

        # Check if the metadata CSV file already exists
        if os.path.exists(metadata_csv_path):
            # Load existing metadata
            existing_metadata_df = pd.read_csv(metadata_csv_path)
            existing_tickers = set(existing_metadata_df["Ticker"])
        else:
            # If the file doesn't exist, initialize an empty set
            existing_tickers = set()

        for ticker, (data, meta_data) in dfs.items():
            if meta_data is not None and ticker not in existing_tickers:
                # Add the ticker to the metadata dictionary
                meta_data["Ticker"] = ticker
                metadata_list.append(meta_data)

        # If there is new metadata to add, append it to the file
        if metadata_list:
            new_metadata_df = pd.DataFrame(metadata_list)
            if os.path.exists(metadata_csv_path):
                # Append to the existing file
                new_metadata_df.to_csv(metadata_csv_path, mode='a', header=False, index=False)
            else:
                # Create a new file
                new_metadata_df.to_csv(metadata_csv_path, index=False)
        else:
            print("No new metadata to add.")