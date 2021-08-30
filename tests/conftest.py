# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import os
from collections import namedtuple

import pytest

from here_location_services.autosuggest_api import AutosuggestApi
from here_location_services.destination_weather_api import DestinationWeatherApi
from here_location_services.exceptions import ConfigException
from here_location_services.geocoding_search_api import GeocodingSearchApi
from here_location_services.isoline_routing_api import IsolineRoutingApi
from here_location_services.platform.credentials import PlatformCredentials
from here_location_services.routing_api import RoutingApi
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()
HERE_USER_ID = os.environ.get("HERE_USER_ID")
HERE_CLIENT_ID = os.environ.get("HERE_CLIENT_ID")
HERE_ACCESS_KEY_ID = os.environ.get("HERE_ACCESS_KEY_ID")
HERE_ACCESS_KEY_SECRET = os.environ.get("HERE_ACCESS_KEY_SECRET")


@pytest.fixture()
def geo_search_api():
    """Create shared low level Location services GeocodingSearchApi instance as a pytest fixture.
    :return: :class:`GeocodingSearchApi` object.
    """
    api = GeocodingSearchApi(api_key=LS_API_KEY)
    return api


@pytest.fixture()
def isoline_routing_api():
    """Create shared low level Location services IsolineRoutingApi instance as a pytest fixture."""
    api = IsolineRoutingApi(api_key=LS_API_KEY)
    return api


@pytest.fixture()
def routing_api():
    """Create shared low level Location services IsolineRoutingApi instance as a pytest fixture."""
    api = RoutingApi(api_key=LS_API_KEY)
    return api


@pytest.fixture()
def autosuggest_api():
    """Create shared low level Location services AutosuggestApi instance as a pytest fixture."""
    api = AutosuggestApi(api_key=LS_API_KEY)
    return api


@pytest.fixture()
def destination_weather_api():
    """Create shared low level Location services Dest Weather instance as a pytest fixture."""
    api = DestinationWeatherApi(api_key=LS_API_KEY)
    return api


def env_setup_done():
    """This function will return env variables required to authenticate APIs using auth token."""
    try:
        _ = PlatformCredentials.from_default()
    except (ConfigException, AssertionError):
        return False
    else:
        return True


def get_mock_response(status_code: int, reason: str, text: str):
    """
    Return mock response.

    :param status_code: An int representing status_code.
    :param reason: A string to represent reason.
    :param text: A string to represent text.
    :return: MockResponse object.
    """
    MockResponse = namedtuple("MockResponse", ["status_code", "reason", "text"])
    mock_response = MockResponse(status_code, reason, text)
    return mock_response
