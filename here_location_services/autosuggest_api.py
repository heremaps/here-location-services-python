# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Autosuggest API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-autosuggest-brief.html>`_.
"""  # noqa E501

from typing import Dict, List, Optional, Tuple

from here_location_services.config.autosuggest_config import SearchCircle
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
        query: str,
        at: Optional[List] = None,
        search_in_circle: Optional[SearchCircle] = None,
        search_in_bbox: Optional[Tuple] = None,
        in_country: Optional[List[str]] = None,
        limit: Optional[int] = 20,
        terms_limit: Optional[int] = None,
        lang: Optional[List[str]] = None,
        political_view: Optional[str] = None,
        show: Optional[List[str]] = None,
    ):
        """Suggest address or place candidates based on an incomplete or misspelled query

        :param query: A string for free-text query. Example: res, rest
        :param at: Specify the center of the search context expressed as list of coordinates
            One of `at`, `search_in_circle` or `search_in_bbox` is required.
            Parameters "at", "search_in_circle" and "search_in_bbox" are mutually exclusive. Only
            one of them is allowed.
        :param search_in_circle: Search within a circular geographic area provided as
            latitude, longitude, and radius (in meters)
        :param search_in_bbox: Search within a rectangular bounding box geographic area provided
            as tuple of west longitude, south latitude, east longitude, north latitude
        :param in_country: Search within a specific or multiple countries provided as
            comma-separated ISO 3166-1 alpha-3 country codes. The country codes are to be
            provided in all uppercase. Must be accompanied by exactly one of
            `at`, `search_in_circle` or `search_in_bbox`.
        :param limit: An integer specifiying maximum number of results to be returned.
        :param terms_limit: An integer specifiying maximum number of Query Terms Suggestions
            to be returned.
        :param lang: List of strings to select the language to be used for result rendering
            from a list of BCP 47 compliant language codes.
        :param political_view: Toggle the political view.
        :param show: Select additional fields to be rendered in the response. Please note
            that some of the fields involve additional webservice calls and can increase
            the overall response time.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.

        """
        path = "v1/autosuggest"
        url = f"{self._base_url}/{path}"
        params: Dict[str, str] = {
            "q": query,
        }
        if at:
            params["at"] = ",".join([str(i) for i in at])
        if in_country:
            params["in"] = "countryCode:" + ",".join([str(i) for i in in_country])
        if search_in_circle:
            params["in"] = (
                "circle:"
                + str(search_in_circle.lat)
                + ","
                + str(search_in_circle.lng)
                + ";r="
                + str(search_in_circle.radius)
            )
        if limit:
            params["limit"] = str(limit)
        if terms_limit:
            params["termsLimit"] = str(terms_limit)
        if lang:
            params["lang"] = ",".join([str(i) for i in lang])
        if political_view:
            params["politicalView"] = political_view
        if show:
            params["show"] = ",".join([str(i) for i in show])
        if search_in_bbox:
            params["in"] = "bbox:" + ",".join([str(i) for i in search_in_bbox])
        resp = self.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
