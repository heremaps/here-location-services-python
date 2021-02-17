# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains base classes for accessing the Location Services RESTful APIs.
"""

import urllib
import urllib.request
from typing import Optional

from here_location_services.config.url_config import conf


class Api:
    """A base class for low-level HTTP RESTful API client for location services."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        self.credentials = dict(api_key=api_key)
        self.proxies = proxies or urllib.request.getproxies()
        self.country = country

    @property
    def credential_params(self) -> dict:
        """
        Return dict. with credentials info to be used as query parameters.
        """
        if self.credentials["api_key"]:
            return dict(apiKey=self.credentials["api_key"])
        else:
            raise Exception(
                f"api_key: {self.credentials['api_key']} is not present in credentials."
            )

    def _get_url_string(self) -> str:
        """
        Get url string from config based on type of country.

        For china url string ends with ``hereapi.cn`` and for rest of the countries
        deonoted by ``row`` it is ``hereapi.com``.

        :raises Exception: If ``api_key`` not found in credentials.
        """
        if self.credentials["api_key"]:
            url = conf[self.country]["here_api"]
            return url
        else:
            raise Exception(
                f"api_key: {self.credentials['api_key']} is not present in credentials."
            )
