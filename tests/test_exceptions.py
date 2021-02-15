# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""Module for testing API exceptions."""


import pytest

from here_location_services import LS
from here_location_services.exceptions import ApiError


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
