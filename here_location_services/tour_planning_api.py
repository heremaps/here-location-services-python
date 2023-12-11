# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Tour Planning API <https://developer.here.com/documentation/tour-planning/2.3.0/api-reference-swagger.html>`_.
"""  # noqa E501

from typing import Any, Dict, Optional

import requests

from here_location_services.config.tour_planning_config import Fleet, Plan, Configuration, Objectives
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
        configuration: Configuration,
        fleet: Fleet,
        plan: Plan,
        objectives: Optional[dict[str]]=None,
        is_async: Optional[bool] = False,
    ):
        """Requests profile-aware routing data, creates a Vehicle Routing Problem and solves it.

        :param fleet: A fleet represented by various vehicle types for serving jobs.
        :param plan: Represents the list of jobs to be served.
        :param is_async: Solves the problem Asynchronously
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200 or 202.

        """
        path = ""
        if is_async:
            path = "v3/problems/async"
        else:
            path = "v3/problems"

        url = f"{self._base_url}/{path}"

        data: Dict[Any, Any] = {}


        data["configuration"] = vars(configuration)
        data["fleet"] = vars(fleet)
        data["plan"] = vars(plan)
        l_objectives = []
        if objectives:
            for o in objectives:
                l_objectives.append(o)
            data["objectives"] = l_objectives
            print(l_objectives)
        print(url)
        # print(data)


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
