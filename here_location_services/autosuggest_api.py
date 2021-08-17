# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Autosuggest API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-autosuggest-brief.html>`_.
"""  # noqa E501

from typing import Dict, List, Optional

from here_location_services.config.autosuggest_config import SearchBox, SearchCircle
from here_location_services.platform.auth import Auth

from .apis import Api
from .exceptions import ApiError


class AutosuggestApi(Api):
    """A class for accessing HERE Autosuggest API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, auth=auth, proxies=proxies, country=country)
        self._base_url = f"https://autosuggest.search.{self._get_url_string()}"

    def get_autosuggest(
        self,
        q: str,
        at: Optional[List] = None,
        search_in_circle: Optional[SearchCircle] = None,
        search_in_box: Optional[SearchBox] = None,
        in_country: Optional[List] = None,
        limit: Optional[int] = None,
        terms_limit: Optional[int] = None,
        lang: Optional[List] = None,
        political_view: Optional[str] = None,
        show: Optional[str] = None,
    ):
        """Calculate route between two endpoints.

        See further information `here <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>_`.

        :param transport_mode: A string to represent mode of transport.

        """  # noqa E501
        path = "v1/autosuggest"
        url = f"{self._base_url}/{path}"
        params: Dict[str, str] = {
            "q": q,
        }
        if at:
            params["at"] = ",".join([str(i) for i in at])
        if in_country:
            params["in[countryCode]"] = ",".join([str(i) for i in in_country])
        if search_in_circle:
            params["in[circle]"] = search_in_circle.lat + "," + search_in_circle.lng
            params["in[r]"] = str(search_in_circle.radius)
        if limit:
            params["limit"] = str(limit)
        if terms_limit:
            params["termsLimit"] = str(terms_limit)
        if lang:
            params["lang"] = ",".join([str(i) for i in lang])
        if political_view:
            params["politicalView"] = political_view
        if show:
            params["show"] = show
        if search_in_box:
            params["in[bbox]"] = (
                search_in_box.west
                + ","
                + search_in_box.south
                + ","
                + search_in_box.east
                + ","
                + search_in_box.north
            )
        resp = self.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
