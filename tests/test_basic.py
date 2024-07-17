import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

def test_mysql_connection():
    mysql_config = {
        'host': os.getenv('MYSQL_HOST'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        # 'database': os.getenv('MYSQL_DATABASE'),
    }
    assert mysql_config['user'] == "appinho"
    assert mysql_config['host'] == "appinho.mysql.pythonanywhere-services.com"

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        results = cursor.fetchall()
        for rows in results:
            print(rows)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        assert False

test_mysql_connection()