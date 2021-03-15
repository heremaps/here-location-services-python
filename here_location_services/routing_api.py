# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Routing API <https://developer.here.com/documentation/routing-api/8.17.0/dev_guide/index.html>`_.
"""  # noqa E501

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import requests

from here_location_services.config.matrix_routing_config import AvoidBoundingBox, Truck
from here_location_services.config.routing_config import PlaceOptions, Scooter, WayPointOptions

from .apis import Api
from .exceptions import ApiError


class RoutingApi(Api):
    """A class for accessing HERE routing APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, proxies, country)
        self._base_url = f"https://router.{self._get_url_string()}"

    def route(
        self,
        transport_mode: str,
        origin: List,
        destination: List,
        via: Optional[List[Tuple]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        via_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
        via_waypoint_options: Optional[WayPointOptions] = None,
        scooter: Optional[Scooter] = None,
        departure_time: Optional[datetime] = None,
        routing_mode: str = "fast",
        alternatives: int = 0,
        units: str = "metric",
        lang: str = "en-US",
        return_results: Optional[List] = None,
        spans: Optional[List] = None,
        truck: Optional[Truck] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        exclude: Optional[List[str]] = None,
    ):
        """Calculate route between two endpoints.

        See further information `here <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>_`.

        :param transport_mode: A string to represent mode of transport.
        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of tuples of ``latitude`` and ``longitude`` of via points.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param via_place_options: :class:`PlaceOptions` optinal place options for ``via``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
        :param via_waypoint_options: :class:`WayPointOptions` optional waypoint options for ``via``.
        :param scooter: Additional attributes for scooter route.
        :param departure_time: :class:`datetime.datetime` object.
        :param routing_mode: A string to represent routing mode.
        :param alternatives: Number of alternative routes to return aside from the optimal route.
            default value is ``0`` and maximum is ``6``.
        :param units: A string representing units of measurement used in guidance instructions.
            The default is metric.
        :param lang: A string representing preferred language of the response.
            The value should comply with the IETF BCP 47.
        :param return_results: A list of strings.
        :param spans: A list of strings to define which attributes are included in the response
            spans.
        :param truck: Different truck options to use during route calculation.
            use object of :class:`Truck here_location_services.config.matrix_routing_config.Truck>`
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area
            use object of :class:`AvoidBoundingBox here_location_services.config.matrix_routing_config.AvoidBoundingBox>`.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """  # noqa E501
        path = "v8/routes"
        url = f"{self._base_url}/{path}"
        params: Dict[str, str] = {
            "origin": ",".join([str(i) for i in origin]),
            "destination": ",".join([str(i) for i in destination]),
            "transportMode": transport_mode,
        }
        if via:
            lat, lng = via[0]
            via_str = f"?via={lat},{lng}"
            if len(via) > 1:
                vias = "&".join("via=" + str(item[0]) + "," + str(item[1]) for item in via[1:])
                via_str = via_str + "&" + vias
            if via_place_options:
                via_place_opt = ";".join(
                    key + "=" + str(val)
                    for key, val in vars(via_place_options).items()
                    if val is not None
                )
                via_str = via_str + ";" + via_place_opt
            if via_waypoint_options:
                via_way_opt = "!".join(
                    key + "=" + str(val)
                    for key, val in vars(via_waypoint_options).items()
                    if val is not None
                )
                via_str = via_str + "!" + via_way_opt
            url += via_str

        if departure_time:
            params["departureTime"] = departure_time.isoformat(timespec="seconds")
        params["routingMode"] = routing_mode
        params["alternatives"] = str(alternatives)
        params["units"] = units
        params["lang"] = lang
        if return_results:
            params["return"] = ",".join(return_results)
        if spans:
            params["spans"] = ",".join(spans)

        if origin_place_options:
            origin_place_opt = ";".join(
                key + "=" + str(val)
                for key, val in vars(origin_place_options).items()
                if val is not None
            )
            params["origin"] = ";".join([params["origin"], origin_place_opt])

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

        if scooter:
            if scooter.allowHighway is True:
                params["scooter[allowHighway]"] = "true"
            else:
                params["scooter[allowHighway]"] = "false"

        if truck:
            for key, val in vars(truck).items():
                if key == "shippedHazardousGoods" and val:
                    params[f"truck[{key}]"] = ",".join(val)
                elif val is not None:
                    params[f"truck[{key}]"] = val

        if avoid_features:
            params["avoid[features]"] = ",".join(avoid_features)

        if avoid_areas:
            bbox_areas = []
            for area in avoid_areas:
                area_attrs = vars(area)
                bbox_areas.append(
                    "bbox:{west},{south},{east},{north}".format(
                        west=area_attrs["west"],
                        south=area_attrs["south"],
                        east=area_attrs["east"],
                        north=area_attrs["north"],
                    )
                )
            params["avoid[areas]"] = "|".join(bbox_areas)

        if exclude:
            params["exclude"] = ",".join(exclude)

        if self.credential_params:
            params.update(self.credential_params)

        resp = requests.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)
