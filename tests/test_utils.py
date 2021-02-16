# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import os

from here_location_services.utils import get_apikey


def test_get_apikey():
    """Test ``get_apikey`` returns empty string when
    environment variable ``LS_API_KEY`` is not set.
    """
    api_key = os.environ.get("LS_API_KEY")
    del os.environ["LS_API_KEY"]
    key = get_apikey()
    assert key == ""
    os.environ["LS_API_KEY"] = api_key
