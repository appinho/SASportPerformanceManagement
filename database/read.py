import logging
from datetime import datetime

import mysql.connector

from database.connect import get_db_connection

dummy_data = [
    (datetime(2024, 4, 1).date(), 20, 30),
    (datetime(2024, 5, 1).date(), 23, 29),
    (datetime(2024, 6, 1).date(), 27, 33),
    (datetime(2024, 7, 1).date(), 26, 34),
]


def get_vo2max():
    try:
        conn = get_db_connection()
    except Exception as err:
        logging.error(f"Error getting dummy data: {err}")
        return dummy_data

    if conn is None:
        return dummy_data
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT x, y FROM plot_data")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as err:
        logging.error(f"Error getting dummy data: {err}")
        return dummy_data


def get_sports():
    sports = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Sports")
        data = cursor.fetchall()
        sports = {d[1]: d[0] for d in data}
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        logging.error(f"Error getting sports: {err}")
    return sports


# def get_vo2max():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT date,value,sport_id FROM Vo2Max')
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return data

#     except mysql.connector.Error as err:
#         logging.error(f"Error getting Vo2Max data: {err}")
#         raise mysql.connector.Error(msg=err)
