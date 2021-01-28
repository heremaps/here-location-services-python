# Copyright (C) 2019-2020 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""This module defines all the constants which will be required as inputs to various APIs."""

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


ROUTING_MODE = RoutingMode(**{"fast": "fast", "short": "short"})


class RoutingReturn(Bunch):
    """A class to define constant attributes which are included in routing API's response
    as part of data representation of route or section.

    * ``polyline`` - Polyline for the route in Flexible Polyline Encoding. Either a 2D polyline
      (without elevation specified), or a 3D polyline with the 3rd dimension type Elevation
      (with elevation specified).

    * ``actions`` - Actions (such as maneuvers or tasks) that must be taken to complete the
      section.

    * instructions - Include instructions in returned actions. Instructions are localized to the
      requested language.

    * ``summary`` - Include summary for the section.

    * ``travelSummary`` - Include summary for the travel portion of the section.

    * ``turnByTurnActions`` - Include all information necessary to support turn by turn guidance
      to complete the section.

    * ``mlDuration`` - Use a region-specific machine learning model to calculate route duration.
      Disclaimer: This parameter is currently in beta release, and is therefore subject
      to breaking changes.

    * ``elevation`` - Include elevation information in coordinate and geometry types.
      See e.g. polyline or location.

    * ``routeHandle`` - Encode calculated route and return a handle which can be used with
      routes/{routeHandle} to decode the route at a later point in time.

    * ``incidents`` - Include a list of all incidents applicable to each section.

    Following restrictions apply when specifying return parameter:

    * If ``actions`` is requested, then ``polyline`` must also be requested as well.

    * If ``instructions`` is requested, then ``actions`` must also be requested as well.

    * If ``turnByTurnActions`` is requested, then ``polyline`` must also be requested as well.

    * If at least one attribute is requested within the ``spans`` parameter, then ``polyline``
      must be request as well.
    """


return_attributes = {
    "polyline": "polyline",
    "actions": "actions",
    "instructions": "instructions",
    "summary": "summary",
    "travelSummary": "travelSummary",
    "mlDuration": "mlDuration",
    "turnByTurnActions": "turnByTurnActions",
    "elevation": "elevation",
    "routeHandle": "routeHandle",
    "passthrough": "passthrough",
    "incidents": "incidents",
}
ROUTING_RETURN = RoutingReturn(**return_attributes)


class RoutingSpans(Bunch):
    """A class to define constant attributes which are included in the response spans.

    ``walkAttributes`` ``streetAttributes`` ``carAttributes`` ``truckAttributes``
    ``scooterAttributes`` ``names`` ``length`` ``duration`` ``baseDuration`` ``countryCode``
    ``functionalClass`` ``routeNumbers`` ``speedLimit`` ``maxSpeed`` ``dynamicSpeedInfo``
    ``segmentId`` ``segmentRef`` ``consumption``.
    """


routing_spans = {
    "walkAttributes": "walkAttributes",
    "streetAttributes": "streetAttributes",
    "carAttributes": "streetAttributes",
    "truckAttributes": "truckAttributes",
    "scooterAttributes": "scooterAttributes",
    "names": "names",
    "length": "length",
    "duration": "duration",
    "baseDuration": "baseDuration",
    "countryCode": "countryCode",
    "functionalClass": "functionalClass",
    "routeNumbers": "routeNumbers",
    "speedLimit": "speedLimit",
    "maxSpeed": "maxSpeed",
    "dynamicSpeedInfo": "dynamicSpeedInfo",
    "segmentId": "segmentId",
    "segmentRef": "segmentRef",
    "consumption": "consumption",
}

ROUTING_SPANS = RoutingSpans(**routing_spans)


class RoutingTransportMode(Bunch):
    """A class to define constant attributes for mode of transport to be used for the
    calculation of the route.

    * ``car``
    * ``truck``
    * ``pedestrian``
    * ``bicycle``
    * ``scooter``
    """


transport_mode = {
    "car": "car",
    "truck": "truck",
    "pedestrian": "pedestrian",
    "bicycle": "bicycle",
    "scooter": "scooter",
}

ROUTING_TRANSPORT_MODE = RoutingTransportMode(**transport_mode)


class RouteCourse(Bunch):
    """A class to define constant attributes for Course option."""


route_course = {"east": 90, "south": 180, "west": 270, "north": 360}

ROUTE_COURSE = RouteCourse(**route_course)


class RouteMatchSideOfStreet(Bunch):
    """A class to define constant attribuites for ``matchSideOfStreet``."""


match_sideof_street = {"always": "always", "onlyIfDivided": "onlyIfDivided"}

ROUTE_MATCH_SIDEOF_STREET = RouteMatchSideOfStreet(**match_sideof_street)


class PlaceOptions:
    """A class to define ``PlaceOptions`` for ``origin``/ ``via``/ ``destination``.

    Various options can be found here:
    `PlaceOptions <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>_`.  # noqa E501
    """

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
            Indicating desired direction at the place. E.g. 90 indicating ``east``.
            This is defined in constant ``ROUTE_COURSE``.
        :param sideof_street_hint: A list of latitude and longitude.Indicating the side of the
            street that should be used.
        :param match_sideof_street:
        :param namehint: A string for the router to look for the place with the most similar name.
            This can e.g. include things like: North being used to differentiate between
            interstates I66 North and I66 South, Downtown Avenue being used to correctly
            select a residental street.
        :param radius: In meters Asks the router to consider all places within the given radius as
            potential candidates for route calculation. This can be either because it is not
            important which place is used, or because it is unknown. Radius more than 200 meter
            are not supported.
        :param min_course_distance: In meters Asks the routing service to try find a route that
            avoids actions for the indicated distance. E.g. if the origin is determined by a moving
            vehicle, the user might not have time to react to early actions.
        """
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
    `PlaceOptions <https://developer.here.com/documentation/routing-api/8.16.0/api-reference-swagger.html>_`.  # noqa E501
    """

    def __init__(self, stop_duration: Optional[int] = None, pass_through: Optional[bool] = None):
        self.stopDuration = stop_duration
        self.passThrough = pass_through

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class Scooter:
    """A class to define attributes specific for scooter route.

    Scooter specific parameters.
    allowHighway: Specifies whether scooter is allowed on highway or not.
    This parameter is optional. If not provided, then by default scooter is not allowed to use
    highway. There is a similar parameter avoid[features]=controlledAccessHighway to disallow
    highway usage. avoid[features] takes precedence so if this parameter is also used then
    scooters are not allowed to use highways even if allowHighway is used with value as true.
    Possible values:
    true: scooter is allowed to use highway.
    false: scooter is not allowed to use highway.
    """

    def __init__(self, allow_highway: bool):
        self.allowHighway = allow_highway

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)
