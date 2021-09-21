# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Tour Planning API <https://developer.here.com/documentation/tour-planning/2.3.0/api-reference-swagger.html>`_.
"""  # noqa E501

from typing import Dict, List, Optional, Tuple

from _pytest.mark import param

from here_location_services.config.tour_planning_config import Fleet, VehicleProfile, VehicleType
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

    def solve_problem(
        self,
        # fleet: Fleet,
        id: Optional[str] = None,
        is_async: Optional[bool] = False,
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
        path = ""
        if is_async:
            path = "v2/problems/async"
        else:
            path = "v2/problems"

        url = f"{self._base_url}/{path}"
        # params: Dict[str, str] = {
        #     "fleet": fleet,
        # }
        fleet = Fleet(
            # vehicle_types=[{
            #     "id": "09c77738-1dba-42f1-b00e-eb63da7147d6",
            #     "profile": "normal_car",
            #     "costs": {"fixed": 22, "distance": 0.0001, "time": 0.0048},
            #     "shifts": [
            #         {
            #             "start": {
            #                 "time": "2020-07-04T09:00:00Z",
            #                         "location": {"lat": 52.5256, "lng": 13.4542},
            #             },
            #             "end": {
            #                 "time": "2020-07-04T18:00:00Z",
            #                         "location": {"lat": 52.5256, "lng": 13.4542},
            #             },
            #             "breaks": [
            #                 {
            #                     "duration": 1800,
            #                     "times": [
            #                         ["2020-07-04T11:00:00Z", "2020-07-04T13:00:00Z"]
            #                     ],
            #                 }
            #             ],
            #         }
            #     ],
            #     "capacity": [100, 5],
            #     "skills": ["fridge"],
            #     "limits": {"maxDistance": 20000, "shiftTime": 21600},
            #     "amount": 1,
            # }], vehicle_profiles=[{"type": "car", "name": "normal_car"}],
            vehicle_types=[
                VehicleType(
                    id="09c77738-1dba-42f1-b00e-eb63da7147d6",
                    profile="normal_car",
                    costs_fixed=22,
                    costs_distance=0.0001,
                    costs_time=0.0048,
                    capacity=[100, 5],
                    skills=["fridge"],
                    amount=1,
                    shift_start={
                        "time": "2020-07-04T09:00:00Z",
                        "location": {"lat": 52.5256, "lng": 13.4542},
                    },
                    limits={
                        "maxDistance": 20000,
                        "shiftTime": 21600
                    },
                    shift_end={
                        "location": {
                            "lat": 52.5256,
                            "lng": 13.4542
                        },
                        "time": "2020-07-04T18:00:00Z"
                    },
                    shift_breaks=[{
                        "duration": 1800,
                        "times": [
                            [
                                "2020-07-04T11:00:00Z",
                                "2020-07-04T13:00:00Z"
                            ]
                        ]
                    }]
                )
            ],
            vehicle_profiles=[VehicleProfile(name="normal_car", vehicle_mode="car")],
        )

        data: Dict[str, str] = {
            "id": "7f3423c2-784a-4983-b472-e14107d5a54a",
            "configuration": {
                "optimizations": {
                    "traffic": "liveOrHistorical",
                    "waitingTime": {"reduce": True, "bufferTime": 15},
                }
            },

            "plan": {
                "jobs": [
                    {
                        "id": "4bbc206d-1583-4266-bac9-d1580f412ac0",
                        "places": {
                            "pickups": [
                                {
                                    "times": [["2020-07-04T10:00:00Z", "2020-07-04T12:00:00Z"]],
                                    "location": {"lat": 52.53088, "lng": 13.38471},
                                    "duration": 180,
                                    "demand": [10],
                                }
                            ],
                            "deliveries": [
                                {
                                    "times": [["2020-07-04T14:00:00Z", "2020-07-04T16:00:00Z"]],
                                    "location": {"lat": 52.54016, "lng": 13.40241},
                                    "duration": 300,
                                    "demand": [10],
                                }
                            ],
                        },
                        "skills": ["fridge"],
                        "priority": 2,
                    }
                ],
                "relations": [
                    {
                        "type": "sequence",
                        "jobs": ["departure", "4bbc206d-1583-4266-bac9-d1580f412ac0", "arrival"],
                        "vehicleId": "09c77738-1dba-42f1-b00e-eb63da7147d6_1",
                    }
                ],
            },
        }

        data["fleet"] = vars(fleet)

        print(data)
        # # if at:
        # #     params["at"] = ",".join([str(i) for i in at])
        # if in_country:
        #     params["in"] = "countryCode:" + ",".join([str(i) for i in in_country])
        # if search_in_circle:
        #     params["in"] = (
        #         "circle:"
        #         + str(search_in_circle.lat)
        #         + ","
        #         + str(search_in_circle.lng)
        #         + ";r="
        #         + str(search_in_circle.radius)
        #     )
        # if limit:
        #     params["limit"] = str(limit)
        # if terms_limit:
        #     params["termsLimit"] = str(terms_limit)
        # if lang:
        #     params["lang"] = ",".join([str(i) for i in lang])
        # if political_view:
        #     params["politicalView"] = political_view
        # if show:
        #     params["show"] = ",".join([str(i) for i in show])
        # if search_in_bbox:
        #     params["in"] = "bbox:" + ",".join([str(i) for i in search_in_bbox])
        resp = self.post(url, data=data)
        print(resp.url)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
