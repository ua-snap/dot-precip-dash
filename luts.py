# pylint: disable=C0103
"""
Common shared text strings, formatting defaults and lookup tables.
"""

import os
import plotly.io as pio

# Core page components
title = "DOT Precipitation GUI"
url = "https://snap.uaf.edu"
preview = "http://snap.uaf.edu/assets/preview.png"
description = "Check precipitation frequency forecast data for any part of Alaska."
gtag_id = os.getenv("GTAG_ID", default="")
index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{gtag_id}');
        </script>
        {{%metas%}}
        <title>{{%title%}}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Schema.org markup for Google+ -->
        <meta itemprop="name" content="{title}">
        <meta itemprop="description" content="{description}">
        <meta itemprop="image" content="{preview}">

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <!-- Twitter summary card with large image must be at least 280x150px -->
        <meta name="twitter:image:src" content="{preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{url}" />
        <meta property="og:image" content="{preview}" />
        <meta property="og:description" content="{description}" />
        <meta property="og:site_name" content="{title}" />

        <link rel="alternate" hreflang="en" href="{url}" />
        <link rel="canonical" href="{url}"/>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

DURATIONS = [
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
]

INTERVALS = [2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0, 500.0, 1000.0]

# Plotly format template
plotly_template = pio.templates["simple_white"]
axis_configs = {
    "automargin": True,
    "showgrid": False,
    "showline": False,
    "ticks": "",
    "title": {"standoff": 0},
    "zeroline": False,
    "fixedrange": True,
}
xaxis_config = {**axis_configs, **{"tickformat": "%B %-d, %Y"}}
plotly_template.layout.xaxis = xaxis_config
plotly_template.layout.yaxis = axis_configs

# Used to make the chart exports nice
fig_download_configs = dict(
    filename="Statewide_Temperature_Index", width="1000", height="650", scale=2
)
fig_configs = dict(
    displayModeBar=True,
    showSendToCloud=False,
    toImageButtonOptions=fig_download_configs,
    modeBarButtonsToRemove=[
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "hoverClosestPie",
        "hoverClosest3d",
        "hoverClosestGl2d",
        "hoverClosestGeo",
        "toggleHover",
        "toggleSpikelines",
    ],
    displaylogo=False,
)

# Colors to reference
colors = ["#405bfe", "#ff3d00"]  # cold  # hot
