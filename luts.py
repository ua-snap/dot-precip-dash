# pylint: disable=C0103,E0401
"""
Common shared text strings, formatting defaults and lookup tables.
"""

import os
import plotly.io as pio

# Core page components
title = "Future Projections of Precipitation for Alaska Infrastructure"
url = "https://snap.uaf.edu"
preview = "http://snap.uaf.edu/assets/preview.png"
description = "Check precipitation frequency forecast data for any part of Alaska."

index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <script async defer 
            data-website-id="da73d5d1-4fd1-4fdf-b7ed-20a39fc7a523"
            data-do-not-track="true"
            data-domains="snap.uaf.edu"
            src="https://umami.snap.uaf.edu/umami.js">
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
    "2d",
    "3d",
    "4d",
    "7d",
    "10d",
    "20d",
    "30d",
    "45d",
    "60d",
]

INTERVALS = [2, 5, 10, 25, 50, 100, 200, 500, 1000]

# Jinja template
table_template = """
<table class="table">
    <caption class="title is-5">Modeled cumulative rainfall at {{ lat }}&deg;N, {{ lon }}&deg;E, {{ gcm }}, {{ ts_str }} ({{ units }})</caption>
    <thead>
        <tr class="noborder">
            <th scope="col">Duration</th>
            <th scope="col" colspan="9">Annual exceedance probability (1/years)</th>
        </tr>
        <tr>
            <th><!-- spacer --></th>
            {% for interval in intervals %}
                <th scope="col">1/{{ interval }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
    {% for duration, row in rows.items() %}
        <tr>
            <th scope="row">{{ duration }}</th>
            {% for values in row %}
                <td>
                    <strong>{{ values.value }}</strong>
                    <br>
                    <span>{{ values.lo }}&ndash;{{ values.hi }}</span>
                </td>
            {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
"""

# Plotly format template
plotly_template = pio.templates["simple_white"]
