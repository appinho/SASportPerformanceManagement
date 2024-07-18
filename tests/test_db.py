import mysql.connector

from config import MYSQL_CONFIG


def test_db_connection():

    assert MYSQL_CONFIG["user"] == "appinho"

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
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        assert False


def test_read():

    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sport")
        sports = cursor.fetchall()
        print(f"Sports {sports}")
        assert len(sports) > 1

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error reading: {err}")
        assert False


test_db_connection()
test_read()
