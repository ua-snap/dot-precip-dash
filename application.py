# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
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


def generate_table_data(dt, gcm="GFDL-CM3", ts_str="2020-2049"):
    pf_data_table = []
    for duration in [
        "60m",
        "2h",
        "3h",
        "6h",
        "12h",
        "24h",
        "3d",
        "4d",
        "7d",
        "10d",
        "20d",
        "30d",
        "45d",
        "60d",
    ]:
        pf_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf") / 1000
        )
        pf_values = pf_values.round(decimals=2)

        pf_upper_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf-upper")
            / 1000
        )
        pf_upper_values = pf_upper_values.round(decimals=2)

        pf_lower_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf-lower")
            / 1000
        )
        pf_lower_values = pf_lower_values.round(decimals=2)

        row = []
        row.append(
            html.Th(
                ddsih.DangerouslySetInnerHTML(
                    f"""
                <p align="center">{duration}</p>"""
                )
            )
        )
        for i in range(len(pf_values)):
            row.append(
                html.Td(
                    ddsih.DangerouslySetInnerHTML(
                        f"""
                <p align="center"><b>{pf_values.values[i]}</b></p>
                <p align="center">( <i>{pf_lower_values.values[i]} - {pf_upper_values.values[i]}</i> )</p>
                """
                    )
                )
            )
            # for value in pf_values.values:
            #    row.append(html.Td(value))

        pf_data_table.append(html.Tr(row))

    return pf_data_table


def generate_table(dt, ts_str):
    return [
        html.H3("GFDL-CM3"),
        html.Table(
            id="gfdl-pf-table",
            className="table is-bordered",
            children=[
                html.Tr(
                    children=[
                        html.Th("Duration", rowSpan=2,),
                        html.Th(
                            ddsih.DangerouslySetInnerHTML(
                                f"""
                <p align="center"><b>Average recurrence interval(years)</b></p>"""
                            ),
                            colSpan=9,
                        ),
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th(
                            ddsih.DangerouslySetInnerHTML(
                                f"""<p align="center">{col}</p>"""
                            )
                        )
                        for col in [2, 5, 10, 25, 50, 100, 200, 500, 1000]
                    ]
                ),
                html.Tbody(generate_table_data(dt, "GFDL-CM3", ts_str)),
            ],
        ),
        html.H3("NCAR-CCSM4"),
        html.Table(
            id="ncar-pf-table",
            className="table is-bordered",
            children=[
                html.Tr(
                    children=[
                        html.Th("Duration", rowSpan=2,),
                        html.Th(
                            ddsih.DangerouslySetInnerHTML(
                                f"""
                <p align="center"><b>Average recurrence interval(years)</b></p>"""
                            ),
                            colSpan=9,
                        ),
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th(
                            ddsih.DangerouslySetInnerHTML(
                                f"""<p align="center">{col}</p>"""
                            )
                        )
                        for col in [2, 5, 10, 25, 50, 100, 200, 500, 1000]
                    ]
                ),
                html.Tbody(generate_table_data(dt, "NCAR-CCSM4", ts_str)),
            ],
        ),
    ]


@app.callback(Output("layer", "children"), [Input("ak-map", "click_lat_lng")])
def drop_pin_on_map(click_lat_lng):
    print(click_lat_lng)

    return [
        dl.Marker(
            position=click_lat_lng,
            children=dl.Tooltip("({:.2f}, {:.2f})".format(*click_lat_lng)),
        )
    ]


@app.callback(Output("lat-input", "value"), [Input("ak-map", "click_lat_lng")])
def change_lat(click_lat_lng):
    return round(click_lat_lng[0], 2)


@app.callback(Output("lon-input", "value"), [Input("ak-map", "click_lat_lng")])
def chnage_lat(click_lat_lng):
    return round(click_lat_lng[1], 2)


@app.callback(
    Output("pf-data-tables", "children"),
    [Input("ak-map", "click_lat_lng"), Input("timeslice-dropdown", "value")],
)
def return_pf_data(click_lat_lng, ts_str):
    wgs84 = pyproj.CRS("EPSG:4326")
    epsg3338 = pyproj.CRS("EPSG:3338")
    nad83_lat_lon = pyproj.transform(
        wgs84, epsg3338, click_lat_lng[0], click_lat_lng[1]
    )
    print(ts_str)
    print(nad83_lat_lon)
    pf_data = fetch_data(nad83_lat_lon[0], nad83_lat_lon[1])
    print(pf_data)
    return generate_table(pf_data, ts_str)


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
