# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import dash
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
from dash.dependencies import Input, Output
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


def generate_table_data(dt, gcm="GFDL-CM3", ts_str="2020-2049", units="imperial"):
    pf_data_table = []
    for duration in luts.DURATIONS:
        # All of the PF values are in 1000th of an inch
        pf_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf") / 1000
        )

        pf_upper_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf-upper")
            / 1000
        )

        pf_lower_values = (
            dt.sel(gcm=gcm, duration=duration, timerange=ts_str, variable="pf-lower")
            / 1000
        )

        if units == "metric":
            pf_values = pf_values * 25.4
            pf_upper_values = pf_upper_values * 25.4
            pf_lower_values = pf_lower_values * 25.4

        pf_values = pf_values.round(decimals=2)
        pf_upper_values = pf_upper_values.round(decimals=2)
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
        for interval in luts.INTERVALS:
            row.append(
                html.Td(
                    ddsih.DangerouslySetInnerHTML(
                        f"""
                <p align="center"><b>{pf_values.sel(interval=interval).values}</b></p>
                <p align="center">( <i>{pf_lower_values.sel(interval=interval).values} - {pf_upper_values.sel(interval=interval).values}</i> )</p>
                        """
                    )
                )
            )

        pf_data_table.append(html.Tr(row))

    return pf_data_table


def generate_table(dt, ts_str, units):
    table = []
    for gcm in dt.coords["gcm"].values:
        table.append(
            html.Table(
                id=f"""{gcm}-pf-table""",
                className="table is-bordered",
                children=[
                    html.Tr(
                        html.Th(
                            ddsih.DangerouslySetInnerHTML(
                                f"""<p align="center">Data for model {gcm} for time range {ts_str} in {"millimeters" if units == "metric" else "inches"}</p>"""
                            ),
                            colSpan=11,
                        ),
                    ),
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
                                    f"""<p align="center">{int(col)}</p>"""
                                )
                            )
                            for col in luts.INTERVALS
                        ]
                    ),
                    html.Tbody(generate_table_data(dt, gcm, ts_str, units)),
                ],
            ),
        )

    return table


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
    [
        Input("ak-map", "click_lat_lng"),
        Input("timeslice-dropdown", "value"),
        Input("units-radio", "value"),
    ],
)
def return_pf_data(click_lat_lng, ts_str, units):
    wgs84 = pyproj.CRS("EPSG:4326")
    epsg3338 = pyproj.CRS("EPSG:3338")
    nad83_lat_lon = pyproj.transform(
        wgs84, epsg3338, click_lat_lng[0], click_lat_lng[1]
    )
    print(ts_str)
    print(nad83_lat_lon)
    pf_data = fetch_data(nad83_lat_lon[0], nad83_lat_lon[1])
    print(pf_data)
    table = generate_table(pf_data, ts_str, units)
    return table


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
