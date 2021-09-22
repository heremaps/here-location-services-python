# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Tour Planning API <https://developer.here.com/documentation/tour-planning/2.3.0/api-reference-swagger.html>`_.
"""  # noqa E501

from typing import Dict, List, Optional, Tuple

from _pytest.mark import param
import requests

from here_location_services.config.tour_planning_config import (
    Fleet,
    Job,
    JobPlaces,
    Plan,
    Relation,
    VehicleProfile,
    VehicleType,
)
from here_location_services.platform.auth import Auth

from .apis import Api
from .exceptions import ApiError


class TourPlanningApi(Api):
    """A class for accessing HERE Tour Planning API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, auth=auth, proxies=proxies, country=country)
        self._base_url = f"https://tourplanning.{self._get_url_string()}"

    def solve_tour_planning(
        self,
        fleet: Fleet,
        plan: Plan,
        id: Optional[str] = None,
        optimization_traffic: Optional[str] = None,
        optimization_waiting_time: Optional[Dict] = None,
        is_async: Optional[bool] = False,
    ) -> Dict:
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
        path = ""
        if is_async:
            path = "v2/problems/async"
        else:
            path = "v2/problems"

        url = f"{self._base_url}/{path}"

        data: Dict[str, str] = {
            "configuration": {"optimizations": {}},
        }

        if id:
            data["id"] = id

        if optimization_traffic:
            data["configuration"]["optimizations"]["traffic"] = optimization_traffic

        if optimization_traffic:
            data["configuration"]["optimizations"]["waitingTime"] = optimization_waiting_time

        data["fleet"] = vars(fleet)
        data["plan"] = vars(plan)

        print(data)

        resp = self.post(url, data=data)
        print(resp.url)
        if resp.status_code == 200 or resp.status_code == 202:
            return resp
        else:
            raise ApiError(resp)

    def get_async_tour_planning_status(self, status_url: str) -> requests.Response:
        """Get the status of async tour planning calculation for the provided status url."""
        return self.get(status_url, allow_redirects=False)

    def get_async_tour_planning_results(self, result_url: str) -> requests.Response:
        """Get the results of async tour planning for the provided result url."""
        resp = self.get(result_url)
        if resp.status_code != 200:
            raise ApiError(resp)
        return resp.json()
