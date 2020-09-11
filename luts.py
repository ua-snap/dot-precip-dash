# pylint: disable=C0103,E0401
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

# Jinja template
table_template = """
<table class="table">
    <caption>Modeled cumulative rainfall for model {{ gcm }} for time range {{ ts_str }} in {{ units }}</caption>
    <thead>
        <tr class="noborder">
            <th scope="col">Duration</th>
            <th scope="col" colspan="9">Return Interval<th>
        </tr>
        <tr>
            <th><!-- spacer --></th>
            {% for interval in intervals %}
                <th scope="col">{{ interval }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
    {% for duration, row in rows.items() %}
        <tr>
            <th scope="row">{{ duration }}</th>
            {% for values in row %}
                <td>
                    <p><strong>{{ values.value }}</strong></p>
                    <span><em>({{ values.lo }}&ndash;{{ values.hi }})</em></span>
                </td>
            {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
"""

# Plotly format template
plotly_template = pio.templates["simple_white"]
