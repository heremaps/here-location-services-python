# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to Isoline routing API."""

from .base_config import Bunch


class IsolineRoutingTransportMode(Bunch):
    """A class to define constant attributes for mode of transport to be used for the
    calculation of the route.

    * ``car``
    * ``truck``
    * ``pedestrian``
    """


transport_mode = {
    "car": "car",
    "truck": "truck",
    "pedestrian": "pedestrian",
}

#: Use this config for transport_mode of isoline routing API.
#: Example: for ``car`` transport_mode use ``ISOLINE_ROUTING_TRANSPORT_MODE.car``.
ISOLINE_ROUTING_TRANSPORT_MODE = IsolineRoutingTransportMode(**transport_mode)


class RangeType(Bunch):
    """A Class to define constant values for specifying the type of range for Isoline Routing API

    ``distance``:
    Units in meters

    ``time``:
    Units in seconds

    ``consumption``:
    Units in Wh
    """


#: Use this config s optimised_for of isoline routing API.
#: Example: for optimising for ``balanced`` mode use ``OPTIMISED_FOR.balanced``.
RANGE_TYPE = RangeType(**{"distance": "distance", "time": "time", "consumption": "consumption"})


class OptimisedFor(Bunch):
    """A Class to define constant values for optimising calculation for Isoline Routing API

    ``quality``:
    Calculation of isoline focuses on quality, that is, the graph used for isoline calculation
    has higher granularity generating an isoline that is more precise.

    ``performance``:
    Calculation of isoline is performance-centric, quality of isoline is reduced to provide
    better performance.

    ``balanced``:
    Calculation of isoline takes a balanced approach averaging between quality and performance.
    """


#: Use this config s optimised_for of isoline routing API.
#: Example: for optimising for ``balanced`` mode use ``OPTIMISED_FOR.balanced``.
OPTIMISED_FOR = OptimisedFor(
    **{"quality": "quality", "performance": "performance", "balanced": "balanced"}
)


class IsolineRoutingAvoidFeatures(Bunch):
    """A class to define values for features to avoid features during isoline calculation."""


#: Use this config for avoid_features of isoline API.
#: Example: for ``tollRoad`` avoid_features  use ``ISOLINE_ROUTING_AVOID_FEATURES.tollRoad``.
ISOLINE_ROUTING_AVOID_FEATURES = IsolineRoutingAvoidFeatures(
    **{
        "tollRoad": "tollRoad",
        "controlledAccessHighway": "controlledAccessHighway",
        "ferry": "ferry",
        "carShuttleTrain": "carShuttleTrain",
        "tunnel": "tunnel",
        "dirtRoad": "dirtRoad",
        "difficultTurns": "difficultTurns",
    }
)
