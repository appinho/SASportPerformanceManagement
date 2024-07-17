# import plotly.express as px
import plotly.graph_objects as go
import logging

def plot_df(df):
    logging.info("Plot df...")
    df_running = df[df["sport"] == "Running"].dropna()
    df_cycling = df[df["sport"] == "Cycling"].dropna()
    # fig = px.line(df_running, x='date', y='value', title='VO2Max Running')
    fig = go.Figure()

    # Add the first line
    fig.add_trace(
        go.Scatter(
            x=df_running["date"],
            y=df_running["value"],
            mode="lines",
            name="VO2Max Running",
        )
    )

    # Add the second line
    fig.add_trace(
        go.Scatter(
            x=df_cycling["date"],
            y=df_cycling["value"],
            mode="lines",
            name="VO2Max Cycling",
        )
    )

    fig.update_layout(
        title="VO2 Max", xaxis_title="Date", yaxis_title="VO2 Max (ml/min/kg)"
    )
    logging.info("Plot df successfully")
    return fig
