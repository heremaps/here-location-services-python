# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to Tour planning API."""
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from here_location_services.config.isoline_routing_config import IsolineRoutingAvoidFeatures

from .base_config import Bunch, Truck


class TourPlanningAvoidFeatures(Bunch):
    """A class to define values for features to avoid features during tour planning calculation."""


#: Use this config for avoid of Tour planning API.
#: Example: for ``tollRoad`` avoids  use ``TOUR_PLANNING_AVOID_FEATURES.tollRoad``.
TOUR_PLANNING_AVOID_FEATURES = TourPlanningAvoidFeatures(
    **{
        "tollRoad": "tollRoad",
        "motorway": "motorway",
        "ferry": "ferry",
        "tunnel": "tunnel",
        "dirtRoad": "dirtRoad",
    }
)


class VehicleMode(Bunch):
    """A class to define values vehicle mode in vehicle profile."""


#: Use this config for vehicle_mode of Tour planning API.
#: Example: for ``scooter`` avoids  use ``VEHICLE_MODE.scooter``.
VEHICLE_MODE = VehicleMode(
    **{
        "scooter": "scooter",
        "bicycle": "bicycle",
        "pedestrian": "pedestrian",
        "car": "car",
        "truck": "truck",
    }
)


class VehicleType(object):
    """A class to define ``VehicleType``

    Type of vehicle in a fleet
    """

    def __init__(
        self,
        id: str,
        profile_name: str,
        amount: int,
        capacity: List[int],
        shift_start: Dict,
        shift_end: Optional[Dict] = None,
        shift_breaks: Optional[List] = None,
        costs_fixed: Optional[float] = 0,
        costs_distance: Optional[float] = 0,
        costs_time: Optional[float] = 0,
        skills: Optional[List[str]] = None,
        limits: Optional[Dict] = None,
    ):
        """
        :param id: Specifies id of the vehicle type. Avoid assigning real-life identifiers,
          such as vehicle license plate as the id of a vehicle
        :param profile_name: characters ^[a-zA-Z0-9_-]+$ Specifies the name of the profile.
          Avoid assigning real-life identifiers, such as a vehicle license plate Id or
          personal name as the profileName of the routing profile.
        :param amount: Amount of vehicles available.
        :param capacity: Unit of measure, e.g. volume, mass, size, etc.
        :param shift_start: Represents a depot: a place where a vehicle starts
        :param costs_fixed: A fixed cost to start using vehicle of this type. It is
          optional with a default value of zero
        :param shift_end: Represents a depot: a place where a vehicle ends
        :param shift_breaks: Represents a depot: a place where a vehicle takes breaks
        :param costs_distance: A cost per meter. It is optional with a default value of zero.
        :param costs_time: A cost per second. It is optional with a default value of zero.
          In case time and distance costs are zero then a small time cost 0.00000000001
          will be used instead
        :param skills: A list of skills for a vehicle or a job.
        :param limits: Contains constraints applied to a vehicle type.

        """
        self.id = id
        self.profile = profile_name
        self.amount = amount
        self.capacity = capacity
        self.costs = {"fixed": costs_fixed, "distance": costs_distance, "time": costs_time}
        shifts: Dict[Any, Any] = {"start": shift_start}
        if shift_end:
            shifts["end"] = shift_end
        if shift_breaks:
            l_breaks = []
            for b in shift_breaks:
                l_breaks.append(b)
            shifts["breaks"] = l_breaks
        self.shifts = [shifts]
        self.skills = skills
        self.limits = limits


class VehicleProfile(object):
    """A class to define ``VehicleProfile``

    Profile of vehicle in a fleet

    :param name: Specifies the name of the profile. Avoid assigning real-life identifiers,
            such as a vehicle license plate Id or personal name as the profileName of
            the routing profile.
    :param vehicle_mode: Contains constraints applied to a vehicle type.
    :param departure_time: Represents time of departure.
    :param avoid: Avoid routes that violate these properties.
    :param truck_options: Specifies truck profile options.
    :param allow_highway_for_scooter: Specifies whether routing calculation should take
        highways into account. When this parameter isn't provided, then by default
        highways would be avoided. If the avoid feature motorway is provided, then
        highways would be avoided, even if this is set to true.
    :raises ValueError: If ``truck_options`` are provided without setting `vehicle_mode` to
        ``VEHICLE_MODE.truck``
    :raises ValueError: If ``allow_highway_for_scooter`` is provided without setting
        `vehicle_mode` to ``VEHICLE_MODE.scooter``
    """

    def __init__(
        self,
        name: str,
        vehicle_mode: str,
        departure_time: Optional[datetime] = None,
        avoid: Optional[List[IsolineRoutingAvoidFeatures]] = None,
        truck_options: Optional[Truck] = None,
        allow_highway_for_scooter: Optional[bool] = None,
    ):
        if vehicle_mode != "truck" and truck_options:
            raise ValueError(
                "`truck_options` can only be provided when `vehicle_mode` is `VEHICLE_MODE.truck`"
            )
        if vehicle_mode != "scooter" and allow_highway_for_scooter:
            raise ValueError(
                "`allow_highway_for_scooter` can only be provided when "
                + "`vehicle_mode` is `VEHICLE_MODE.scooter`"
            )
        self.name = name
        self.type = vehicle_mode
        if departure_time:
            self.departureTime = departure_time.isoformat()
        if avoid:
            self.avoid = {"features": avoid}
        if truck_options:
            self.options = vars(truck_options)
        if allow_highway_for_scooter:
            self.options = {"allowHighway": allow_highway_for_scooter}


