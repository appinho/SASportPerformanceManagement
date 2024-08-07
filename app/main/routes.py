# Define routes and views

from flask import render_template

from app.main import bp
from app.utils import plot_vo2max_to_html
from database.read import get_vo2max


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/plot")
def plot():
    try:
        data = get_vo2max()
    except Exception as err:
        return render_template("error.html", error_message=str(err))

    # Convert MySQL data to lists of x and y points
    x_points = [row[0] for row in data]
    y_running = [row[1] for row in data]
    y_cycling = [row[2] for row in data]

    # Generate plot HTML
    plot_html = plot_vo2max_to_html(x_points, y_running, y_cycling)
    return render_template(
        "plot.html", plot_html=plot_html
    )  #     return render_template('plot.html', plot_html=plot_html)#     plot_html = plot_vo2max_to_html(x_points, y_running, y_cycling)
