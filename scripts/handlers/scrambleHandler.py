# Imports
import random
from datetime import datetime

class ScrambleHandler:
    """
    A class to handle the scrambling of date formats.
    
    Attributes:
        date_str (str): The date string to be scrambled.
    """
    
    def __init__(self, ):
        """
        Initializes the ScrambleHandler with a date string.
        
        Args:
            date_str (str): The input date string in the format 'YYYY-MM-DD'.
        """
        
# Functions
    def scramble_date_format(date_str):
        """
        Scrambles the date format of the given date string into one of 5 common formats.
        
        Args:
            date_str (str): The input date string in the format 'YYYY-MM-DD'.
        
        Returns:
            str: The date string in a randomly chosen format.
        """
        # Define 5 common date formats
        date_formats = [
            "%Y-%m-%d",  # Example: 2025-05-07
            "%d-%m-%Y",  # Example: 07-05-2025
            "%m/%d/%Y",  # Example: 05/07/2025
            "%B %d, %Y", # Example: May 7, 2025
            "%d %b %Y"   # Example: 07 May 2025
        ]
        
        # Parse the input date string
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Randomly select a format
        random_format = random.choice(date_formats)
        
        # Return the date in the selected format
        return date_obj.strftime(random_format)
    
    def scramble_currency_format(currency_str):
        """
        Scrambles the currency format of the given currency string into one of 5 common formats.
        
        Args:
            currency_str (str): The input currency string in the format 'USD 100.00'.
        
        Returns:
            str: The currency string in a randomly chosen format.
        """
        # Define 5 common currency formats
        currency_formats = [
            "${:,.2f}",  # Example: $100.00
            "USD {:,.2f}",  # Example: USD 100.00
            "{:,.2f} USD",  # Example: 100.00 USD
            "${:,.0f}",  # Example: $100
            "USD {:,.0f}"   # Example: USD 100
        ]
        
        # Parse the input currency string
        amount = float(currency_str.split()[1])
        
        # Randomly select a format
        random_format = random.choice(currency_formats)
        
        # Return the currency in the selected format
        return random_format.format(amount)
