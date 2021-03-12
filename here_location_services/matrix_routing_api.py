"""
This module contains classes for accessing `HERE Matrix Routing API <https://developer.here.com/documentation/matrix-routing-api/8.3.0/dev_guide/index.html>`_.
"""  # noqa E501
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests

from .apis import Api
from .config.matrix_routing_config import (
    AutoCircleRegion,
    AvoidBoundingBox,
    BoundingBoxRegion,
    CircleRegion,
    PolygonRegion,
    Truck,
    WorldRegion,
)
from .exceptions import ApiError


class MatrixRoutingApi(Api):
    """A class to access Matrix Routing API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, proxies, country)
        self._base_url = f"https://matrix.router.{self._get_url_string()}"

    def __send_post_request(
        self,
        async_req: str,
        origins: List[Dict],
        region_definition: Union[
            CircleRegion, BoundingBoxRegion, PolygonRegion, AutoCircleRegion, WorldRegion
        ],
        destinations: Optional[List[Dict]] = None,
        profile: Optional[str] = None,
        departure_time: Optional[Union[datetime, str]] = None,
        routing_mode: Optional[str] = None,
        transport_mode: Optional[str] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[str]] = None,
    ) -> Dict:
        path = "v8/matrix"
        url = f"{self._base_url}/{path}"
        params = {"async": async_req}
        if self.credential_params:
            params.update(self.credential_params)
        data: Dict[Any, Any] = {
            "origins": origins,
        }
        if routing_mode:
            data["routingMode"] = routing_mode
        if transport_mode:
            data["transportMode"] = transport_mode

        regn_defn = vars(region_definition)
        data["regionDefinition"] = regn_defn
        if destinations:
            data["destinations"] = destinations
        if profile:
            data["profile"] = profile
        if departure_time:
            if isinstance(departure_time, datetime):
                data["departureTime"] = departure_time.isoformat(timespec="seconds")
            else:
                data["departureTime"] = departure_time
        if avoid_features and avoid_areas:
            avoid: Dict[str, Any] = {"features": avoid_features, "areas": []}
            for area in avoid_areas:
                avoid["areas"].append(vars(area))
            data["avoid"] = avoid
        if truck:
            data["truck"] = {k: v for k, v in vars(truck).items() if v is not None}
        if matrix_attributes:
            data["matrixAttributes"] = matrix_attributes
        resp = self.post(url, data=data, params=params)
        if resp.status_code in (200, 202):
            return resp.json()
        else:
            raise ApiError(resp)

    def matrix_route(
        self,
        origins: List[Dict],
        region_definition: Union[
            CircleRegion, BoundingBoxRegion, PolygonRegion, AutoCircleRegion, WorldRegion
        ],
        destinations: Optional[List[Dict]] = None,
        profile: Optional[str] = None,
        departure_time: Optional[Union[datetime, str]] = None,
        routing_mode: Optional[str] = None,
        transport_mode: Optional[str] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[str]] = None,
    ) -> Dict:
        """To Calculate routing matrix between multiple ``origins`` and ``destinations``
        synchronously.

        :param origins: A list of dictionaries containing lat and long for origin points.
        :param region_definition: Definition of a region in which the matrix will be calculated.
            Use object of atleast one of the following regions:
            :class:`here_location_services.config.matrix_routing_config.CircleRegion`
            :class:`here_location_services.config.matrix_routing_config.BoundingBoxRegion`
            :class:`here_location_services.config.matrix_routing_config.PolygonRegion`
            :class:`here_location_services.config.matrix_routing_config.AutoCircleRegion`
            :class:`here_location_services.config.matrix_routing_config.WorldRegion`
        :param destinations: A list of dictionaries containing lat and long for destination points.
            When no destinations are specified the matrix is assumed to be quadratic with origins
            used as destinations.
        :param profile: A string to represent profile id. A set predefined profile ids for route
            calculation can be used from config
            :attr:`PROFILE <here_location_services.config.matrix_routing_config.PROFILE>`
        :param departure_time: :class:`datetime.datetime` object.
        :param routing_mode: A string to represent routing mode. Routing mode values are defined
            in :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`
        :param transport_mode: A string to represent transport mode. Transport modes are defined
            in :attr:`ROUTING_TRANSPORT_MODE <here_location_services.config.routing_config.ROUTING_TRANSPORT_MODE>`
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.matrix_routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area
            use object of :class:`AvoidBoundingBox here_location_services.config.matrix_routing_config.AvoidBoundingBox>`
        :param truck: Different truck options to use during route calculation when
            transportMode = truck. use object of :class:`Truck here_location_services.config.matrix_routing_config.Truck>`
        :param matrix_attributes: Defines which attributes are included in the response as part of
            the data representation of the matrix entries summaries. Matrix attributes are defined
            in :attr:`MATRIX_ATTRIBUTES <here_location_services.config.matrix_routing_config.MATRIX_ATTRIBUTES>`
        :return: :class:`requests.Response` object.
        """  # noqa E501
        return self.__send_post_request(
            async_req="false",
            origins=origins,
            region_definition=region_definition,
            destinations=destinations,
            profile=profile,
            departure_time=departure_time,
            routing_mode=routing_mode,
            transport_mode=transport_mode,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            truck=truck,
            matrix_attributes=matrix_attributes,
        )

    def matrix_route_async(
        self,
        origins: List[Dict],
        region_definition: Union[
            CircleRegion, BoundingBoxRegion, PolygonRegion, AutoCircleRegion, WorldRegion
        ],
        destinations: Optional[List[Dict]] = None,
        profile: Optional[str] = None,
        departure_time: Optional[Union[datetime, str]] = None,
        routing_mode: Optional[str] = None,
        transport_mode: Optional[str] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[str]] = None,
    ) -> Dict:
        """To Calculate routing matrix between multiple ``origins`` and ``destinations``
        asynchronously.

        :param origins: A list of dictionaries containing lat and long for origin points.
        :param region_definition: Definition of a region in which the matrix will be calculated.
            Use object of atleast one of the following regions:
            :class:`here_location_services.config.matrix_routing_config.CircleRegion`
            :class:`here_location_services.config.matrix_routing_config.BoundingBoxRegion`
            :class:`here_location_services.config.matrix_routing_config.PolygonRegion`
            :class:`here_location_services.config.matrix_routing_config.AutoCircleRegion`
            :class:`here_location_services.config.matrix_routing_config.WorldRegion`
        :param destinations: A list of dictionaries containing lat and long for destination points.
            When no destinations are specified the matrix is assumed to be quadratic with origins
            used as destinations.
        :param profile: A string to represent profile id. A set predefined profile ids for route
            calculation can be used from config
            :attr:`PROFILE <here_location_services.config.matrix_routing_config.PROFILE>`
        :param departure_time: :class:`datetime.datetime` object.
        :param routing_mode: A string to represent routing mode. Routing mode values are defined
            in :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`
        :param transport_mode: A string to represent transport mode. Transport modes are defined
            in :attr:`ROUTING_TRANSPORT_MODE <here_location_services.config.routing_config.ROUTING_TRANSPORT_MODE>`
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.matrix_routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area
            use object of :class:`AvoidBoundingBox here_location_services.config.matrix_routing_config.AvoidBoundingBox>`
        :param truck: Different truck options to use during route calculation when
            transportMode = truck. use object of :class:`Truck here_location_services.config.matrix_routing_config.Truck>`
        :param matrix_attributes: Defines which attributes are included in the response as part of
            the data representation of the matrix entries summaries. Matrix attributes are defined
            in :attr:`MATRIX_ATTRIBUTES <here_location_services.config.matrix_routing_config.MATRIX_ATTRIBUTES>`
        :return: :class:`requests.Response` object.
        """  # noqa E501
        return self.__send_post_request(
            async_req="true",
            origins=origins,
            region_definition=region_definition,
            destinations=destinations,
            profile=profile,
            departure_time=departure_time,
            routing_mode=routing_mode,
            transport_mode=transport_mode,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            truck=truck,
            matrix_attributes=matrix_attributes,
        )

    def get_async_matrix_route_status(self, status_url: str) -> requests.Response:
        """Get the status of async matrix calculation for the provided status url."""
        return self.get(status_url, allow_redirects=False)

    def get_async_matrix_route_results(self, result_url: str) -> requests.Response:
        """Get the results of async matrix calculation for the provided result url."""
        resp = self.get(result_url)
        if resp.status_code != 200:
            raise ApiError(resp)
        return resp.json()
