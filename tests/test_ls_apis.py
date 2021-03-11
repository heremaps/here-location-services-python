# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import pytest
import requests

from here_location_services.apis import Api
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_geocoding(geo_search_api):
    """Test geocoding api."""
    address = "Goregaon West, Mumbai 400062, India"
    resp = geo_search_api.get_geocoding(query=address)
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_geocoding_exception():
    """Test geocoding api. """
    address = "Goregaon West, Mumbai 400062, India"
    api = Api()
    with pytest.raises(Exception):
        api.get_geocoding(query=address)


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
        start=[52.5, 13.4], range="900", range_type="time", mode="fastest;car;"
    )

    coordinates = result.json()["response"]["isoline"][0]["component"][0]["shape"]
    assert coordinates[0]


def test_credentials_exception():
    """Test exception for credentials."""
    api = Api()
    with pytest.raises(Exception):
        _ = api.credential_params
