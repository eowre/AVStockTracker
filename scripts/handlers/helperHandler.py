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