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
