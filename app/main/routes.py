# Define routes and views


from datetime import datetime, timedelta

from flask import render_template, request

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
    # Generate plot HTML
    plot_html = plot_vo2max_to_html(data)
    return render_template("plot.html", plot_html=plot_html)

@bp.route('/plot_interactive', methods=['GET'])
def plot_interactive():
    data = get_vo2max()  # Fetch data dynamically

    sports = request.args.getlist('sport')
    date_filter = request.args.get('filter', 'all')

    # If no sport is selected, default to 'Running' and 'Cycling'
    if not sports:
        sports = ['Running', 'Cycling']

    # Filter the selected sports
    dfs = {}
    for sport in sports:
        if sport in data:
            df = data[sport].copy()
            if date_filter == 'this_year':
                start_date = datetime(datetime.now().year, 1, 1)
                end_date = datetime.now()
            elif date_filter == 'last_4_weeks':
                end_date = datetime.now()
                start_date = end_date - timedelta(weeks=4)
            else:
                start_date = df['date'].min()
                end_date = df['date'].max()

            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            dfs[sport] = df
    plot_html = plot_vo2max_to_html(dfs, date_filter)

    return render_template('plot_interactive.html', plot_html=plot_html, sports=sports)
