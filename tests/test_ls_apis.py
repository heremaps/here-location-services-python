# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

from argparse import Namespace
from datetime import datetime

import pytest
import requests
from geojson import Point

from here_location_services.config.dest_weather_config import DEST_WEATHER_PRODUCT
from here_location_services.config.isoline_routing_config import (
    ISOLINE_ROUTING_TRANSPORT_MODE,
    RANGE_TYPE,
)
from here_location_services.config.matrix_routing_config import WorldRegion
from here_location_services.exceptions import ApiError
from here_location_services.matrix_routing_api import MatrixRoutingApi
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_destination_weather(destination_weather_api):
    """Test Destination Weather api."""
    resp = destination_weather_api.get_dest_weather(
        products=[DEST_WEATHER_PRODUCT.observation], query="Chicago"
    )
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_weather_alerts(destination_weather_api):
    """Test Destination Weather api."""
    resp = destination_weather_api.get_weather_alerts(
        geometry=Point(coordinates=[15.256, 23.456]),
        start_time=datetime.now(),
    )
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_autosuggest(autosuggest_api):
    """Test autosuggest api."""
    resp = autosuggest_api.get_autosuggest(query="res", limit=5, at=["52.93175,12.77165"])
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_geocoding(geo_search_api):
    """Test geocoding api."""
    address = "Goregaon West, Mumbai 400062, India"
    resp = geo_search_api.get_geocoding(query=address)
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_reverse_geocoding(geo_search_api):
    """Test reverse geocoding."""
    resp = geo_search_api.get_reverse_geocoding(lat=19.1646, lng=72.8493)
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_isonline_routing(isoline_routing_api):
    """Test isonline routing api."""
    result = isoline_routing_api.get_isoline_routing(
        origin=[52.5, 13.4],
        range="3000",
        range_type=RANGE_TYPE.distance,
        transport_mode=ISOLINE_ROUTING_TRANSPORT_MODE.car,
    )

    coordinates = result.json()["isolines"][0]["polygons"][0]["outer"]
    assert coordinates[0]


def test_mock_api_error(mocker):
    """Mock Test for geocoding api."""
    mock_response = Namespace(status_code=300)
    mocker.patch(
        "here_location_services.matrix_routing_api.requests.post",
        return_value=mock_response,
    )
    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
    ]
    region_definition = WorldRegion()
    mat = MatrixRoutingApi(api_key="dummy")
    with pytest.raises(ApiError):
        _ = mat.matrix_route(
            origins=origins,
            region_definition=region_definition,
        )
