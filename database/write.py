# import logging

# from database.connect import get_db_connection
from database.read import get_sports


def write_vo2max(data):

    sports = get_sports()
    print(sports)
    return
    # # Table name
    # table_name = 'VO2Max'

    # # Get column names
    # columns = ', '.join(data.keys())

    # # Generate insert queries
    # insert_queries = []
    # for row in zip(*data.values()):
    #     values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in row])
    #     query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    #     insert_queries.append(query)

    # # Print insert queries
    # for query in insert_queries:
    #     print(query)
    # return
    # try:
    #     conn = get_db_connection()
    # except Exception as err:
    #     logging.error(f"Error getting dummy data: {err}")

    # try:
    #     cursor = conn.cursor()
    #     for query in insert_queries:
    #         cursor.execute('SELECT x, y FROM plot_data')
    #     data = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return data
    # except mysql.connector.Error as err:
    #     logging.error(f"Error getting dummy data: {err}")
    #     return dummy_data
