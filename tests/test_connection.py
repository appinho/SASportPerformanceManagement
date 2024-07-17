import mysql.connector
from config import MYSQL_CONFIG

def test_mysql_connection():

    assert MYSQL_CONFIG['user'] == "appinho"

    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"Databases {databases}")
        assert len(databases) > 1
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables {tables}")
        assert len(tables) > 0
        cursor.execute("SELECT * FROM plot_data")
        datapoints = cursor.fetchall()
        print(f"Datapoints {datapoints}") 
        assert len(datapoints) > 1
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        assert False

test_mysql_connection()