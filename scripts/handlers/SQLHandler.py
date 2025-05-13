import sqlite3
import pandas as pd
import os

class SQLHandler:
    """
    Helper class to handle SQL storage operations.
    """
    def __init__(self, db_path):
        """
        Initialize the SQLHandler with a database path. Ensure the database file and directory exist.

        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path

        # Ensure the directory for the database exists
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"Created directory for database: {db_dir}")

        # Create the database file if it doesn't exist
        if not os.path.exists(self.db_path):
            with sqlite3.connect(self.db_path) as conn:
                print(f"Database created at: {self.db_path}")

    def save_dfs_to_table(self, dfs):
        """
        Save multiple DataFrames to SQL tables, including the index as a column and setting it as the primary key.

        :param dfs: Dictionary where keys are table names and values are tuples with data and metadata.
        """
        for table_name, (df, meta_data) in dfs.items():
            if df is not None:
                # Save the DataFrame to the SQL table
                self.save_df_to_table(df, table_name)
                print(f"DataFrame saved to table: {table_name}")
            else:
                print(f"No data available for table: {table_name}. Skipping.")

    def save_df_to_table(self, df, table_name):
        print(self.db_path)
        """
        Save a DataFrame to a SQL table, including the index as a column and setting it as the primary key.

        :param df: DataFrame to save.
        :param table_name: Name of the SQL table.
        """
        with sqlite3.connect(self.db_path) as conn:
            # Add the index as a column
            df_with_index = df.reset_index()

            # Create the table with the index column as the primary key
            cursor = conn.cursor()

            cursor.execute(f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
        """)
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            # Create the table with the index column as the primary key
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS stock_prices (
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER
                );
                """
            cursor.execute(create_table_query)

        # Insert the data into the table (append if it exists)
        df_with_index.to_sql(table_name, conn, if_exists='append', index=False)

    def load_table_to_df(self, table_name):
        """
        Load a SQL table into a DataFrame.

        :param table_name: Name of the SQL table.
        :return: DataFrame containing the table data.
        """
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql(f"SELECT * FROM {table_name}", conn, index_col=0)