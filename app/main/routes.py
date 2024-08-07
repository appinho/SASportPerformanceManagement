# Define routes and views

from flask import render_template

from app.main import bp
from app.utils import plot_interactive, plot_vo2max_to_html
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

    # Generate plot HTML
    plot_html = plot_interactive(data)
    return render_template("plot.html", plot_html=plot_html)
