import sqlite3

# import mysql.connector
import pandas as pd

from database.config import db_config, db_path


def get_dataframe_from_db(db_type="sqlite3"):
    try:
        # Connect to the database
        print(f"Use {db_type}")
        if db_type == "sqlite3":
            conn = sqlite3.connect(db_path)
        # elif db_type == "mysql":
        #     conn = mysql.connector.connect(**db_config)
        else:
            raise NotImplementedError(f"Unknown database type: {db_type}")
        print("Database connection successful")

        # Query the database
        query = "SELECT * FROM Vo2max"

        # Read the data into a pandas DataFrame
        df = pd.read_sql(query, conn)
        print("Dataframe loaded successfully")

        # Close the connection
        conn.close()
        print("Database connection closed")

        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()  # Return an empty dataframe on error


def get_tables_from_db():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        print("Database connection successful")

        # Query to get all tables
        query = "SELECT name FROM sqlite_master WHERE type='table';"

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        print(tables)

        # Close the connection
        conn.close()
        print("Database connection closed")

        return [table[0] for table in tables]
    except Exception as e:
        print(f"Error: {e}")
        return []
