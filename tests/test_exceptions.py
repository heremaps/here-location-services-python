# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""Module for testing API exceptions."""


import pytest

from here_location_services import LS
from here_location_services.exceptions import (
    ApiError,
    AuthenticationException,
    TooManyRequestsException,
)
from here_location_services.platform.apis.api import Api
from tests.conftest import get_mock_response


def test_exception_requests_inalid():
    """Raise exception via requests as response for invalid api_key."""
    ls = LS(api_key="dummy")
    with pytest.raises(ApiError) as execinfo:
        resp = ls.geocode(query="abc")
        raise ApiError(resp)
    resp = execinfo.value.args[0]
    assert resp.status_code == 401
    assert resp.reason == "Unauthorized"
    assert str(execinfo.value).startswith('401, Unauthorized, {"error":"Unauthorized"')


def test_raise_response_exception():
    reason = "This is mock reason"
    text = "This is mock text"
    mock_response = get_mock_response(513, reason, text)

    mock_response = get_mock_response(401, reason, text)
    with pytest.raises(AuthenticationException):
        Api.raise_response_exception(mock_response)

    mock_response = get_mock_response(429, reason, text)
    with pytest.raises(TooManyRequestsException):
        Api.raise_response_exception(mock_response)
