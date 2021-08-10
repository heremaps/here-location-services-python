# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module defines all the base classes which will be used for configuration classes of
various APIs.
"""

import json
from typing import List, Optional


class Bunch(dict):
    """A class for dot notation implementation of dictionary."""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


class RoutingMode(Bunch):
    """A Class to define constant values for Routing Modes.

    ``fast``:
    Route calculation from start to destination optimized by travel time. In many cases, the route
    returned by the fast mode may not be the route with the fastest possible travel time.
    For example, the routing service may favor a route that remains on a highway, even
    if a faster travel time can be achieved by taking a detour or shortcut through
    an inconvenient side road.

    ``short``:
    Route calculation from start to destination disregarding any speed information. In this mode,
    the distance of the route is minimized, while keeping the route sensible. This includes,
    for example, penalizing turns. Because of that, the resulting route will not necessarily be
    the one with minimal distance.
    """


#: Use this config for routing_mode of routing API.
#: Example: for ``fast`` routing_mode use ``ROUTING_MODE.fast``.
ROUTING_MODE = RoutingMode(**{"fast": "fast", "short": "short"})


class ShippedHazardousGoods(Bunch):
    """A class to define the constant values for truck option ``shippedHazardousGoods``."""


#: Use this config for shipped_hazardous_goods attribute of Truck options of matrix Routing API.
#: Example: for ``explosive`` shipped_hazardous_goods  use ``SHIPPED_HAZARDOUS_GOODS.explosive``.
SHIPPED_HAZARDOUS_GOODS = ShippedHazardousGoods(
    **{
        "explosive": "explosive",
        "gas": "gas",
        "flammable": "flammable",
        "combustible": "combustible",
        "organic": "organic",
        "poison": "poison",
        "radioactive": "radioactive",
        "corrosive": "corrosive",
        "poisonousInhalation": "poisonousInhalation",
        "harmfulToWater": "harmfulToWater",
        "other": "other",
    }
)


class Truck:
    """A class to define different truck options which will be used during route calculation.
    Truck options should be used when transport_mode is ``truck``.
    """

    def __init__(
        self,
        shipped_hazardous_goods: Optional[List] = None,
        gross_weight: Optional[int] = None,
        weight_per_axle: Optional[int] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        length: Optional[int] = None,
        tunnel_category: Optional[str] = None,
        axle_count: Optional[int] = None,
        truck_type: str = "straight",
        trailer_count: int = 0,
    ):
        """Object Initializer.

        :param shipped_hazardous_goods: List of hazardous materials in the vehicle. valid values
            for hazardous materials can be used from config
            :attr:`SHIPPED_HAZARDOUS_GOODS <here_location_services.config.matrix_routing_config.SHIPPED_HAZARDOUS_GOODS>`
        :param gross_weight: Total vehicle weight, including trailers and shipped goods, in
            kilograms. Should be greater than or equal to zero.
        :param weight_per_axle: Vehicle weight per axle, in kilograms. Should be greater than or
            equal to zero.
        :param height: Vehicle height, in centimeters. Should be in range [0, 5000]
        :param width: Vehicle width, in centimeters. Should be in range [0, 5000]
        :param length: Vehicle length, in centimeters. Should be in range [0, 5000]
        :param tunnel_category: A string for category of tunnel. Valid values are "B", "C", "D", "E".
            Specifies the `cargo tunnel restriction code <https://adrbook.com/en/2017/ADR/8.6.3>`_.
            The route will pass only through tunnels of less restrictive categories.
        :param axle_count: Total number of axles that the vehicle has. Should be in the
            range [2, 255].
        :param truck_type: A string to represent the type of truck.
        :param trailer_count: Number of trailers attached to the vehicle.
        """  # noqa E501
        self.shippedHazardousGoods = shipped_hazardous_goods
        self.grossWeight = gross_weight
        self.weightPerAxle = weight_per_axle
        self.height = height
        self.width = width
        self.length = length
        self.tunnelCategory = tunnel_category
        self.axleCount = axle_count
        self.type = truck_type
        self.trailerCount = trailer_count


class PlaceOptions:
    """A class to define ``PlaceOptions`` for ``origin``/ ``via``/ ``destination``.

    Various options can be found here:

    `PlaceOptions <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>`_.
    """  # noqa E501

    def __init__(
        self,
        course: Optional[int] = None,
        sideof_street_hint: Optional[List[float]] = None,
        match_sideof_street: Optional[str] = None,
        namehint: Optional[str] = None,
        radius: Optional[int] = None,
        min_course_distance: Optional[int] = None,
    ):
        """Object Initializer.

        :param course: An int representing degrees clock-wise from north.
            Indicating the desired direction at the place. E.g. 90 indicating ``east``.
            This is defined in constant ``ROUTE_COURSE``.
        :param sideof_street_hint: A list of latitude and longitude.Indicating the side of the
            street that should be used.
        :param match_sideof_street: Specifies how the location set by ``sideof_street_hint`` should
            be handled. If this is set then sideof_street_hint should also be set. There are two
            valid values for match_sideof_street:

            ``always``:
            Always prefer the given side of street.

            ``onlyIfDivided``:
            Only prefer using side of street set by ``sideof_street_hint`` in case the street
            has dividers. This is the default behavior.

            These values are mainted as config in:
            :attr:`ROUTE_MATCH_SIDEOF_STREET <here_location_services.config.routing_config.ROUTE_MATCH_SIDEOF_STREET>`
        :param namehint: A string for the router to look for the place with the most similar name.
            This can e.g. include things like: North being used to differentiate between
            interstates I66 North and I66 South, Downtown Avenue being used to correctly
            select a residential street.
        :param radius: In meters Asks the router to consider all places within the given radius as
            potential candidates for route calculation. This can be either because it is not
            important which place is used, or because it is unknown. Radius more than 200 meters
            are not supported.
        :param min_course_distance: In meters Asks the routing service to try to find a route that
            avoids actions for the indicated distance. E.g. if the origin is determined by a moving
            vehicle, the user might not have time to react to early actions.
        """  # noqa E501
        self.course = course
        self.sideOfStreetHint: Optional[str] = None
        if sideof_street_hint is not None:
            self.sideOfStreetHint = ",".join([str(point) for point in sideof_street_hint])
        self.matchSideOfStreet = match_sideof_street
        self.namehint = namehint
        self.radius = radius
        self.minCourseDistance = min_course_distance

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class WayPointOptions:
    """A class to define ``PlaceOptions`` for ``via``/ ``destination``.

    Various options can be found here:

    `PlaceOptions <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>`_.
    """  # noqa E501

    def __init__(self, stop_duration: Optional[int] = None, pass_through: Optional[bool] = None):
        self.stopDuration = stop_duration
        self.passThrough = pass_through

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)
