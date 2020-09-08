"""
Responsible for fetching, preprocessing
and caching community data.
"""
# pylint: disable=C0103, E0401

import urllib.parse
import os
import logging
import pickle

DASH_LOG_LEVEL = os.getenv("DASH_LOG_LEVEL", default="info")
logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

API_URL = os.getenv(
    "API_URL", default="http://apollo.snap.uaf.edu:3000/api/percentiles"
)
logging.info("Using API url %s", API_URL)


def fetch_api_data(x, y):
    """
    Creates an API request for precipitation frequency data given an
      X & Y coordinate in the EPSG:3338 grid.
    Inputs:
        * x - The X-coordinate in the EPSG:3338 coordinate system.
        * y - The Y-coordinate in the EPSG:3338 coordinate system.
    Returns:
        * A 5-D XArray DataArray containing PF data for the given
          X & Y coordinate which has dimensions (gcm, duration, timerange,
          variable, and interval).
          - gcm = Global Climate Model Name
              (GFDL-CM3 or NCAR-CCSM4)
          - duration = A duration of time for which the precipitation variables represent:
              (60m, 2h, 3h, 6h, 12h, 24h, 3d, 4d, 7d, 10d, 20d, 30d, 45d, 60d)
          - timerange = Time range of given prediction
              (2020-2049, 2050-2079, 2080-2099)
          - variable = Name of variable desired:
              (pf - median value,
              pf-upper - upper confidence interval,
              pf-lower - lower confidence interval)
          - interval = Return interval in years for which the precipitation variables represent:
              (2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0, 500.0, 1000.0)
    """

    logging.info("Calling fetch_api_data()")

    values = {"xcoord": x, "ycoord": y}
    data = urllib.parse.urlencode(values)
    response = urllib.request.urlopen(API_URL + "?" + data)
    pkl = response.read()
    data = pickle.loads(pkl)
    return data
