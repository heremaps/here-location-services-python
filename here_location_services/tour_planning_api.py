# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Tour Planning API <https://developer.here.com/documentation/tour-planning/2.3.0/api-reference-swagger.html>`_.
"""  # noqa E501

from typing import Any, Dict, Optional

import requests

from here_location_services.config.tour_planning_config import Fleet, Plan
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
    ):
        """Requests profile-aware routing data, creates a Vehicle Routing Problem and solves it.

        :param fleet: A fleet represented by various vehicle types for serving jobs.
        :param plan: Represents the list of jobs to be served.
        :param id: A unique identifier of an entity. Avoid referencing any confidential or
            personal information as part of the Id.
        :param optimization_traffic: "liveOrHistorical" "historicalOnly" "automatic"
            Specifies what kind of traffic information should be considered for routing
        :param optimization_waiting_time: Configures departure time optimization which tries to
            adapt the starting time of the tour in order to reduce waiting time as a consequence
            of a vehicle arriving at a stop before the starting time of the time window defined
            for serving the job.
        :param is_async: Solves the problem Asynchronously
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200 or 202.

        """
        path = ""
        if is_async:
            path = "v2/problems/async"
        else:
            path = "v2/problems"

        url = f"{self._base_url}/{path}"

        data: Dict[Any, Any] = {
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

        resp = self.post(url, data=data)
        if resp.status_code == 200 or resp.status_code == 202:
            return resp
        else:
            raise ApiError(resp)

    def get_async_tour_planning_status(self, status_url: str) -> requests.Response:
        """Get the status of async tour planning calculation for the provided status url."""
        return self.get(status_url, allow_redirects=False)

    def get_async_tour_planning_results(self, result_url: str):
        """Get the results of async tour planning for the provided result url."""
        resp = self.get(result_url)
        if resp.status_code != 200:
            raise ApiError(resp)
        return resp
