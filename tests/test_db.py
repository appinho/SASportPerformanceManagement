import mysql.connector
from config import MYSQL_CONFIG
import logging

logging.basicConfig(level=logging.INFO)

def test_db_connection():

    assert MYSQL_CONFIG['user'] == "appinho"

    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        logging.info(f"Databases {databases}")
        assert len(databases) > 1
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        logging.info(f"Tables {tables}")
        assert len(tables) > 0
        cursor.execute("SELECT * FROM plot_data")
        datapoints = cursor.fetchall()
        logging.info(f"Datapoints {datapoints}") 
        assert len(datapoints) > 1

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        assert False

test_db_connection()