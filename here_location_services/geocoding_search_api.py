# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Geocoding & Search API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/index.html>`_.
"""  # noqa: E501

from typing import Dict, List, Optional

import requests

from .apis import Api
from .exceptions import ApiError


class GeocodingSearchApi(Api):
    """A class for accessing HERE Geocoding & search APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, proxies, country)
        self._base_url = "https://{0}.search.{1}"

    def get_geocoding(self, query: str, limit: int = 20, lang: str = "en-US") -> requests.Response:
        """
        Get point for given free-form search query.

        See further information here:
        |geocoder|

        .. |geocoder| raw:: html

           <a href="https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-geocode-brief.html" target="_blank">Geocode</a>

        :param query: a string containing the query to make.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 20.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """  # noqa E501
        path = "/v1/geocode"
        url = self._base_url.format("geocode", self._get_url_string()) + path
        params: dict = dict(q=query, limit=limit, lang=lang)
        if self.credential_params:
            params.update(self.credential_params)
        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)

    def get_reverse_geocoding(
        self, lat: float, lng: float, limit: int = 1, lang: str = "en-US"
    ) -> requests.Response:
        """Get address for given latitude and longitude.

        See further information here:
        |reverse_geocode|

        .. |reverse_geocode| raw:: html

           <a href="https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-reverse-geocode-brief.html" target="_blank">Reverse Geocode</a>

        :param lat: A float representing latitude of point.
        :param lng: A float representing longitude of point.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 1.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """  # noqa E501
        path = "/v1/revgeocode"
        url = self._base_url.format("geocode", self._get_url_string()) + path
        params: dict = dict(at=f"{lat},{lng}", limit=limit, lang=lang)
        if self.credential_params:
            params.update(self.credential_params)
        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)

    def get_search_discover(
        self,
        query: str,
        center: Optional[List[float]] = None,
        radius: Optional[int] = None,
        country_codes: Optional[List] = None,
        bounding_box: Optional[List[float]] = None,
        limit: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> requests.Response:
        """Search places using Location Services discover endpoint.

        This method uses location services ``discover`` endpoint to search places based on
        query which is free-form text.

        :param query: A string representing free-test query to search places.
        :param center: A list of latitude and longitude representing the center for
            search query.
        :param radius: A radius in meters along with center for searching places.
        :param country_codes: A list of  ISO 3166-1 alpha-3 country codes.
        :param bounding_box: A bounding box, provided as west longitude, south latitude,
            east longitude, north latitude.
        :param limit: An int representing maximum number of results to be returned.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        path = "/v1/discover"
        url = self._base_url.format("discover", self._get_url_string()) + path
        params: Dict[str, str] = {"q": query}
        if center is not None and radius is not None:
            circle = "circle:" + ",".join([str(x) for x in center])
            params["in"] = circle + f";r={radius}"
        elif center is not None and country_codes:
            params["at"] = ",".join([str(x) for x in center])
            params["in"] = "countryCode:" + ",".join([str(x) for x in country_codes])
        elif bounding_box:
            params["in"] = "bbox:" + ",".join([str(x) for x in bounding_box])
        if lang:
            params["lang"] = lang
        if limit:
            params["limit"] = str(limit)

        if self.credential_params:
            params.update(self.credential_params)

        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)

    def get_search_browse(
        self,
        center: List,
        radius: Optional[int] = None,
        country_codes: Optional[List] = None,
        bounding_box: Optional[List[float]] = None,
        categories: Optional[List] = None,
        limit: Optional[int] = None,
        name: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> requests.Response:
        """Get search results for places based on different filters such as categories or name.

        :param center: A list of latitude and longitude representing the center for
            search query.
        :param radius: A radius in meters along with center for searching places.
        :param country_codes: A list of  ISO 3166-1 alpha-3 country codes.
        :param bounding_box: A bounding box, provided as west longitude, south latitude,
            east longitude, north latitude.
        :param categories: A List of strings of category-ids.
        :param limit: An int representing maximum number of results to be returned.
        :param name: A string representing Full-text filter on POI names/titles.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        path = "/v1/browse"
        url = self._base_url.format("browse", self._get_url_string()) + path
        params: Dict[str, str] = {"at": ",".join([str(x) for x in center])}

        if radius is not None:
            params["area"] = "circle:" + ",".join([str(x) for x in center]) + f";r={radius}"
        elif country_codes:
            params["area"] = "countryCode:" + ",".join([str(c) for c in country_codes])
        elif bounding_box:
            params["area"] = "bbox:" + ",".join([str(b) for b in bounding_box])
        if categories:
            params["categories"] = ",".join(categories)
        if name:
            params["name"] = name
        if limit:
            params["limit"] = str(limit)
        if lang:
            params["lang"] = lang

        if self.credential_params:
            params.update(self.credential_params)

        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)

    def get_search_lookup(self, location_id: str, lang: Optional[str] = None) -> requests.Response:
        """
        Get search results by providing ``location_id``.

        :param location_id: A string representing id.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        path = "/v1/lookup"
        url = self._base_url.format("lookup", self._get_url_string()) + path
        params: Dict[str, str] = {"id": location_id}
        if lang:
            params["lang"] = lang

        if self.credential_params:
            params.update(self.credential_params)

        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
