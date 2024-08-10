import logging
from datetime import datetime

import mysql.connector
import pandas as pd

from database.connect import get_db_connection

start_date = '2023-01-01'
end_date = datetime.today().strftime('%Y-%m-01')
date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
dummy_data = {}
dummy_data["Running"] = pd.DataFrame({'date': date_range, 'value': [10 + i for i in range(len(date_range))]}) #, index=date_range)
dummy_data["Cycling"] = pd.DataFrame({'date': date_range, 'value': [24 - i for i in range(len(date_range))]}) #, index=date_range)

def get_vo2max():
    try:
        conn = get_db_connection()
    except Exception as err:
        logging.error(f"Error establishing connection to database: {err}")
        return dummy_data

    if conn is None:
        return dummy_data
    try:
        sports = get_sports()
        vo2maxs = {}
        cursor = conn.cursor()
        for sport_name, sport_id in sports.items():
            cursor.execute(
                f"SELECT v.date, v.value FROM VO2Max v WHERE sport_id = {sport_id} ORDER BY v.date"
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=columns)
            vo2maxs[sport_name] = df

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
