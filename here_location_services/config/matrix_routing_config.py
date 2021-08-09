# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to matrix Routing API."""
import json
from typing import Dict, List

from .base_config import Bunch


class CircleRegion:
    """A class to define attributes of Circle Region for Matrix Routing API."""

    def __init__(self, center: Dict, radius: int):
        self.type = "circle"
        self.center = center
        self.radius = radius

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class BoundingBoxRegion:
    """A class to define attributes of BoundingBox Region for Matrix Routing API."""

    def __init__(self, north: float, south: float, west: float, east: float):
        self.type = "boundingBox"
        self.north = north
        self.south = south
        self.west = west
        self.east = east

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class PolygonRegion:
    """A class to define attributes of Polygon Region for Matrix Routing API."""

    def __init__(self, outer: List):
        self.type = "polygon"
        self.outer = outer

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class AutoCircleRegion:
    """A class to define attributes of AutoCircle Region for Matrix Routing API."""

    def __init__(self, margin: int = 10000):
        self.type = "autoCircle"
        self.margin = margin

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)


class WorldRegion:
    """A class to define attributes of World Region for Matrix Routing API."""

    def __init__(self):
        self.type = "world"


class Profile(Bunch):
    """A class to define constant values for ``Profile`` of Matrix Routing API.

    A profile ID enables the calculation of matrices with routes of arbitrary length.
    All profiles explicitly set departureTime to any and require that the obligatory request
    parameter REGION_DEFINITION_TYPE is set to world.

    .. csv-table:: Profiles
        :header: "Profile ID", "Description"
        :widths: 10, 30

        "carFast", "Car with fast routing mode"
        "carShort", "Car with short routing mode"
        "truckFast", "Truck with fast routing mode"
        "pedestrian", "Pedestrian transport mode"
        "bicycle", "Bicycle transport mode"
    """


#: Use this config for profile of matrix Routing API.
#: Example: for ``carFast`` profile  use ``PROFILE.carFast``.
PROFILE = Profile(
    **{
        "carFast": "carFast",
        "carShort": "carShort",
        "truckFast": "truckFast",
        "pedestrian": "pedestrian",
        "bicycle": "bicycle",
    }
)


class MatrixAttributes(Bunch):
    """A class to define constant values for ``matrixAttributes`` of Matrix Routing API.

    MatrixAttributes: ``travelTimes``, ``distances``.
    """


#: Use this config for matrix_attributes of matrix Routing API.
#: Example: for ``travelTimes`` matrix_attributes  use ``MATRIX_ATTRIBUTES.travelTimes``.
MATRIX_ATTRIBUTES = MatrixAttributes(**{"travelTimes": "travelTimes", "distances": "distances"})


class AvoidFeatures(Bunch):
    """A class to define constant values for features to avoid during matrix route calculation."""


#: Use this config for avoid_features of matrix Routing API.
#: Example: for ``tollRoad`` avoid_features  use ``AVOID_FEATURES.tollRoad``.
AVOID_FEATURES = AvoidFeatures(
    **{
        "tollRoad": "tollRoad",
        "controlledAccessHighway": "controlledAccessHighway",
        "ferry": "ferry",
        "tunnel": "tunnel",
        "dirtRoad": "dirtRoad",
    }
)


class AvoidBoundingBox:
    """A class to define attributes of Avoid areaBoundingBox for Matrix Routing API."""

    def __init__(self, north: float, south: float, west: float, east: float):
        self.type = "boundingBox"
        self.north = north
        self.south = south
        self.west = west
        self.east = east

    def __repr__(self):
        """Return string representation of this instance."""
        return json.dumps(self.__dict__)
