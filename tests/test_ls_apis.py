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

import pytest
import requests

from here_location_services.apis import Api
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_geocoding(api):
    """Test geocoding api."""
    address = "Goregaon West, Mumbai 400062, India"
    resp = api.get_geocoding(query=address)
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
def test_reverse_geocoding(api):
    """Test reverse geocoding."""
    resp = api.get_reverse_geocoding(lat=19.1646, lng=72.8493)
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_isonline_routing(api):
    """Test isonline routing api."""
    result = api.get_isoline_routing(
        start=[52.5, 13.4], range="900", range_type="time", mode="fastest;car;"
    )

    coordinates = result.json()["response"]["isoline"][0]["component"][0]["shape"]
    assert coordinates[0]
