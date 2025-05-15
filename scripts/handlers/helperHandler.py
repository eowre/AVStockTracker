import os
import re
import pandas as pf

class helperHandler:
    """
    Helper class to handle file operations.
    """

    def __init__(self):
        """
        Initializes the helperHandler class.
        """
        pass

    def find_files(self, directory, pattern):
        """
        Find all files in a directory that match a given regex pattern.

        :param directory: Directory to search in.
        :param pattern: Regex pattern to match file names.
        :return: List of file paths that match the pattern.
        """
        matching_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if re.match(pattern, file):
                    matching_files.append(os.path.join(root, file))
        return matching_files

    def create_sets(self, sliced_data, date_ranges):

        ret = []
        # Iterate over the date ranges and create sets
        for i, date_range in enumerate(date_ranges):
            try:
                # Get the slices for the current date range
                aapl_slice = sliced_data["AAPL"]["sliced_data"][date_range]
                amzn_slice = sliced_data["AMZN"]["sliced_data"][date_range]

                # Ensure both slices are valid
                if aapl_slice is not None and amzn_slice is not None:
                    ret.append({
                        "AAPL": (aapl_slice, sliced_data["AAPL"]["meta_data"]),
                        "AMZN": (amzn_slice, sliced_data["AMZN"]["meta_data"])
                    })
                else:
                    print(f"Skipping set for date range {date_range} due to missing data.")
            except KeyError as e:
                print(f"Error accessing data for date range {date_range}: {e}")
        return ret
