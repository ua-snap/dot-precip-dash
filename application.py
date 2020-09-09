# pylint: disable=C0103,C0301,E0401,R0913,W0603
"""
Template for SNAP Dash apps.
"""
import os
import logging
import dash
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import pyproj
from gui import layout, path_prefix
from data import fetch_api_data, DASH_LOG_LEVEL
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

logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

# Global counts for number of clicks to allow for both map click and lat / lon input
pin_num_clicks = 0
table_num_clicks = 0

# A list of lists containing past lat / lon combinations + associated data array
past_points = []


def generate_table_data(dt, gcm="GFDL-CM3", ts_str="2020-2049", units="imperial"):
    """
    Generates table formatted data from 5-D XArray of PF values to be displayed in the generated table.
    Accepts the following input:
        * dt - The XArray DataArray containing the data returned from the NC files via API call.
        * gcm - String of the global climate model (GCM) desired: GFDL-CM3 or NCAR-CCSM4
        * ts_str - String of the time interval desired: 2020-2049, 2050-2079, or 2080-2099
        * units - String of the units desired: imperial (inches) or metric (mm)

    Returns:
        * Rows <tr> and columns <td> to populate a table containing data from our input.
    """
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
                <p align="center">(<i>{pf_lower_values.sel(interval=interval).values}-{pf_upper_values.sel(interval=interval).values}</i>)</p>
                        """
                    )
                )
            )

        pf_data_table.append(html.Tr(row))

    return pf_data_table


def generate_table(dt, ts_str, units):
    """
    Initializes the data table to be displayed from the 5-D XArray input.
    Accepts the following input:
        * dt - The XArray DataArray containing the data returned from the NC files via API call.
        * ts_str - String of the time interval desired: 2020-2049, 2050-2079, or 2080-2099
        * units - String of the units desired: imperial (inches) or metric (mm)
    Returns:
         * A formatted table containing both GCMs output for a given lat / lon at a given time range
           and in units requested.
    """
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
                                    "<p align='center'><b>Average recurrence interval(years)</b></p>"
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


@app.callback(
    Output("layer", "children"),
    [Input("ak-map", "click_lat_lng"), Input("submit-lat-lon", "n_clicks")],
    [State("lat-input", "value"), State("lon-input", "value")],
)
def drop_pin_on_map(click_lat_lng, n_clicks, lat, lon):
    """
    Places a pin on the map of Alaska given either a click on the map OR
    by entering a lat / lon set and hitting the Submit button.
    Inputs:
        * click_lat_lng - Only generated upon a click on the map. Produces a tuple of (lat, lon)
        * n_clicks - Number of clicks of the Submit button. Updates +1 per click. This allows us to track button clicks.
    States:
        * lat - Only generated when Submit button is pressed. Value is latitude entered into lat-input Input field.
        * lon - Only generated when Submit button is pressed. Value is longitude entered into lon-input Input field.
    Returns:
        * A new marker on the map of Alaska for where was pressed or representing the lat / lon input.
    """
    global pin_num_clicks
    if n_clicks != pin_num_clicks:

        pin_num_clicks = n_clicks
        return [
            dl.Marker(
                position=(lat, lon),
                children=dl.Tooltip("({:.2f}, {:.2f})".format(lat, lon)),
            )
        ]

    return [
        dl.Marker(
            position=click_lat_lng,
            children=dl.Tooltip("({:.2f}, {:.2f})".format(*click_lat_lng)),
        )
    ]


@app.callback(Output("lat-input", "value"), [Input("ak-map", "click_lat_lng")])
def change_lat(click_lat_lng):
    """
    Changes the Input lat-input's value to match the latitude of the clicked point.
    Inputs:
        * click_lat_lng - The latitude and longitude of a clicked place on map of Alaska in tuple (lat, lon)
    Returns:
        * Latitude value rounded to 2 decimal places.
    """
    return round(click_lat_lng[0], 2)


@app.callback(Output("lon-input", "value"), [Input("ak-map", "click_lat_lng")])
def change_lon(click_lat_lng):
    """
    Changes the Input lon-input's value to match the longitude of the clicked point.
    Inputs:
        * click_lat_lng - The latitude and longitude of a clicked place on map of Alaska in tuple (lat, lon)
    Returns:
        * Longitude value rounded to 2 decimal places.
    """
    return round(click_lat_lng[1], 2)


@app.callback(
    Output("pf-data-tables", "children"),
    [
        Input("ak-map", "click_lat_lng"),
        Input("submit-lat-lon", "n_clicks"),
        Input("timeslice-dropdown", "value"),
        Input("units-radio", "value"),
    ],
    [State("lat-input", "value"), State("lon-input", "value")],
)
def return_pf_data(click_lat_lng, n_clicks, ts_str, units, lat, lon):
    """
    Main function for generating the PF tables given all of the available inputs from the web application.
    Inputs:
        * click_lat_lng - Only generated upon a click on the map. Produces a tuple of (lat, lon)
        * n_clicks - Number of clicks of the Submit button. Updates +1 per click. This allows us to track button clicks.
    States:
        * lat - Only generated when Submit button is pressed. Value is latitude entered into lat-input Input field.
        * lon - Only generated when Submit button is pressed. Value is longitude entered into lon-input Input field.
    Returns:
        * A formatted table containing both GCMs output for a given lat / lon at a given time range
           and in units requested.
    """
    global table_num_clicks

    wgs84 = pyproj.CRS("EPSG:4326")
    epsg3338 = pyproj.CRS("EPSG:3338")

    if n_clicks != table_num_clicks:
        table_num_clicks = n_clicks

        for point in past_points:
            if point[0] == lat and point[1] == lon:
                logging.info(
                    "Using cached data for latitude %s and longitude %s", lat, lon
                )
                return generate_table(point[2], ts_str, units)

        nad83_lat_lon = pyproj.transform(wgs84, epsg3338, lat, lon)

        pf_data = fetch_api_data(nad83_lat_lon[0], nad83_lat_lon[1])
        past_points.append([lat, lon, pf_data])

    else:
        click_lat = round(click_lat_lng[0], 2)
        click_lon = round(click_lat_lng[1], 2)
        for point in past_points:
            if point[0] == click_lat and point[1] == click_lon:
                logging.info(
                    "Using cached data for latitude %s and longitude %s", lat, lon
                )
                return generate_table(point[2], ts_str, units)

        nad83_lat_lon = pyproj.transform(wgs84, epsg3338, click_lat, click_lon)

        pf_data = fetch_api_data(nad83_lat_lon[0], nad83_lat_lon[1])
        past_points.append([click_lat, click_lon, pf_data])

    return generate_table(pf_data, ts_str, units)


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG") or False, port=8080)
