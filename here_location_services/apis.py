# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains base classes for accessing the Location Services RESTful APIs.
"""

import urllib
import urllib.request
from typing import Dict, Optional

import requests

from here_location_services.config.url_config import conf
from here_location_services.platform.auth import Auth


class Api:
    """A base class for low-level HTTP RESTful API client for location services."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        self.auth = auth
        self.credentials = dict(
            api_key=api_key, access_token=self.auth.token if self.auth else None
        )
        self.proxies = proxies or urllib.request.getproxies()
        self.headers: Dict[str, str] = {}
        self.country = country

    def _get_url_string(self) -> str:
        """
        Get url string from config based on type of country.

        For china url string ends with ``hereapi.cn`` and for rest of the countries
        deonoted by ``row`` it is ``hereapi.com``.

        :raises Exception: If ``api_key`` not found in credentials.
        """
        if self.credentials["api_key"] or self.credentials["access_token"]:
            url = conf[self.country]["here_api"]
            return url
        else:
            raise Exception(
                f"api_key: {self.credentials['api_key']} is not present in credentials."
            )

    def __add_api_key_in_params(self, params: Dict) -> Dict:
        """
        Add api_key in query params dictionary.

        :return: Dict.
        """
        params.update({"apiKey": self.credentials["api_key"]})
        return params

    def get(self, url: str, params: Optional[Dict] = None, **kwargs):
        """Send HTTP GET request.

        :param url: A string to represent URL.
        :param params: An optional dict for query params.
        :param kwargs: An optional extra arguments.
        :return: :class:`requests.Response` object.
        """
        q_params = params if params is not None else {}
        if self.credentials["api_key"]:
            q_params = self.__add_api_key_in_params(q_params)
        elif self.credentials["access_token"]:
            auth_token = {"Authorization": f"Bearer {self.credentials['access_token']}"}
            self.headers.update(auth_token)
        resp = requests.get(url, params=q_params, headers=self.headers, **kwargs)
        return resp

    def post(self, url: str, data: Dict, params: Optional[Dict] = None):
        """
        Send HTTP POST request.

        :param url: A string to represent URL.
        :param data: A dictionary to represent the post data
        :param params: An optional dict for query params.
        :return: :class:`requests.Response` object.
        """
        self.headers.update({"Content-Type": "application/json"})
        q_params = params if params is not None else {}
        if self.credentials["api_key"]:
            q_params = self.__add_api_key_in_params(q_params)
        elif self.credentials["access_token"]:
            auth_token = {"Authorization": f"Bearer {self.credentials['access_token']}"}
            self.headers.update(auth_token)
        resp = requests.post(
            url, params=q_params, json=data, proxies=self.proxies, headers=self.headers
        )
        return resp
