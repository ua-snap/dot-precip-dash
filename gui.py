# pylint: disable=C0103,C0301,E0401,R0913,W0603
"""
GUI for app
"""

import os
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import dash_leaflet as dl

# For hosting
path_prefix = os.getenv("REQUESTS_PATHNAME_PREFIX") or "/"


# Helper functions
def wrap_in_section(content, section_classes="", container_classes="", div_classes=""):
    """
    Helper function to wrap sections.
    Accepts an array of children which will be assigned within
    this structure:
    <section class="section">
        <div class="container">
            <div>[children]...
    """
    return html.Section(
        className="section " + section_classes,
        children=[
            html.Div(
                className="container " + container_classes,
                children=[html.Div(className=div_classes, children=content)],
            )
        ],
    )


def wrap_in_field(label, control, className=""):
    """
    Returns the control wrapped
    in Bulma-friendly markup.
    """
    return html.Div(
        className="field " + className,
        children=[
            html.Label(label, className="label"),
            html.Div(className="control", children=control),
        ],
    )


header = ddsih.DangerouslySetInnerHTML(
    f"""
<div class="container">
<nav class="navbar" role="navigation" aria-label="main navigation">

  <div class="navbar-brand">
    <a class="navbar-item" href="https://uaf-snap.org">
      <img src="{path_prefix}assets/snap_acronym.svg">
    </a>

    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div class="navbar-menu">

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a href="https://uaf-iarc.typeform.com/to/mN7J5cCK#tool=DOT%20Precipitation%20Forecast%20Tool" class="button is-link" target="_blank">
            Feedback
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</div>
"""
)

about = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            "<h1 class='title is-3'>DOT Precipitation Application</h1>"
        )
    ],
    section_classes="lead",
    div_classes="content is-size-5",
)


alaska_map = html.Div(
    dl.Map(
        [dl.TileLayer(), dl.LayerGroup(id="layer")],
        id="ak-map",
        zoom=4,
        center=(62.5, -160),
        minZoom=4,
        maxZoom=8,
        maxBounds=[[47.87, -194.72], [72.29, -125.20]],
        style={"width": "800px", "height": "600px"},
    )
)
timerange_dropdown = wrap_in_field(
    "Choose timerange for returned data",
    dcc.Dropdown(
        id="timeslice-dropdown",
        options=[
            {"label": "2020-2049", "value": "2020-2049"},
            {"label": "2050-2079", "value": "2050-2079"},
            {"label": "2080-2099", "value": "2080-2099"},
        ],
        value="2020-2049",
    ),
    className="timerange",
)
lat_lon_inputs = html.Div(
    children=[
        wrap_in_field(
            "Latitude",
            dcc.Input(id="lat-input", type="number", placeholder="Enter latitude"),
        ),
        wrap_in_field(
            "Longitude",
            dcc.Input(id="lon-input", type="number", placeholder="Enter longitude"),
        ),
        html.Button("Submit", id="submit-lat-lon", n_clicks=0),
    ],
    className="lat_lon_div",
)
units_radio = wrap_in_field(
    "Choose returned units",
    dcc.RadioItems(
        id="units-radio",
        options=[
            {"label": "Imperial Units", "value": "imperial"},
            {"label": "Metric Units", "value": "metric"},
        ],
        value="imperial",
        labelClassName="label_spacing",
    ),
    className="units",
)

data_table = wrap_in_section(
    dcc.Loading(
        id="loading-1",
        children=[html.Div(id="pf-data-tables", className="tabContent")],
        type="cube",
        className="loading-cube",
    ),
    section_classes="tables",
)

left_column = [html.H5("Choose a point on the map of Alaska"), alaska_map]

right_column = [timerange_dropdown, units_radio, lat_lon_inputs]

main_section = wrap_in_section(
    html.Div(
        className="columns",
        children=[
            html.Div(className="column", children=left_column),
            html.Div(className="column", children=right_column),
        ],
    )
)


# Used in copyright date
current_year = datetime.now().year

footer = html.Footer(
    className="footer",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
<div class="container">
    <div class="wrapper is-size-6">
        <img src="{path_prefix}assets/UAF.svg"/>
        <div class="wrapped">
            <p>The DOT Precipitation Frequency Tool was developed by the Scenarios Network for Alaska & Arctic Planning (SNAP) and Neptune Inc. from data provided by the National Weather Service Atlas 14 system and climitalogical forecast data generated by Peter Bieniek of UAF. This website was developed by the <a href="https://uaf-snap.org/">Scenarios Network of Alaska & Arctic Planning</a>, research groups at the <a href="https://uaf-iarc.org/">International Arctic Research Center (IARC)</a> at the <a href="https://uaf.edu/uaf/">University of Alaska Fairbanks (UAF)</a>.</p>
            <p>Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
        </div>
    </div>
</div>
            """
        ),
    ],
)

layout = html.Div(children=[header, main_section, data_table, footer])
