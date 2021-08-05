# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""
This module implements base class for low level api client.
"""
import urllib.request
from typing import Optional, Union

import requests

from here_location_services.exceptions import AuthenticationException, TooManyRequestsException


class Api:
    """Base class for low level api calls."""

    def __init__(self, access_token, proxies: Optional[dict] = None):
        self.access_token = access_token
        self._user_agent = "dhpy"
        self.proxies: Optional[dict] = proxies or urllib.request.getproxies()

    @property
    def headers(self) -> dict:
        """
        Return HTTP request headers with Bearer token in ``Authorization``
        field.

        :return: authorization tokens
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def post(
        self,
        url: str,
        data: Optional[Union[dict, list, bytes, str]] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        **kwargs,
    ) -> requests.Response:
        """
        Perform a post request of an API at a specified URL with backoff.

        :param url: URL of the API.
        :param data: Post data for http request.
        :param params: Parameters to pass to the API.
        :param headers: Request headers. Defaults to the api headers property.
        :param kwargs: Optional arguments that request takes.
        :return: response from the API.
        """
        headers = headers or self.headers
        headers["User-Agent"] = self._user_agent
        if isinstance(data, dict) or isinstance(data, list):
            return requests.post(
                url,
                headers=headers,
                json=data,
                params=params,
                proxies=self.proxies,
                **kwargs,
            )
        else:
            return requests.post(
                url,
                headers=headers,
                data=data,
                params=params,
                proxies=self.proxies,
                **kwargs,
            )

    @staticmethod
    def raise_response_exception(resp: requests.Response) -> None:
        """
        Parse HTTP errors status code and raise necessary exceptions.

        :param resp: An HTTP response to parse.
        :raises TooManyRequestsException: If platform responds with HTTP 429.
        :raises AuthenticationException: If platform responds with HTTP 401 or 403.
        :raises Exception: If client responds with any other exception.
        """
        if resp.status_code == 429:
            raise TooManyRequestsException(resp)
        elif resp.status_code in [401, 403]:
            raise AuthenticationException(resp)
        else:
            raise Exception(resp.text)
