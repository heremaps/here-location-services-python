# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import pytest

from here_location_services.geocoding_search_api import GeocodingSearchApi
from here_location_services.isoline_routing_api import IsolineRoutingApi
from here_location_services.routing_api import RoutingApi
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


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
