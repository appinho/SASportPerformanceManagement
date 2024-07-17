from flask import render_template
from app.main import bp
from app.utils import plot_to_html
import mysql.connector
from config import MYSQL_CONFIG


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/plot')
def plot():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Fetch x and y points from MySQL
        cursor.execute('SELECT x, y FROM plot_data')
        data = cursor.fetchall()

        # Close connection
        cursor.close()
        conn.close()

        # Convert MySQL data to lists of x and y points
        x_points = [row[0] for row in data]
        y_points = [row[1] for row in data]

        # Generate plot HTML
        plot_html = plot_to_html(x_points, y_points)

        return render_template('plot.html', plot_html=plot_html)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        # Handle error gracefully, maybe render an error page
        return render_template('error.html')