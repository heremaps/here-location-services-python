# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""This module will test Location services APIs using auth token for authentication."""
import os
from datetime import datetime

import pytest
import pytz

from here_location_services import LS
from here_location_services.config.base_config import ROUTING_MODE
from here_location_services.config.matrix_routing_config import (
    AVOID_FEATURES,
    MATRIX_ATTRIBUTES,
    AvoidBoundingBox,
    WorldRegion,
)
from here_location_services.config.routing_config import ROUTING_TRANSPORT_MODE
from here_location_services.platform.credentials import PlatformCredentials
from here_location_services.responses import GeocoderResponse
from tests.conftest import env_setup_done

auth_present = env_setup_done()


@pytest.mark.skipif(not auth_present, reason="Credentials are not setup in env.")
def test_ls_geocoding_auth_token():
    """Test geocoding api."""
    api_key = os.environ.get("LS_API_KEY")
    try:
        del os.environ["LS_API_KEY"]
        address = "200 S Mathilda Sunnyvale CA"
        credentials = PlatformCredentials.from_default()
        ls = LS(platform_credentials=credentials)
        resp = ls.geocode(query=address, limit=2)
        assert isinstance(resp, GeocoderResponse)
        assert resp.__str__()
        assert resp.as_json_string()
        geo_json = resp.to_geojson()
        assert geo_json.type == "FeatureCollection"
        assert geo_json.features
        pos = resp.items[0]["position"]
        assert len(resp.items) == 1
        assert pos == {"lat": 37.37634, "lng": -122.03405}
    finally:
        os.environ["LS_API_KEY"] = api_key


@pytest.mark.skipif(not auth_present, reason="Credentials are not setup in env.")
def test_matrix_route_auth_token():
    """Test Matrix routing using auth token."""
    platform_credentials = PlatformCredentials.from_default()
    ls = LS(platform_credentials=platform_credentials)
    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
    ]
    region_definition = WorldRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances, MATRIX_ATTRIBUTES.travelTimes]
    avoid_areas = AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)
    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        destinations=origins,
        routing_mode=ROUTING_MODE.fast,
        departure_time=datetime.now(tz=pytz.utc),
        transport_mode=ROUTING_TRANSPORT_MODE.truck,
        avoid_features=[AVOID_FEATURES.tollRoad],
        avoid_areas=[avoid_areas],
        matrix_attributes=matrix_attributes,
    )
    mat = result.matrix
    assert mat["numOrigins"] == 3
    assert mat["numDestinations"] == 3
    assert len(mat["distances"]) == 9
