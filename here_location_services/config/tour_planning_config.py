# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to Tour planning API."""
from datetime import datetime
import json

from typing import Dict, List, Optional, Tuple

from here_location_services.config.isoline_routing_config import IsolineRoutingAvoidFeatures

from .base_config import Bunch


class VehicleType(object):
    """A class to define ``VehicleType``

    Type of vehicle in a fleet
    """

    def __init__(
        self,
        id: str,
        profile: str,
        amount: int,
        capacity: List[int],
        shift_start: Dict,
        costs_fixed: Optional[float] = 0,
        costs_distance: Optional[float] = 0,
        costs_time: Optional[float] = 0,
        shift_end: Optional[Dict] = None,
        shift_breaks: Optional[List] = None,
        skills: Optional[List[str]] = None,
        limits: Optional[Dict] = None,
    ):
        self.id = id
        self.profile = profile
        self.amount = amount
        self.capacity = capacity
        self.costs = {"fixed": costs_fixed, "distance": costs_distance, "time": costs_time}
        shifts = {"start": shift_start}
        if shift_end:
            shifts["end"] = shift_end
        if shift_breaks:
            shifts["breaks"] = shift_breaks
        self.shifts = [shifts]
        self.skills = skills
        self.limits = limits


class VehicleProfile(object):
    """A class to define ``VehicleProfile``

    Profile of vehicle in a fleet
    """

    def __init__(
        self,
        name: str,
        vehicle_mode: str,
        departure_time: Optional[datetime] = None,
        avoid: Optional[List[IsolineRoutingAvoidFeatures]] = None,
    ):
        self.name = name
        # self.departureTime = departure_time
        # self.avoid["features"] = avoid
        self.type = vehicle_mode


class Fleet(object):
    """A class to define ``Fleet``

    A fleet represented by various vehicle types for serving jobs.
    """

    def __init__(self, vehicle_types: List[VehicleType],
                 vehicle_profiles: List
                 ):
        l_types = []
        for t in vehicle_types:
            l_types.append(vars(t))
        l_profiles = []
        for l in vehicle_profiles:
            l_profiles.append(vars(l))
        self.types = l_types
        self.profiles = l_profiles
