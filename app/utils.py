# Utility functions data processing or plotting


# import seaborn as sns
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

# import plotly.graph_objs as go
# import plotly.io as pio

# def plot_dummy_to_html():
#     fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
#     plot_html = pio.to_html(fig, full_html=False)
#     return plot_html


# def plot_dummy_to_html():
#     # Example data
#     tips = sns.load_dataset('tips')

#     # Create a seaborn plot
#     fig, ax = plt.subplots()
#     sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax)

#     # Save the plot to a BytesIO object
#     img = BytesIO()
#     fig.savefig(img, format='png')
#     img.seek(0)

#     # Encode the image to base64
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')

#     # Return the plot as an HTML image tag
#     return f'<img src="data:image/png;base64,{plot_url}" />'


import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator

matplotlib.use("Agg")


def plot_vo2max_to_html(x_points, y_running, y_cycling):

    # Create a plot
    fig, ax = plt.subplots()
    ax.plot(x_points, y_running, label="Running", color="red")
    ax.plot(x_points, y_cycling, label="Cycling", color="green")
    ax.xaxis.set_major_locator(MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
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
