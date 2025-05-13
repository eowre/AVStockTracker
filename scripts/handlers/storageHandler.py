import os
import pandas as pd
import json

class storageHandler:
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

    def multiple_dfs_to_csv_and_json(self, dfs, file_type="both"):
        """
        Save multiple DataFrames to unique CSV and/or JSON files.

        :param dfs: Dictionary where keys are tickers and values are tuples (DataFrame, metadata).
        :param file_type: String indicating the file type to save ("csv", "json", or "both").
        """
        # Ensure the raw_data directory exists
        output_dir = os.path.join(os.path.dirname(__file__), "../../raw_data")
        os.makedirs(output_dir, exist_ok=True)

        # Validate the file_type parameter
        if file_type not in ["csv", "json", "both"]:
            raise ValueError("Invalid file_type. Must be 'csv', 'json', or 'both'.")

        for ticker, (data, meta_data) in dfs.items():
            if data is not None and meta_data is not None:
                latest_date = data.index[-1].strftime("%Y-%m-%d")

                # Save stock data to CSV if file_type is "csv" or "both"
                if file_type in ["csv", "both"]:
                    csv_file_path = os.path.join(output_dir, f"{ticker}_data_{latest_date}.csv")
                    self.df_to_csv(data, csv_file_path)

                # Save stock data and metadata to JSON if file_type is "json" or "both"
                if file_type in ["json", "both"]:
                    json_file_path = os.path.join(output_dir, f"{ticker}_data_{latest_date}.json")
                    self.df_to_json(data, meta_data, json_file_path)
            else:
                print(f"No data or metadata available for {ticker}. Skipping save.")

        # Save metadata to a master CSV file
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

    def df_builder(self, file_path):
        """
        Build a DataFrame from a CSV or json file

        :param file_path: Path to the CSV/JSON file.
        :return: DataFrame built from the CSV/JSON file.
        """
        if file_path.endswith('.csv'):
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            # Load the JSON file into a DataFrame
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

                if "data" not in data:
                    raise ValueError("Invalid JSON structure. Expected a 'data' key.")
                # Convert the JSON data to a DataFrame
                df = pd.DataFrame(data['data'])  # Assuming the JSON structure has a "data" key
                
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")

        # Convert the 'date' column to datetime and set it as the index
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        return df


