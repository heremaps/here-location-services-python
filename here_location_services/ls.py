# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains class to interact with Location services REST APIs."""

import os
import urllib
import urllib.request
from datetime import date, datetime
from time import sleep
from typing import Dict, List, Optional, Tuple, Union

from geojson import LineString, MultiPolygon, Point, Polygon

from here_location_services.config.routing_config import Scooter, Via
from here_location_services.platform.apis.aaa_oauth2_api import AAAOauth2Api
from here_location_services.platform.auth import Auth
from here_location_services.platform.credentials import PlatformCredentials

from .autosuggest_api import AutosuggestApi
from .config.autosuggest_config import SearchCircle
from .config.base_config import PlaceOptions, Truck, WayPointOptions
from .config.matrix_routing_config import (
    AutoCircleRegion,
    AvoidBoundingBox,
    BoundingBoxRegion,
    CircleRegion,
    PolygonRegion,
    WorldRegion,
)
from .destination_weather_api import DestinationWeatherApi
from .exceptions import ApiError
from .geocoding_search_api import GeocodingSearchApi
from .isoline_routing_api import IsolineRoutingApi
from .matrix_routing_api import MatrixRoutingApi
from .responses import (
    AutosuggestResponse,
    BrowseResponse,
    DestinationWeatherResponse,
    DiscoverResponse,
    GeocoderResponse,
    IsolineResponse,
    LookupResponse,
    MatrixRoutingResponse,
    ReverseGeocoderResponse,
    RoutingResponse,
)
from .routing_api import RoutingApi


