# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""This module will test Location services APIs using auth token for authentication."""
import os

import pytest

from here_location_services import LS
from here_location_services.platform.credentials import PlatformCredentials
from here_location_services.responses import GeocoderResponse
from tests.conftest import env_setup_done

auth_present = env_setup_done()


@pytest.mark.skipif(not auth_present, reason="Credentials are not setup in env.")
def test_ls_geocoding_auth_token():
    """Test geocoding api."""
    try:
        api_key = os.environ.get("LS_API_KEY")
        del os.environ["LS_API_KEY"]
        address = "200 S Mathilda Sunnyvale CA"
        credentials = PlatformCredentials.from_default()
        ls = LS(platfrom_credentials=credentials)
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
