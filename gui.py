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
            """
            <h1 class="title is-4">Future Projections of Precipitation for Alaska Infrastructure</h1>
            <p>Explore projected maximum precipitation events across Alaska. Choose a location by clicking the map or 
            manually entering the latitude and longitude to see precipitation projection tables below.</p>
            """
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
        attributionControl=False,
        maxBounds=[[47.87, -194.72], [72.29, -125.20]],
        scrollWheelZoom=False,
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
    ],
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

right_column = [timerange_dropdown, units_radio, lat_lon_inputs]

main_section = wrap_in_section(
    html.Div(
        children=[
            html.Div(
                className="columns",
                children=[
                    html.Div(className="column", children=alaska_map),
                    html.Div(className="column", children=right_column),
                ],
            ),
        ]
    )
)

above_tables = html.Div(
    id="above_tables",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
                <h1 class="title is-5">What am I looking at?</h1>
                <p>Each grid cell returns the maximum expected precipitation at your selected location over the duration
                specified for that row (60 minutes to 60 days), at a frequency specified for that column (per two year 
                to per thousand years). For example for 66.55N, 149.19W a value of .5 inches is returned for the top 
                left cell: once every two years a precipitation event of .5 inches (rain-water equivalent) over a 1 
                hour period is expected. A 95% confidence interval is shown below the returned value.</p>
                """
        )
    ],
)

below_tables = html.Div(
    id="below_tables",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
                <h1 class="title is-5">About the data</h1>
                <p>Initial inputs into the models and historical data are based on NOAA Atlas 14 data, which provide 
                the best available historical point precipitation frequency estimates, and adjusted to account for 
                climate change using two different Global Circulation Models. The Representative Concentration Pathway 
                (RCP) 8.5 scenario was used for modeling projected data because it most closely matches current trends. 
                Modeled and historical data are downscaled using delta downscaling techniques to remove model bias. 
                Read more about SNAP’s downscaling techniques on the 
                <a href="https://uaf-snap.org/methods-overview/downscaling/">SNAP Website's page on downscaling</a>.</p>
                <br/>
                """
        ),
        ddsih.DangerouslySetInnerHTML(
            f"""
                <h1 class="title is-5">About the models: GFDL-CM3 and NCAR-CCSM4</h1>
                <p>Climate models can only estimate conditions based on the best available data, but each makes 
                different assumptions. This tool uses two of the top-performing models, giving users a chance to 
                explore a model that projects greater changes in temperature (GFDL model), and one that is more 
                conservative (NCAR model). Find more information on the models chosen for this tool in the Final 
                Report.</p>
                <br/>
                <p>The data produced for this project can be 
                <a href="http://ckan.snap.uaf.edu">accessed and downloaded</a> in full through our online 
                data portal.</p>
                <br/>
                """
        ),
    ],
)

data_table = wrap_in_section(
    dcc.Loading(
        id="loading-1",
        children=[
            above_tables,
            html.Div(id="pf-data-tables", className="tabContent"),
            below_tables,
        ],
        type="default",
        className="loading-cube",
    ),
    section_classes="tables",
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
            <p>The DOT Precipitation Frequency Tool was developed by the <a href="https://uaf-snap.org">Scenarios Network for Alaska & Arctic Planning (SNAP)</a> and <a href="http://www.neptuneinc.org/">Neptune Inc.</a> from data provided by the National Weather Service Atlas 14 system and climitalogical forecast data generated by Peter Bieniek of UAF. This website was developed by the <a href="https://uaf-snap.org/">Scenarios Network of Alaska & Arctic Planning</a>, research groups at the <a href="https://uaf-iarc.org/">International Arctic Research Center (IARC)</a> at the <a href="https://uaf.edu/uaf/">University of Alaska Fairbanks (UAF)</a>.</p>
            <p>Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
        </div>
    </div>
</div>
            """
        ),
    ],
)

layout = html.Div(children=[header, about, main_section, data_table, footer])
