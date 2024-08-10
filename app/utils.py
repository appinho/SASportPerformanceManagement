
import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator, WeekdayLocator, YearLocator

matplotlib.use("Agg")

colors = {}
colors["Running"] = "red"
colors["Cycling"] = "green"
colors["Swimming"] = "blue"


def plot_vo2max_to_html(vo2maxs, date_filter=""):
    # Create a plot
    fig, ax = plt.subplots()
    for sport, vo2max in vo2maxs.items():
        ax.plot(vo2max.date, vo2max.value, marker='o', label=sport, color=colors[sport])
    if date_filter == "this_year":
        ax.xaxis.set_major_locator(MonthLocator(bymonthday=1))
        ax.xaxis.set_major_formatter(DateFormatter("%b"))
    elif date_filter == "last_4_weeks":
        ax.xaxis.set_major_locator(WeekdayLocator(byweekday=1))
        ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    else:
        ax.xaxis.set_major_locator(YearLocator(base=1))
        ax.xaxis.set_major_formatter(DateFormatter("%Y"))

    # ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel("Date")
    ax.set_ylabel("VO2Max")
    ax.set_title("VO2Max")
    ax.legend()
    ax.grid(True)

    # Save plot to BytesIO object
    img = BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    # Encode plot to base64
    plot_url = base64.b64encode(img.getvalue()).decode("utf8")

    # Return plot as HTML image tag
    return f'<img src="data:image/png;base64,{plot_url}" />'


def plot_dummy_data_to_html(x_points, y_points):

    # Create a plot
    fig, ax = plt.subplots()
    ax.plot(x_points, y_points)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Dummy data")

    # Save plot to BytesIO object
    img = BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    # Encode plot to base64
    plot_url = base64.b64encode(img.getvalue()).decode("utf8")

    # Return plot as HTML image tag
    return f'<img src="data:image/png;base64,{plot_url}" />'