class Fleet(object):
    """A class to define ``Fleet``

    A fleet represented by various vehicle types for serving jobs.

    :param vehicle_types: A list of vehicle types. The upper limit for the number of vehicle
        types is 35 for the synchronous problems endpoint and 150 for the asynchronous
        problems endpoint.
    :param vehicle_profiles: Specifies the profile of the vehicle.

    """

    def __init__(self, vehicle_types: List[VehicleType], vehicle_profiles: List):
        l_types = []
        for t in vehicle_types:
            l_types.append(vars(t))
        self.types = l_types

        l_profiles = []
        for pro in vehicle_profiles:
            l_profiles.append(vars(pro))
        self.profiles = l_profiles


class JobPlaces(object):
    """A class to define ``JobPlaces``

    :param duration: Represents duration in seconds.
    :param demand: Unit of measure, e.g. volume, mass, size, etc.
    :param location: Represents geospatial location defined by latitude and longitude.
    :param tag: A free text associated with the job place. Avoid referencing any confidential
        or personal information as part of the JobTag.
    :param times: Represents multiple time windows.

    """

    def __init__(
        self,
        duration: int,
        demand: List[int],
        location: Tuple,
        tag: Optional[str] = None,
        times: Optional[List[List[str]]] = None,
    ):
        self.duration = duration
        self.demand = demand
        self.location = {"lat": location[0], "lng": location[1]}
        if tag:
            self.tag = tag
        if times:
            self.times = times


class Job(object):
    """A class to define ``Job``

    A fleet represented by various vehicle types for serving jobs.

    :param id: Specifies id of the job. Avoid referencing any sensitive or personal information,
        such as names, addresses, information about a delivery or service, as part of the jobId.
    :param skills: A list of skills for a vehicle or a job.
    :param priority: Specifies the priority of the job with 1 for high priority jobs and
        2 for normal jobs.
    :param pickups: Places where sub jobs to be performed. All pickups are done before any
        other delivery.
    :param deliveries: Places where sub jobs to be performed. All pickups are done before any
        other delivery.
    :raises ValueError: If no subjob is speficified either as pickup or delivery.

    """

    def __init__(
        self,
        id: str,
        skills: Optional[List] = None,
        priority: Optional[int] = None,
        pickups: Optional[List[JobPlaces]] = None,
        deliveries: Optional[List[JobPlaces]] = None,
    ):
        if pickups is None and deliveries is None:
            raise ValueError("Atleast one subjob must be specified as pickup or delivery")
        self.id = id
        if skills:
            self.skills = skills
        if priority:
            self.priority = priority
        self.places = {}
        if pickups:
            l_pickups = []
            for p in pickups:
                l_pickups.append(vars(p))
            self.places["pickups"] = l_pickups
        if deliveries:
            l_deliveries = []
            for d in deliveries:
                l_deliveries.append(vars(d))
            self.places["deliveries"] = l_deliveries


class Relation(object):
    """A class to define ``Relation``

    Represents a list of preferred relations between jobs, vehicles.

    :param type: "sequence" "tour" "flexible"
        Defines a relation between jobs and a specific vehicle
    :param jobs: Ids of jobs or reserved activities. There are three reserved activity ids:
        - departure: specifies departure activity. Should be first in the list.
        - break: specifies vehicle break activity
        - arrival: specifies arrival activity. Should be last in the list.
    :param vehicle_id: A unique identifier of an entity. Avoid referencing any confidential or
        personal information as part of the Id.

    """

    def __init__(self, type: str, jobs: List, vehicle_id: str):
        self.type = type
        self.jobs = jobs
        self.vehicleId = vehicle_id


class Plan(object):
    """A class to define ``Plan``

    Represents the list of jobs to be served.
    """

    def __init__(self, jobs: List[Job], relations: Optional[List[Relation]]):
        l_jobs = []
        for p in jobs:
            l_jobs.append(vars(p))
            self.jobs = l_jobs

        if relations:
            l_relations = []
            for r in relations:
                l_relations.append(vars(r))
                self.relations = l_relations
