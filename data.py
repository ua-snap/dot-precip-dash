"""
Responsible for fetching, preprocessing
and caching community data.
"""
# pylint: disable=C0103, E0401

import urllib.parse
import os
import datetime
import logging
import numpy as np
import xarray as xr
import pandas as pd
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import scipy.stats
import pickle

DASH_LOG_LEVEL = os.getenv("DASH_LOG_LEVEL", default="info")
logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

API_URL = os.getenv("ACIS_API_URL", default="http://data.rcc-acis.org/MultiStnData?")
logging.info("Using ACIS API url %s", API_URL)


def fetch_api_data(x, y):
    """
    Reads data from ACIS API for selected community.
    """

    url = "http://localhost:5000/api/percentiles"
    values = {"xcoord": x, "ycoord": y}
    data = urllib.parse.urlencode(values)
    response = urllib.request.urlopen(url + "?" + data)
    pkl = response.read()
    data = pickle.loads(pkl)
    return data


def fetch_data(lat, lon):
    """
    Fetches preprocessed data from cache,
    or triggers an API request + preprocessing.
    """
    logging.info("Calling fetch_api_data()")

    return fetch_api_data(lat, lon)
