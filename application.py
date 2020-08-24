# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import datetime
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import flask
from gui import layout, path_prefix
from data import fetch_data
import luts

app = dash.Dash(__name__, requests_pathname_prefix=path_prefix)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server
app.index_string = luts.index_string
app.title = luts.title
app.layout = layout


# This function alerts the Flask application that we want to
# access files that are contained within the "downloads" directory.
@app.server.route("/downloads/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, "downloads"), path)


# Input value added to allow for cache to be refreshed after becoming
# invalid from the number of seconds indicated in data.py. This is set to
# 43200 seconds by default.
@app.callback(Output("daily-index", "figure"), [Input("cache_check_input", "value")])
def update_daily_index(nonce):  # deliberate unused arg
    """ Generate precipitation scatter chart """
    # Get date start/end ranges for default window into data.
    start_date = (datetime.date.today() + datetime.timedelta(days=-180)).strftime(
        "%Y-%m-%d"
    )
    end_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d"
    )

    filename = "downloads/statewide_temperature_daily_index.csv"
    di = fetch_data()
    di.drop(columns=["count"]).rename(
        columns={"date": "Date", "daily_index": "Daily Index"}
    ).to_csv(filename, index=False, header=True)
    above = di[di.daily_index > 0]
    below = di[di.daily_index <= 0]

    return go.Figure(
        data=[
            go.Scatter(
                x=di["date"],
                y=di["daily_index"],
                showlegend=False,
                name="Above Average",
                mode="lines",
                fill="tozeroy",
                hoverinfo="none",
                line=dict(shape="spline", width=0.5, color="#ccc"),
            ),
            go.Scatter(
                x=above["date"],
                y=above["daily_index"],
                marker_color=luts.colors[1],
                name="Above Average",
                mode="markers",
                hovertemplate="%{x} <br><b>Daily Index:</b> %{y}",
            ),
            go.Scatter(
                x=below["date"],
                y=below["daily_index"],
                marker_color=luts.colors[0],
                name="Below Average",
                mode="markers",
                hovertemplate="%{x} <br><b>Daily Index:</b> %{y}",
            ),
            go.Scatter(
                x=di["date"],
                y=di["daily_index"].rolling(30).mean().round(2),
                name="30-day average",
                hovertemplate="%{x} <br><b>30-day Average:</b> %{y}",
                line=dict(shape="spline", color="#333"),
            ),
        ],
        layout=go.Layout(
            template=luts.plotly_template,
            title=dict(text="Alaska Statewide Temperature Index"),
            yaxis=dict(showgrid=True, zeroline=True, title=dict(text="Index")),
            xaxis=dict(
                showgrid=True,
                type="date",
                range=[start_date, end_date],
                rangeslider=dict(
                    range=[di["date"].iloc[0], di["date"].iloc[-1]], visible=True
                ),
            ),
        ),
    )


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
