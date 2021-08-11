# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Routing API <https://developer.here.com/documentation/routing/dev_guide/topics/request-isoline.html>`_.
"""  # noqa E501
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from here_location_services.platform.auth import Auth

from .apis import Api
from .config.base_config import PlaceOptions, Truck, WayPointOptions
from .exceptions import ApiError


class IsolineRoutingApi(Api):
    """A class for accessing HERE isoline routing API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, auth=auth, proxies=proxies, country=country)
        self._base_url = f"https://isoline.router.{self._get_url_string()}"

    def get_isoline_routing(
        self,
        range: str,
        range_type: str,
        transport_mode: str,
        origin: Optional[List] = None,
        departure_time: Optional[datetime] = None,
        destination: Optional[List] = None,
        arrival_time: Optional[datetime] = None,
        routing_mode: Optional[str] = "fast",
        shape_max_points: Optional[int] = None,
        optimised_for: Optional[str] = "balanced",
        avoid_features: Optional[List[str]] = None,
        truck: Optional[Truck] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
    ) -> requests.Response:
        """Get isoline routing.

        Request a polyline that connects the endpoints of all routes
        leaving from one defined center with either a specified length
        or specified travel time.

        :param range: A string representing a range of isoline, unit is defined by
            parameter ``range_type``. Example: range='1000' or range='1000,2000,3000'
        :param range_type: A string representing a type of ``range``. Possible values are
            ``distance``, ``time`` and ``consumption``. For distance the unit meters. For a
            time the unit is seconds. For consumption, it is defined by the consumption
            model.
        :param transport_mode: A string representing Mode of transport to be used for the
            calculation of the isolines.
            Example: ``car``.
        :param origin: Center of the isoline request. The Isoline(s) will cover the region
            which can be reached from this point within given range. It cannot be used in
            combination with ``destination`` parameter.
        :param departure_time: Specifies the time of departure as defined by either date-time
            or full-date partial-time in RFC 3339, section 5.6 (for example, 2019-06-24T01:23:45).
            The requested time is converted to the local time at origin. When the optional timezone
            offset is not specified, time is assumed to be local. If neither departure_time or
            arrival_time are specified, current time at departure location will be used. All Time
            values in the response are returned in the timezone of each location.
        :param destination: Center of the isoline request. The Isoline(s) will cover the
            region within the specified range that can reach this point. It cannot be used
            in combination with ``origin`` parameter.
        :param arrival_time: Specifies the time of arrival as defined by either date-time or
            full-date T partial-time in RFC 3339, section 5.6 (for example, 2019-06-24T01:23:45).
            The requested time is converted to the local time at destination. When the optional
            timezone offset is not specified, time is assumed to be local. All Time values in
            the response are returned in the timezone of each location.
        :param routing_mode: A string to represent routing mode.
        :param shape_max_points: An integer to Limit the number of points in the resulting isoline
            geometry. If the isoline consists of multiple components, the sum of points from all
            components is considered. This parameter doesn't affect performance.
        :param optimised_for: A string to specify how isoline calculation is optimized.
        :param avoid_features: Avoid routes that violate these properties. Avoid features
            are defined in :attr:
            `AVOID_FEATURES <here_location_services.config.isoline_routing_config.AVOID_FEATURES>`
        :param truck: Different truck options to use during route calculation when transport_mode
            = truck. use object of :class:`Truck here_location_services.config.base_config.Truck>`
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """
        path = "v8/isolines"
        url = f"{self._base_url}/{path}"
        params: Dict[str, Any] = {
            "range[type]": range_type,
            "range[values]": range,
            "transportMode": transport_mode,
        }
        if origin:
            params["origin"] = ",".join([str(i) for i in origin])
        if destination:
            params["destination"] = ",".join([str(i) for i in destination])
        if arrival_time:
            params["arrivalTime"] = arrival_time.isoformat(timespec="seconds")
        if departure_time:
            params["departureTime"] = departure_time.isoformat(timespec="seconds")
        if routing_mode:
            params["routingMode"] = routing_mode
        if optimised_for:
            params["optimizeFor"] = optimised_for
        if avoid_features:
            avoid: Dict[str, Any] = {"features": avoid_features}
            params["avoid"] = avoid
        if truck:
            params["truck"] = {k: v for k, v in vars(truck).items() if v is not None}
        if shape_max_points:
            params["shape[maxPoints]"] = shape_max_points

        if origin_place_options:
            origin_place_opt = ";".join(
                key + "=" + str(val)
                for key, val in vars(origin_place_options).items()
                if val is not None
            )
            params["origin"] = ";".join([params["origin"], origin_place_opt])

        if origin_waypoint_options:
            origin_way_opt = "!".join(
                key + "=" + str(val)
                for key, val in vars(origin_waypoint_options).items()
                if val is not None
            )
            params["origin"] = "!".join([params["origin"], origin_way_opt])

        if destination_place_options:
            dest_place_opt = ";".join(
                key + "=" + str(val)
                for key, val in vars(destination_place_options).items()
                if val is not None
            )
            params["destination"] = ";".join([params["destination"], dest_place_opt])

        if destination_waypoint_options:
            dest_way_opt = "!".join(
                key + "=" + str(val)
                for key, val in vars(destination_waypoint_options).items()
                if val is not None
            )
            params["destination"] = "!".join([params["destination"], dest_way_opt])
        resp = self.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
