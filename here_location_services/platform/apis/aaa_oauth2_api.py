# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""
This module contains an :class:`AAAOauth2ApiClient` class to perform oauth API operations.

The HERE API reference documentation used in this module can be found here:
|iam_api_reference|

.. |iam_api_reference| raw:: html

   <a href="https://developer.here.com/documentation/identity-access-management/api-reference-swagger.html">IAM API Reference</a>
"""  # noqa

from typing import Dict, Optional

from requests_oauthlib import OAuth1

from here_location_services.platform.apis.api import Api


class AAAOauth2Api(Api):
    """
    This class provides access to HERE platform AAA Oauth2 APIs.
    """

    def __init__(
        self,
        base_url: str,
        proxies: Optional[dict] = None,
    ):
        self.base_url = base_url
        self.proxies: Optional[Dict] = proxies
        super().__init__(
            access_token=None,
            proxies=self.proxies,
        )

    def request_scoped_access_token(self, oauth: OAuth1, data: str) -> Dict:  # type: ignore[return]  # noqa E501
        """
        Request scoped access oauth2 token from platform.

        :param oauth: oauth1 configuration.
        :param data: a string which represents request body.
        :return: a json with scoped access token.
        """
        resp = self.post(
            url=self.base_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
            auth=oauth,
        )
        if resp.status_code == 200:
            resp_dict: dict = resp.json()
            return resp_dict
        else:
            self.raise_response_exception(resp)
