from flask import render_template
from app.main import bp
from app.utils import plot_to_html
import mysql.connector
from config import MYSQL_CONFIG
import logging

def get_db_connection():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None

def get_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT x, y FROM plot_data')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    except mysql.connector.Error as err:
        logging.error(f"Error getting data from MySQL: {err}")
        return None

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/plot')
def plot():

    try:
        logging.warning(f"Connect for user: {MYSQL_CONFIG['user']}")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT x, y FROM plot_data')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return render_template('error.html', error_message=str(err))
    

    # Convert MySQL data to lists of x and y points
    x_points = [row[0] for row in data]
    y_points = [row[1] for row in data]

    # Generate plot HTML
    plot_html = plot_to_html(x_points, y_points)
    return render_template('plot.html', plot_html=plot_html)