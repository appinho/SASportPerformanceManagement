import logging
from datetime import datetime

import mysql.connector

from database.connect import get_db_connection

dummy_data = {}
dummy_data["Running"] = {}
dummy_data["Running"]["x"] = [
    datetime(2024, 4, 1).date(),
    datetime(2024, 5, 1).date(),
    datetime(2024, 6, 1).date(),
]
dummy_data["Running"]["y"] = [50, 52, 55]
dummy_data["Cycling"] = {}
dummy_data["Cycling"]["x"] = [
    datetime(2024, 5, 1).date(),
    datetime(2024, 6, 1).date(),
    datetime(2024, 7, 1).date(),
]
dummy_data["Cycling"]["y"] = [54, 51, 56]


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
        cursor.execute(
            "SELECT v.date, v.value, s.name FROM VO2Max v INNER JOIN Sport s ON v.sport_id = s.id"
        )
        entries = cursor.fetchall()
        vo2maxs = {}
        for entry in entries:
            date = entry[0]
            vo2max = entry[1]
            sport = entry[2]
            if sport not in vo2maxs:
                vo2maxs[sport] = {}
                vo2maxs[sport]["x"] = []
                vo2maxs[sport]["y"] = []
            vo2maxs[sport]["x"].append(date)
            vo2maxs[sport]["y"].append(vo2max)

        cursor.close()
        conn.close()
        return vo2maxs
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