class LS:
    """
    A single interface for the user to interact with rest of
    the Location services APIs.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        platform_credentials: Optional[PlatformCredentials] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        api_key = api_key or os.environ.get("LS_API_KEY")
        self.auth: Optional[Auth] = None
        if not api_key:
            credentials = platform_credentials or PlatformCredentials.from_default()
            aaa_oauth2_api = AAAOauth2Api(
                base_url=credentials.cred_properties["endpoint"], proxies={}
            )
            self.auth = Auth(credentials=credentials, aaa_oauth2_api=aaa_oauth2_api)

        self.proxies = proxies or urllib.request.getproxies()
        self.geo_search_api = GeocodingSearchApi(
            api_key=api_key,
            auth=self.auth,
            proxies=proxies,
            country=country,
        )
        self.isoline_routing_api = IsolineRoutingApi(
            api_key=api_key,
            auth=self.auth,
            proxies=proxies,
            country=country,
        )
        self.routing_api = RoutingApi(
            api_key=api_key,
            auth=self.auth,
            proxies=proxies,
            country=country,
        )
        self.matrix_routing_api = MatrixRoutingApi(
            api_key=api_key, auth=self.auth, proxies=proxies, country=country
        )
        self.autosuggest_api = AutosuggestApi(
            api_key=api_key,
            auth=self.auth,
            proxies=proxies,
            country=country,
        )
        self.destination_weather_api = DestinationWeatherApi(
            api_key=api_key,
            auth=self.auth,
            proxies=proxies,
            country=country,
        )

    def geocode(self, query: str, limit: int = 20, lang: str = "en-US") -> GeocoderResponse:
        """Calculate coordinates as result of geocoding for the given ``query``.

        :param query: A string containing the input query.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 20.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :raises ValueError: If ``query`` is empty or having all whitespace characters.
        :return: :class:`GeocoderResponse` object.
        """
        if not query or query.isspace():
            raise ValueError(f"Invalid input query: {query}")

        resp = self.geo_search_api.get_geocoding(query, limit=limit, lang=lang)
        return GeocoderResponse.new(resp.json())

    def reverse_geocode(
        self, lat: float, lng: float, limit: int = 1, lang: str = "en-US"
    ) -> ReverseGeocoderResponse:
        """
        Return the address label string as the result of reverse-geocoding the
        given ``latitude`` and ``longitude``.

        :param lat: A float representing latitude of point.
        :param lng: A float representing longitude of point.
        :param limit: An int representing maximum number of results to be returned.
            Default value is 1.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :raises ValueError: If Latitude is not in range between -90 and 90 or
             Longitude is not in range between -180 and 180.
        :return: :class:`ReverseGeocoderResponse` object.
        """
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be in range -90 to 90.")
        if not -180 <= lng <= 180:
            raise ValueError("Longitude must be in range -180 to 180.")

        resp = self.geo_search_api.get_reverse_geocoding(lat=lat, lng=lng, limit=limit, lang=lang)
        return ReverseGeocoderResponse.new(resp.json())

    def calculate_isoline(
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
    ) -> IsolineResponse:
        """Calculate isoline routing.

        Request a polyline that connects the endpoints of all routes
        leaving from one defined center with either a specified length
        or specified travel time.

        :param range: A string representing a range of isoline, unit is defined by
            parameter range type. Example: range='1000' or range='1000,2000,3000'
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
        :raises ValueError: If ``origin`` and ``destination`` are provided together.
        :return: :class:`IsolineResponse` object.
        """

        if origin and destination:
            raise ValueError("`origin` and `destination` can not be provided together.")
        if origin is None and destination is None:
            raise ValueError("please provide either `origin` or `destination`.")
        if departure_time and origin is None:
            raise ValueError("`departure_time` must be provided with `origin`")
        if arrival_time and destination is None:
            raise ValueError("`arrival` must be provided with `destination`")

        resp = self.isoline_routing_api.get_isoline_routing(
            range=range,
            range_type=range_type,
            transport_mode=transport_mode,
            origin=origin,
            departure_time=departure_time,
            destination=destination,
            arrival_time=arrival_time,
            routing_mode=routing_mode,
            shape_max_points=shape_max_points,
            optimised_for=optimised_for,
            avoid_features=avoid_features,
            truck=truck,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
        )
        response = IsolineResponse.new(resp.json())

        if response.notices:
            raise ValueError("Isolines could not be calculated.")
        return response

    def autosuggest(
        self,
        query: str,
        at: Optional[List] = None,
        search_in_circle: Optional[SearchCircle] = None,
        search_in_bbox: Optional[Tuple] = None,
        in_country: Optional[List[str]] = None,
        limit: Optional[int] = 20,
        terms_limit: Optional[int] = None,
        lang: Optional[List[str]] = None,
        political_view: Optional[str] = None,
        show: Optional[List[str]] = None,
    ) -> AutosuggestResponse:
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
        :raises ValueError: If ``search_in_circle``,``search_in_bbox`` and ``destination``
            are provided together.
        """

        i = iter([search_in_circle, search_in_bbox, at])
        if not (any(i) and not any(i)):
            raise ValueError(
                "Exactly one of `search_in_circle` or `search_in_bbox` or `at` must be provided."
            )

        resp = self.autosuggest_api.get_autosuggest(
            query=query,
            at=at,
            search_in_bbox=search_in_bbox,
            search_in_circle=search_in_circle,
            in_country=in_country,
            limit=limit,
            terms_limit=terms_limit,
            lang=lang,
            political_view=political_view,
            show=show,
        )
        response = AutosuggestResponse.new(resp.json())

        return response

    def get_dest_weather(
        self,
        products: List[str],
        at: Optional[List] = None,
        query: Optional[str] = None,
        zipcode: Optional[str] = None,
        hourly_date: Optional[Union[date, datetime]] = None,
        one_observation: Optional[bool] = None,
        language: Optional[str] = None,
        units: Optional[str] = None,
    ) -> DestinationWeatherResponse:
        """Retrieves weather reports, weather forecasts, severe weather alerts
            and moon and sun rise and set information.

        :param products: List of :class:`DestWeatherProduct` identifying the type of
            report to obtain.
        :param at: A list of ``latitude`` and ``longitude`` specifying the area covered
            by the weather report.
        :param query: Free text query. Examples: "125, Berliner, berlin", "Beacon, Boston"
        :param zipcode: ZIP code of the location. This parameter is supported only for locations in
            the United States of America.
        :param hourly_date: Date for which hourly forecasts are to be retrieved. Can be either a
            `date` or `datetime` object
        :param one_observation: Boolean, if set to true, the response only includes the closest
            location. Only available when the `product` parameter is set to
            `DEST_WEATHER_PRODUCT.observation`.
        :param language: Defines the language used in the descriptions in the response.
        :param units: Defines whether units or imperial units are used in the response.
        :raises ValueError: If neither `at`, `query` or `zipcode` are passed.
        :raises ValueError: If `one_observation` is set to true without passing
            DEST_WEATHER_PRODUCT.observation in `products`
        :return: :class:`DestinationWeatherResponse` object.
        """

        if at is None and query is None and zipcode is None:
            raise ValueError("please provide either `at` or `query` or `zipcode`.")
        if "observation" not in products and one_observation:
            raise ValueError(
                "`one_observation` can only be set when the `products` parameter "
                + "is set to DEST_WEATHER_PRODUCT.observation"
            )

        resp = self.destination_weather_api.get_dest_weather(
            products=products,
            at=at,
            query=query,
            zipcode=zipcode,
            hourly_date=hourly_date,
            one_observation=one_observation,
            language=language,
            units=units,
        )
        response = DestinationWeatherResponse.new(resp.json())
        return response

    def get_weather_alerts(
        self,
        geometry: Union[Point, LineString, Polygon, MultiPolygon],
        start_time: datetime,
        id: Optional[str] = None,
        weather_severity: Optional[int] = None,
        weather_type: Optional[str] = None,
        country: Optional[str] = None,
        end_time: Optional[datetime] = None,
        width: Optional[int] = 50000,
    ) -> DestinationWeatherResponse:
        """Retrieves weather reports, weather forecasts, severe weather alerts
            and moon and sun rise and set information.

        :param geometry: Point or LineString or Polygon or MultiPolygon defining the route or
            a single location
        :param start_time: Start time of the event
        :param id: Unique weather alert id.
        :param weather_severity: Defines the severity of the weather event as defined
            in :class:`WeatherSeverity`.
        :param weather_type: Defines the type of the weather event as defined
            in :class:`WeatherType`.
        :param country: String for ISO-3166-1 2-letter country code.
        :param end_time: End time of the event. If not present, warning is valid until
            it is not removed from the feed by national weather institutes
            (valid until warning is present in the response)
        :param width: int. default 50000
        :return: :class:`DestinationWeatherResponse` object.
        """

        resp = self.destination_weather_api.get_weather_alerts(
            geometry=geometry,
            id=id,
            weather_severity=weather_severity,
            weather_type=weather_type,
            country=country,
            start_time=start_time,
            end_time=end_time,
            width=width,
        )
        response = DestinationWeatherResponse.new(resp.json())
        return response

    def discover(
        self,
        query: str,
        center: Optional[List[float]] = None,
        radius: Optional[int] = None,
        country_codes: Optional[List] = None,
        bounding_box: Optional[List[float]] = None,
        limit: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> DiscoverResponse:
        """Search places using Location Services discover endpoint.

        This method uses location services ``discover`` endpoint to search places based on
        query which is free-form text.
        There are three different combination of inputs as shown below to search places
        using discover:

        - ``center`` and ``country_code``
        - ``center`` and ``radius``
        - ``bounding_box``

        :param query: A string representing free-text query to search places.
        :param center: A list of latitude and longitude representing the center for
            search query.
        :param radius: A radius in meters along with center for searching places.
        :param country_codes: A list of  ISO 3166-1 alpha-3 country codes.
        :param bounding_box: A bounding box, provided as west longitude, south latitude,
            east longitude, north latitude.
        :param limit: An int representing maximum number of results to be returned.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :raises ValueError: If ``center`` and ``bounding_box`` are provided together.
        :return: :class:`DiscoverResponse` object.
        """
        if center and bounding_box:
            raise ValueError(
                f"Params: center:{center} and bounding_box:{bounding_box} "
                f"can not be provided together."
            )

        resp = self.geo_search_api.get_search_discover(
            query=query,
            center=center,
            radius=radius,
            country_codes=country_codes,
            bounding_box=bounding_box,
            limit=limit,
            lang=lang,
        )
        return DiscoverResponse.new(resp.json())

    def browse(
        self,
        center: List,
        radius: Optional[int] = None,
        country_codes: Optional[List] = None,
        bounding_box: Optional[List[float]] = None,
        categories: Optional[List] = None,
        limit: Optional[int] = None,
        name: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> BrowseResponse:
        """Get search results for places based on different filters such as categories or name.

        :param center: A list of latitude and longitude representing the center for
            search query.
        :param radius: A radius in meters along with center for searching places.
        :param country_codes: A list of  ISO 3166-1 alpha-3 country codes.
        :param bounding_box: A bounding box, provided as west longitude, south latitude,
            east longitude, north latitude.
        :param categories: A list strings of category-ids.
        :param limit: An int representing maximum number of results to be returned.
        :param name: A string representing Full-text filter on POI names/titles.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`BrowseResponse` object.
        """
        resp = self.geo_search_api.get_search_browse(
            center=center,
            radius=radius,
            country_codes=country_codes,
            bounding_box=bounding_box,
            categories=categories,
            limit=limit,
            name=name,
            lang=lang,
        )
        return BrowseResponse.new(resp.json())

    def lookup(self, location_id: str, lang: Optional[str] = None) -> LookupResponse:
        """
        Get search results by providing ``location_id``.

        :param location_id: A string representing id.
        :param lang: A string to represent language to be used for result rendering from
            a list of BCP47 compliant Language Codes.
        :return: :class:`LookupResponse` object.
        """
        resp = self.geo_search_api.get_search_lookup(location_id=location_id, lang=lang)
        return LookupResponse.new(resp.json())

    def car_route(
        self,
        origin: List,
        destination: List,
        via: Optional[List[Via]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
        departure_time: Optional[datetime] = None,
        routing_mode: str = "fast",
        alternatives: int = 0,
        units: str = "metric",
        lang: str = "en-US",
        return_results: Optional[List] = None,
        spans: Optional[List] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        exclude: Optional[List[str]] = None,
    ) -> RoutingResponse:
        """Calculate ``car`` route between two endpoints.

        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of :class:`Via` objects.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
        :param departure_time: :class:`datetime.datetime` object.
        :param routing_mode: A string to represent routing mode. use config defined in :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`
        :param alternatives: Number of alternative routes to return aside from the optimal route.
            default value is ``0`` and maximum is ``6``.
        :param units: A string representing units of measurement used in guidance instructions.
            The default is metric.
        :param lang: A string representing preferred language of the response.
            The value should comply with the IETF BCP 47.
        :param return_results: A list of strings.
        :param spans: A list of strings to define which attributes are included in the response
            spans. use config defined in :attr:`ROUTING_SPANS <here_location_services.config.routing_config.ROUTING_SPANS>`
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`RoutingResponse` object.
        """  # noqa: E501

        resp = self.routing_api.route(
            transport_mode="car",
            origin=origin,
            destination=destination,
            via=via,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
            departure_time=departure_time,
            routing_mode=routing_mode,
            alternatives=alternatives,
            units=units,
            lang=lang,
            return_results=return_results,
            spans=spans,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            exclude=exclude,
        )
        return RoutingResponse.new(resp.json())

    def bicycle_route(
        self,
        origin: List,
        destination: List,
        via: Optional[List[Via]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
        departure_time: Optional[datetime] = None,
        routing_mode: str = "fast",
        alternatives: int = 0,
        units: str = "metric",
        lang: str = "en-US",
        return_results: Optional[List] = None,
        spans: Optional[List] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        exclude: Optional[List[str]] = None,
    ) -> RoutingResponse:
        """Calculate ``bicycle`` route between two endpoints.

        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of :class:`Via` objects.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
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
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`RoutingResponse` object.
        """  # noqa E501
        resp = self.routing_api.route(
            transport_mode="bicycle",
            origin=origin,
            destination=destination,
            via=via,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
            departure_time=departure_time,
            routing_mode=routing_mode,
            alternatives=alternatives,
            units=units,
            lang=lang,
            return_results=return_results,
            spans=spans,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            exclude=exclude,
        )
        return RoutingResponse.new(resp.json())

    def truck_route(
        self,
        origin: List,
        destination: List,
        via: Optional[List[Via]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
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
    ) -> RoutingResponse:
        """Calculate ``truck`` route between two endpoints.

        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of :class:`Via` objects.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
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
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`RoutingResponse` object.
        """  # noqa E501
        resp = self.routing_api.route(
            transport_mode="truck",
            origin=origin,
            destination=destination,
            via=via,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
            departure_time=departure_time,
            routing_mode=routing_mode,
            alternatives=alternatives,
            units=units,
            lang=lang,
            return_results=return_results,
            spans=spans,
            truck=truck,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            exclude=exclude,
        )
        return RoutingResponse.new(resp.json())

    def scooter_route(
        self,
        origin: List,
        destination: List,
        via: Optional[List[Via]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
        scooter: Optional[Scooter] = None,
        departure_time: Optional[datetime] = None,
        routing_mode: str = "fast",
        alternatives: int = 0,
        units: str = "metric",
        lang: str = "en-US",
        return_results: Optional[List] = None,
        spans: Optional[List] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        exclude: Optional[List[str]] = None,
    ) -> RoutingResponse:
        """Calculate ``scooter`` route between two endpoints.

        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of :class:`Via` objects.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
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
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`RoutingResponse` object.
        """  # noqa E501
        resp = self.routing_api.route(
            transport_mode="scooter",
            origin=origin,
            destination=destination,
            via=via,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
            scooter=scooter,
            departure_time=departure_time,
            routing_mode=routing_mode,
            alternatives=alternatives,
            units=units,
            lang=lang,
            return_results=return_results,
            spans=spans,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            exclude=exclude,
        )
        return RoutingResponse.new(resp.json())

    def pedestrian_route(
        self,
        origin: List,
        destination: List,
        via: Optional[List[Via]] = None,
        origin_place_options: Optional[PlaceOptions] = None,
        origin_waypoint_options: Optional[WayPointOptions] = None,
        destination_place_options: Optional[PlaceOptions] = None,
        destination_waypoint_options: Optional[WayPointOptions] = None,
        departure_time: Optional[datetime] = None,
        routing_mode: str = "fast",
        alternatives: int = 0,
        units: str = "metric",
        lang: str = "en-US",
        return_results: Optional[List] = None,
        spans: Optional[List] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        exclude: Optional[List[str]] = None,
    ) -> RoutingResponse:
        """Calculate ``pedestrian`` route between two endpoints.

        :param origin: A list of ``latitude`` and ``longitude`` of origin point of route.
        :param destination: A list of ``latitude`` and ``longitude`` of destination point of route.
        :param via: A list of :class:`Via` objects.
        :param origin_place_options: :class:`PlaceOptions` optinal place options for ``origin``.
        :param origin_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``origin``.
        :param destination_place_options: :class:`PlaceOptions` optinal place options
            for ``destination``.
        :param destination_waypoint_options: :class:`WayPointOptions` optional waypoint options
            for ``destination``.
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
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area.
        :param exclude: A comma separated list of three-letter country codes
            (ISO-3166-1 alpha-3 code) that routes will exclude.
        :return: :class:`RoutingResponse` object.
        """  # noqa E501
        resp = self.routing_api.route(
            transport_mode="pedestrian",
            origin=origin,
            destination=destination,
            via=via,
            origin_place_options=origin_place_options,
            origin_waypoint_options=origin_waypoint_options,
            destination_place_options=destination_place_options,
            destination_waypoint_options=destination_waypoint_options,
            departure_time=departure_time,
            routing_mode=routing_mode,
            alternatives=alternatives,
            units=units,
            lang=lang,
            return_results=return_results,
            spans=spans,
            avoid_features=avoid_features,
            avoid_areas=avoid_areas,
            exclude=exclude,
        )
        return RoutingResponse.new(resp.json())

    def matrix(
        self,
        origins: List[Dict],
        region_definition: Union[
            CircleRegion,
            BoundingBoxRegion,
            PolygonRegion,
            AutoCircleRegion,
            WorldRegion,
        ],
        async_req: bool = False,
        destinations: Optional[List[Dict]] = None,
        profile: Optional[str] = None,
        departure_time: Optional[Union[datetime, str]] = None,
        routing_mode: Optional[str] = None,
        transport_mode: Optional[str] = None,
        avoid_features: Optional[List[str]] = None,
        avoid_areas: Optional[List[AvoidBoundingBox]] = None,
        truck: Optional[Truck] = None,
        matrix_attributes: Optional[List[str]] = None,
    ) -> MatrixRoutingResponse:
        """
        Calculate routing matrix between multiple ``origins`` and ``destinations`` using
        synchronous and asynchronous requests.

        A routing matrix is a matrix with rows labeled by origins and columns by destinations.
        Each entry of the matrix is travel time or distance from the origin to the destination.
        The response contains 2 optional flat arrays ``TravelTimes`` and ``distances`` depending
        upon the specified ``matrix_attributes``. Each array represents a 2D matrix where rows (i)
        corresponds to ``origins`` and columns (j) to destinations. The kth position in the array
        corresponds to the (i, j) position in the matrix defined by the following relationship:
        k = num_destitions * i + j.

        :param origins: A list of dictionaries containing lat and long for origin points.
        :param region_definition: Definition of a region in which the matrix will be calculated.
            Use object of atleast one of the following regions:

            :class:`CircleRegion <here_location_services.config.matrix_routing_config.CircleRegion>`

            :class:`BoundingBoxRegion <here_location_services.config.matrix_routing_config.BoundingBoxRegion>`

            :class:`PolygonRegion <here_location_services.config.matrix_routing_config.PolygonRegion>`

            :class:`AutoCircleRegion <here_location_services.config.matrix_routing_config.AutoCircleRegion>`

            :class:`WorldRegion <here_location_services.config.matrix_routing_config.WorldRegion>`
        :param async_req: If set to True reuqests will be sent to asynchronous matrix routing API
            else It will be sent to synchronous matrix routing API. For larger matrices, or longer
            routes, or routes in denser road networks, it is recommended to set to True.
        :param destinations: A list of dictionaries containing lat and long for destination points.
            When no destinations are specified the matrix is assumed to be quadratic with origins
            used as destinations.
        :param profile: A string to represent profile id. A set predefined profile ids for route
            calculation can be used from config
            :attr:`PROFILE <here_location_services.config.matrix_routing_config.PROFILE>`
        :param departure_time: :class:`datetime.datetime` object with explicit timezone. When
            departure_time is not specified, it is implicitly assumed to be the current time.
            The special value ``any`` enforces non time-aware routing.
        :param routing_mode: A string to represent routing mode. Routing mode values are defined
            in :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`
        :param transport_mode: A string to represent transport mode. Transport modes are defined
            in :attr:`ROUTING_TRANSPORT_MODE <here_location_services.config.routing_config.ROUTING_TRANSPORT_MODE>`
        :param avoid_features: Avoid routes that violate these properties. Avoid features are
            defined in :attr:`AVOID_FEATURES <here_location_services.config.matrix_routing_config.AVOID_FEATURES>`
        :param avoid_areas: A list of areas to avoid during route calculation. To define avoid area
            use object of :class:`AvoidBoundingBox <here_location_services.config.matrix_routing_config.AvoidBoundingBox>`
        :param truck: Different truck options to use during route calculation when
            transport_mode = truck. use object of :class:`Truck <here_location_services.config.matrix_routing_config.Truck>`
        :param matrix_attributes: Defines which attributes are included in the response as part of
            the data representation of the matrix entries summaries. Matrix attributes are defined
            in :attr:`MATRIX_ATTRIBUTES <here_location_services.config.matrix_routing_config.MATRIX_ATTRIBUTES>`
        :raises ValueError: If conflicting options are provided.
        :raises ApiError: If API response status code is not as expected.
        :return: :class:`MatrixRoutingResponse` object.
        """  # noqa E501
        if profile and type(region_definition) != WorldRegion:
            raise ValueError("profile must be used with WorldRegion only.")
        if truck and transport_mode != "truck":
            raise ValueError("Truck option must be used when transport_mode is truck")
        if async_req is True:
            resp = self.matrix_routing_api.matrix_route_async(
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
            status_url = resp["statusUrl"]
            while True:
                resp_status = self.matrix_routing_api.get_async_matrix_route_status(status_url)
                if resp_status.status_code == 200 and resp_status.json().get("error"):
                    raise ApiError(resp_status)
                elif resp_status.status_code == 303:
                    result_url = resp_status.json()["resultUrl"]
                    break
                elif resp_status.status_code in (401, 403, 404, 500):
                    raise ApiError(resp_status)
                sleep(2)
            result = self.matrix_routing_api.get_async_matrix_route_results(result_url)
            return MatrixRoutingResponse.new(result)
        else:
            resp = self.matrix_routing_api.matrix_route(
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
            return MatrixRoutingResponse.new(resp)
