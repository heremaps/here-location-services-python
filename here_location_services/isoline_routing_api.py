# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Routing API <https://developer.here.com/documentation/routing/dev_guide/topics/request-isoline.html>`_.
"""  # noqa E501

from typing import Dict, List, Optional

import requests

from .apis import Api
from .exceptions import ApiError


class IsolineRoutingApi(Api):
    """A class for accessing HERE isoline routing API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, proxies, country)
        self._base_url = f"https://isoline.route.ls.{self._get_url_string()}"

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
        path = "routing/7.2/calculateisoline.json"
        url = f"{self._base_url}/{path}"
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
