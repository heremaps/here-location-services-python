# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to matrix Routing API."""
import json
from typing import Dict, List, Optional

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
    Truck options should be used when transportMode is ``truck``.
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
