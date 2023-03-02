# pylint: disable=C0103,C0301,E0401,R0913,W0603
"""
GUI for app
"""

import os
from datetime import datetime
from dash import dcc, html
import dash_dangerously_set_inner_html as ddsih
import dash_leaflet as dl

# For hosting
path_prefix = os.getenv("DASH_REQUESTS_PATHNAME_PREFIX") or "/"


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
          <a href="https://uaf-iarc.typeform.com/to/mN7J5cCK#tool=Future%20Projections%20of%20Precipitation%20for%20Alaska" class="button is-link" target="_blank">
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
            <h1 class="title is-3">Future Projections of Precipitation for Alaska Infrastructure</h1>
            <p class="is-size-5">Explore projected maximum precipitation events across Alaska. Choose a location by clicking the map or
            manually entering the latitude and longitude, then scroll down to see precipitation projection tables below.  Note: it could take up to three minutes to retrieve data for a selected point.</p>
            """
        )
    ],
    section_classes="words-block-grey",
    div_classes="content",
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
    "Choose time range for returned data",
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
            {"label": "Inches", "value": "imperial"},
            {"label": "Millimeters", "value": "metric"},
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
    ),
    section_classes="roomy",
)

nan_values = html.Div(
    id="nan_values",
    className="is-size-5",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
                <h3 class="title is-4">⚠️ Selected location is outside of this data set</h3>
                <p>Sorry, but the place you selected isn't included in this data set. This data set is limited to the
                land area of the U.S. state of Alaska. Please select a valid point.</p>
                """
        )
    ],
)

above_tables = html.Div(
    id="above_tables",
    className="is-size-5",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
                    <h3 class="title is-4">What am I looking at?</h3>
                    <p>Each table entry below returns the maximum expected precipitation at your selected location over the duration
                    specified for that row (60 minutes to 60 days), at a frequency specified for that column (per two year
                    to per thousand years). For example for 66.55N, 149.19W a value of 0.49 inches is shown for the top
                    left cell: once every two years a precipitation event of 0.49 inches (rain-water equivalent) over a 1
                    hour period would be expected. A 95% confidence interval is shown below the returned value.</p>
            """
        )
    ],
)


data_table = wrap_in_section(
    html.Div(
        children=[
            dcc.Loading(
                children=[
                    nan_values,
                    above_tables,
                    html.Div(id="pf-data-tables"),
                ],
                type="default",
                className="loading-cube",
            )
        ],
    ),
    container_classes="content",
)

explainer_section = wrap_in_section(
    html.Div(
        className="is-size-5",
        children=[
            ddsih.DangerouslySetInnerHTML(
                f"""
                <h3 class="title is-4">About the data</h3>
                <p>Initial inputs into the models and historical data are based on NOAA Atlas 14 data, which provide
                the best available historical point precipitation frequency estimates, and adjusted to account for
                climate change using two different Global Circulation Models. The Representative Concentration Pathway
                (RCP) 8.5 scenario was used for modeling projected data because it most closely matches current trends.
                This data set was developed using dynamically downscaled data from the Weather Research and Forecasting (WRF) model, and <a href="http://ckan.snap.uaf.edu/dataset/historical-and-projected-dynamically-downscaled-climate-data-for-the-state-of-alaska-and-surrou">are available here</a>.
                Read more about the Scenario Network for Alaska and Arctic Data (SNAP) downscaling techniques on the
                <a href="https://uaf-snap.org/methods-overview/downscaling/">SNAP website page on downscaling</a>.</p>
                <p>Source code used to generate this data can be found on <a href="https://github.com/ua-snap/precip-dot">GitHub</a>, and the data produced for this project (as well as additional metadata and information about this data set) can be
                <a href="http://ckan.snap.uaf.edu/dataset/annual-maximum-precipitation-projections-for-alaska">accessed and downloaded</a> in full through our online
                data portal.</p>
                <h3 class="title is-5">About the models: GFDL-CM3 and NCAR-CCSM4</h3>
                <p>Climate models can only estimate conditions based on the best available data, but each makes
                different assumptions. This tool uses two of the top-performing models, giving users a chance to
                explore a model that projects greater changes in precipitation (GFDL model), and one that projects
                moderate changes (NCAR model). Find more information on the models chosen for this tool in the Final
                Report, linked from <a href="https://uaf-snap.org/project/future-projections-of-precipitation-for-alaska-infrastructure/">this page describing this project</a>.</p>
                """
            )
        ],
    ),
    section_classes="words-block-grey",
    container_classes="content",
)

# Used in copyright date
current_year = datetime.now().year

footer = html.Footer(
    className="footer",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
<footer class="container">
    <div class="wrapper is-size-6">
        <img src="{path_prefix}assets/UAF.svg"/>
        <div class="wrapped">
            <p>This tool was developed by the <a href="https://uaf-snap.org">Scenarios Network for Alaska & Arctic Planning (SNAP)</a> and <a href="http://www.neptuneinc.org/">Neptune Inc.</a> from data provided by the National Weather Service Atlas 14 system and climatological forecast data generated by Peter Bieniek of the University of Alaska Fairbanks. Additional funding and support for this project was provided by the <a href="https://uaf-accap.org/">Alaska Center for Climate Assessment and Policy</a>. SNAP is a research group at the <a href="https://uaf-iarc.org/">International Arctic Research Center (IARC)</a> at the <a href="https://uaf.edu/uaf/">University of Alaska Fairbanks (UAF)</a>.</p>
            <p>Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a> and <a href="https://www.alaska.edu/records/records/compliance/gdpr/ua-privacy-statement/">Privacy Statement</a>.</p>
            <p>UA is committed to providing accessible websites. <a href="https://www.alaska.edu/webaccessibility/">Learn more about UA&rsquo;s notice of web accessibility</a>.  If we can help you access this website&rsquo;s content, <a href="mailto:uaf-snap-data-tools@alaska.edu">email us!</a></p>

        </div>
    </div>
</footer>
            """
        ),
    ],
)

layout = html.Div(
    children=[header, about, main_section, data_table, explainer_section, footer]
)
