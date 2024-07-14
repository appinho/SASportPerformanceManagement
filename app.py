from flask import Flask, render_template_string

from database.read import get_dataframe_from_db, get_tables_from_db
from viz.graph import plot_df

app = Flask(__name__)


@app.route("/")
def index():
    # Get the dataframe
    tables = get_tables_from_db()
    print(tables)
    df = get_dataframe_from_db()
    print("Dataframe fetched")

    if df.empty:
        return "No data available or error fetching data"

    # Plot the data using Plotly
    try:
        fig = plot_df(df)

        # Generate HTML for the plot
        plot_html = fig.to_html(full_html=False)

        # Render the HTML
        return render_template_string(
            """
        <html>
            <head>
                <title>Plotly Plot</title>
            </head>
            <body>
                <h1>Data Analytics</h1>
                <div>{{ plot_div|safe }}</div>
            </body>
        </html>
        """,
            plot_div=plot_html,
        )
    except Exception as e:
        print(f"Error creating plot: {e}")
        return "Error creating plot"


if __name__ == "__main__":
    app.run(debug=True)
