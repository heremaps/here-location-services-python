# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""This module will test platform api module."""
import pytest
from requests_oauthlib import OAuth1

from here_location_services.platform.apis.aaa_oauth2_api import AAAOauth2Api
from here_location_services.platform.apis.api import Api as PlaformApi
from here_location_services.utils import get_apikey
from tests.conftest import get_mock_response

LS_API_KEY = get_apikey()


def test_api_headers_property():
    api = PlaformApi(access_token="dummy")
    assert api.headers == {"Authorization": "Bearer dummy"}


def test_mock_request_post(mocker):
    mocker.patch("requests.post", return_value=True)
    api = PlaformApi(access_token="dummy")
    resp = api.post("dummy_url", data={"foo": "bar"})
    assert resp is True


def test_mock_request_scoped_access_token_excception(mocker):
    reason = "This is mock reason"
    text = "This is mock text"
    mock_response = get_mock_response(500, reason, text)
    mocker.patch("here_location_services.platform.apis.api.Api.post", return_value=mock_response)
    aaa_api = AAAOauth2Api(base_url="dummy")
    oauth = OAuth1(
        "dummy_key",
        client_secret="dummy_secret",
        signature_method="HMAC-SHA256",
    )
    with pytest.raises(Exception):
        aaa_api.request_scoped_access_token(oauth=oauth, data="dummy_data")
