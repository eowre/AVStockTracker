import sqlite3
import pandas as pd

class SQLHandler:
    """
    Helper class to handle SQL storage operations.
    """
    def __init__(self, db_path):
        """
        Initialize the SQLHandler with a database path.

        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path

    def save_df_to_table(self, df, table_name):
        """
        Save a DataFrame to a SQL table.

        :param df: DataFrame to save.
        :param table_name: Name of the SQL table.
        """
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

    def load_table_to_df(self, table_name):
        """
        Load a SQL table into a DataFrame.

        :param table_name: Name of the SQL table.
        :return: DataFrame containing the table data.
        """
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql(f"SELECT * FROM {table_name}", conn)