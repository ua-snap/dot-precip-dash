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
import dash_leaflet as dl
import pyproj
import luts

app = dash.Dash(
    __name__, requests_pathname_prefix=path_prefix, prevent_initial_callbacks=True
)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server
app.index_string = luts.index_string
app.title = luts.title
app.layout = layout


@app.callback(Output("layer", "children"), [Input("ak-map", "click_lat_lng")])
def drop_pin_on_map(click_lat_lng):
    print(click_lat_lng)

    return [
        dl.Marker(
            position=click_lat_lng,
            children=dl.Tooltip("({:.2f}, {:.2f})".format(*click_lat_lng)),
        )
    ]


@app.callback(Output("pf-table", "pf_data"), [Input("ak-map", "click_lat_lng")])
def return_pf_data(click_lat_lng):
    wgs84 = pyproj.CRS("EPSG:4326")
    epsg3338 = pyproj.CRS("EPSG:3338")
    nad83_lat_lon = pyproj.transform(
        wgs84, epsg3338, click_lat_lng[0], click_lat_lng[1]
    )
    print(nad83_lat_lon)
    pf_data = fetch_data(nad83_lat_lon[0], nad83_lat_lon[1])
    print(pf_data)
    return pf_data


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
