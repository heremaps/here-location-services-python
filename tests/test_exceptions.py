# Copyright (C) 2019-2020 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

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
