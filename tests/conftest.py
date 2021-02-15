# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import pytest

from here_location_services.apis import Api
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.fixture()
def api():
    """Create shared low level Location services Api instance as a pytest fixture."""
    api = Api(api_key=LS_API_KEY)
    return api
