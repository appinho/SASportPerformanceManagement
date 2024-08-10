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
import os
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator

matplotlib.use("Agg")

colors = {}
colors["Running"] = "red"
colors["Cycling"] = "green"
colors["Swimming"] = "blue"


def plot_vo2max_to_html(vo2maxs):
    # Create a plot
    fig, ax = plt.subplots()
    for sport, vo2max in vo2maxs.items():
        ax.plot(vo2max["x"], vo2max["y"], marker='o', label=sport, color=colors[sport])
    ax.xaxis.set_major_locator(WeekdayLocator(byweekday=1))
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    ax.tick_params(axis='x', rotation=45)
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

# def plot_interactive(vo2maxs):
#   import plotly.graph_objects as go
#     # Create figure
#     fig = go.Figure()

#     for sport, vo2max in vo2maxs.items():
#         fig.add_trace(
#             go.Scatter(x=list(vo2max["x"]), y=list(vo2max["y"]), text=sport, fillcolor=colors[sport], name=sport))

#     # Set title
#     fig.update_layout(
#         title_text="V02Max"
#     )

#     # Add range slider
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1,
#                         label="1m",
#                         step="month",
#                         stepmode="backward"),
#                     dict(count=1,
#                         label="YTD",
#                         step="year",
#                         stepmode="todate"),
#                 ])
#             ),
#             rangeslider=dict(
#                 visible=True
#             ),
#             type="date"
#         )
#     )

    # fig.show()
    # # Save plot to BytesIO object
    # img = BytesIO()
    # # fig.savefig(img, format="png")
    # # if not os.path.exists("images"):
    # #     os.mkdir("images")

    # fig.write_image(img)

    # img.seek(0)

    # Encode plot to base64
    # plot_url = base64.b64encode(img.getvalue()).decode("utf8")

    # Return plot as HTML image tag
    # return f'<img src="data:image/png;base64,{plot_url}" />'