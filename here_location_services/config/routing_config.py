# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to routing APIs."""

import json
from typing import Optional

from .base_config import Bunch, PlaceOptions, WayPointOptions


class RoutingReturn(Bunch):
    """A class to define constant attributes which are included in routing API's response
    as part of the data representation of route or section.

    * ``polyline`` - Polyline for the route in Flexible Polyline Encoding. Either a 2D polyline
      (without elevation specified) or a 3D polyline with the 3rd dimension type Elevation
      (with elevation specified).

    * ``actions`` - Actions (such as maneuvers or tasks) that must be taken to complete the
      section.

    * instructions - Include instructions in returned actions. Instructions are localized to the
      requested language.

    * ``summary`` - Include a summary for the section.

    * ``travelSummary`` - Include a summary for the travel portion of the section.

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
      must be requested as well.
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
#: Use this config for return attributes from routing API for param ``return_results``.
#: Example: To return polyline in results use ``ROUTING_RETURN.polyline``.
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

#: Use this config for spans of routing API.
#: Example: for ``walkAttributes`` routing_mode use ``ROUTING_SPANS.walkAttributes``.
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

#: Use this config for transport_mode of routing API.
#: Example: for ``car`` transport_mode use ``ROUTING_TRANSPORT_MODE.car``.
ROUTING_TRANSPORT_MODE = RoutingTransportMode(**transport_mode)


class RouteCourse(Bunch):
    """A class to define constant attributes for Course option."""


route_course = {"east": 90, "south": 180, "west": 270, "north": 360}

ROUTE_COURSE = RouteCourse(**route_course)


class RouteMatchSideOfStreet(Bunch):
    """A class to define constant attribuites for ``matchSideOfStreet``."""


match_sideof_street = {"always": "always", "onlyIfDivided": "onlyIfDivided"}

#: Use this config for transport_mode of routing API.
#: Example: for ``car`` transport_mode use ``ROUTING_TRANSPORT_MODE.car``.
ROUTE_MATCH_SIDEOF_STREET = RouteMatchSideOfStreet(**match_sideof_street)


class AvoidFeatures(Bunch):
    """A class to define constant values for features to avoid during route calculation."""


#: Use this config for match_sideof_street for PlaceOptions.
#: Example: for match_sideof_street ``always`` use ``ROUTE_MATCH_SIDEOF_STREET.always``.
AVOID_FEATURES = AvoidFeatures(
    **{
        "seasonalClosure": "seasonalClosure",
        "tollRoad": "tollRoad",
        "controlledAccessHighway": "controlledAccessHighway",
        "ferry": "ferry",
        "carShuttleTrain": "carShuttleTrain",
        "tunnel": "tunnel",
        "dirtRoad": "dirtRoad",
        "difficultTurns": "difficultTurns",
    }
)


class Scooter:
    """A class to define attributes specific for the scooter route.

    Scooter specific parameters:

    allowHighway: Specifies whether the scooter is allowed on the highway or not.
    This parameter is optional. If not provided, then by default scooter is not allowed to use
    highway. There is a similar parameter ``avoid[features]=controlledAccessHighway`` to disallow
    highway usage. avoid[features] takes precedence so if this parameter is also used then
    scooters are not allowed to use highways even if allowHighway is used with value as true.
    Possible values:
    true: scooter is allowed to use the highway.
    false: scooter is not allowed to use the highway.
    """

    def __init__(self, allow_highway: bool):
        self.allowHighway = allow_highway

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class Via:
    """A class to define ``via`` waypoint.

    A via waypoint is a location between origin and destination. The route will do a stop at the
    via waypoint.
    """

    def __init__(
        self,
        lat: float,
        lng: float,
        place_options: Optional[PlaceOptions] = None,
        waypoint_options: Optional[WayPointOptions] = None,
    ):
        self.lat = lat
        self.lng = lng
        self.place_options = place_options
        self.waypoint_options = waypoint_options
