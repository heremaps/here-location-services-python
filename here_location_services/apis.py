# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains classes for accessing the Location Services RESTful APIs.
"""

import urllib
from typing import Dict, List, Optional

import requests

from .config import conf
from .exceptions import ApiError


class Api:
    """A low-level HTTP RESTful API client for location services."""

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

    def get_geocoding(self, query: str, limit: int = 20, lang: str = "en-US") -> requests.Response:
        """
        Get point for given free-form search query.

        See further information here:
        |geocoder|

        .. |geocoder| raw:: html

           <a href="https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-geocode-brief.html" target="_blank">Geocode</a>  # noqa E501

        :param query: a string containing the query to make.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 20.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        base_url = f"https://geocode.search.{self._get_url_string()}"
        path = "/v1/geocode"
        url = f"{base_url}/{path}"
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

           <a href="https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-reverse-geocode-brief.html" target="_blank">Reverse Geocode</a>  # noqa E501

        :param lat: A float representing latitude of point.
        :param lng: A float representing longitude of point.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 1.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        base_url = f"https://revgeocode.search.{self._get_url_string()}"
        path = "/v1/revgeocode"
        url = f"{base_url}/{path}"
        params: dict = dict(at=f"{lat},{lng}", limit=limit, lang=lang)
        if self.credential_params:
            params.update(self.credential_params)
        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)

    def get_isoline_routing(
        self,
        mode: str,
        range: str,
        range_type: str,
        start: Optional[List[float]] = None,
        destination: Optional[List[float]] = None,
        arrival: Optional[str] = None,
        departure: Optional[str] = None,
    ) -> requests.Response:
        """Get isoline routing.

        Request a polyline that connects the endpoints of all routes
        leaving from one defined center with either a specified length
        or specified travel time.

        :param mode: A string representing how the route is calculated.
            Example: ``Type;TransportModes;TrafficMode;Feature``.
            ``fastest;car;traffic:disabled;motorway:-3``
        :param range: A string representing a range of isoline, unit is defined by
            parameter range type. Example: range='1000' or range='1000,2000,3000'
        :param range_type: A string representing a type of ``range``. Possible values are
            ``distance``, ``time`` and ``consumption``. For distance the unit meters. For a
            time the unit is seconds.For consumption, it is defined by the consumption
            model.
        :param start: A list of latitude and longitude representing the center of isoline
            request. Isoline will cover all the roads which can be reached from this
            point within a given range. It can not be used in combination with the
            ``destination`` parameter.
        :param destination: A list of latitude and longitude representing the center of
            isoline request. Isoline will cover all roads from which this point can be
            reached within a given range. It can not be used in combination with the
            ``start`` parameter.
        :param arrival: A string representing the time when travel is expected to end.
            It can be used only if the parameter ``destination`` is also used.
            Example: arrival= '2013-07-04T17:00:00+02'.
        :param departure: A string representing the time when travel is expected to
            start. It can be used only if the parameter ``start`` is also used.
            Example: departure= '2013-07-04T17:00:00+02'
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        base_url = f"https://isoline.route.ls.{self._get_url_string()}"
        path = "routing/7.2/calculateisoline.json"
        url = f"{base_url}/{path}"
        params: Dict[str, str] = {
            "range": range,
            "rangetype": range_type,
            "mode": mode,
        }
        if start:
            params["start"] = f"geo!{start[0]},{start[1]}"
        if destination:
            params["destination"] = f"geo!{destination[0]},{destination[1]}"
        if arrival:
            params["arrival"] = arrival
        if departure:
            params["departure"] = departure
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
        url = f"https://discover.search.{self._get_url_string()}/v1/discover"
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
        url = f"https://browse.search.{self._get_url_string()}/v1/browse"
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
        url = f"https://lookup.search.{self._get_url_string()}/v1/lookup"
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
