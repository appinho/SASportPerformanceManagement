import logging

import mysql.connector

from config import MYSQL_CONFIG


def get_db_connection():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None
