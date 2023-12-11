# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to Tour planning API."""
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .base_config import Bunch, Truck
import json
from json import JSONEncoder

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

class Area(object):
    """A class to define ``Territories``
    """

    def __init__(
        self,
        type: str,
        north: Optional[int],
        south: Optional[int],
        east: Optional[int],
        west: Optional[int]
    ):
        """Initializer.
        """
        self.type = str
        if north:
            self.north = north
        if south:
            self.south = south
        if east:
            self.east = east
        if west:
            self.west = west

class ZoneCategory(object):

    def __init__(
        self,
        categories: List[str],
        exceptZoneIds: Optional[str]
    ):
        """Initializer.
        """
        self.categories = categories
        if exceptZoneIds:
            self.exceptZoneIds = exceptZoneIds

class TourPlanningAvoidFeatures(object):
    """A class to define ``Territories``
    """

    def __init__(
        self,
        features: str,
        areas: Optional[List[Area]],
        segments: Optional[List[str]],
        truckRoadTypes: Optional[List[str]],
        zoneCategories: Optional[ZoneCategory]
    ):
        """Initializer.
        """
        self.features = features
        if areas:
            self.areas = areas
        if segments:
            self.segments = segments
        if truckRoadTypes:
            self.truckRoadTypes = truckRoadTypes
        if zoneCategories:
            self.zoneCategories = zoneCategories

class Teritory(object):
    """A class to define ``Territories``
    """

    def __init__(
        self,
        id: str,
        priority: Optional[int],
    ):
        """Initializer.
        """
        self.id = id
        if priority:
            self.priority = priority

class Teritories(object):
    """A class to define ``Territories``
    """

    def __init__(
        self,
        strict: Optional[bool],
        items: List[Teritory],
    ):
        """Initializer.
        """
        self.items = items
        if strict:
            self.strict = strict

class VehicleBreak(object):
    """A class to define ``VehicleBreak``
    """

    def __init__(
        self,
        times: List[str],
        duration: int,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        lat_SideOfStreetHint: Optional[float] = None,
        lng_SideOfStreetHint: Optional[float] = None,
        matchSideOfStreet_sideOfStreetHint: Optional[str] = None,
        nameHint: Optional[str] =None,        
    ):
        """Initializer.
        """
        self.times = times
        self.duration = duration
        if lat and lng:
            location ={}
            location['lat'] = lat
            location['lng'] = lng
            sideOfStreetHint = {}
            if lat_SideOfStreetHint and lng_SideOfStreetHint and matchSideOfStreet_sideOfStreetHint:
                sideOfStreetHint['lat'] = lat_SideOfStreetHint
                sideOfStreetHint['lng'] = lng_SideOfStreetHint
                sideOfStreetHint['matcheSideOfStreet'] = matchSideOfStreet_sideOfStreetHint
                location['sideOfStreetHint'] = sideOfStreetHint
            if nameHint:
                location['nameHint'] = nameHint
            self.location = location

class VehicleShift(object):
    """A class to define ``VehicleShift``
    """

    def __init__(
        self,
        start: Dict,
        end: Optional[Dict]=None,
        breaks: Optional[List[VehicleBreak]]=None,
        reloads: Optional[List[Dict]]=None,
        stopBaseDuration: Optional[Dict]=None,
    ):
        """Initializer.
        """
        self.start = start
        if end:
            self.end = end 
        if breaks:
            self.breaks = breaks 
        if reloads:
            self.reloads = reloads 
        if stopBaseDuration:
            self.stopBaseDuration = stopBaseDuration 

class VehicleType(object):
    """A class to define ``VehicleType``
    Type of vehicle in a fleet
    """

    def __init__(
        self,
        id: str,
        profile_name: str,
        capacity: List[int],
        shifts: List[VehicleShift],
        costs_fixed: float = 0,
        costs_distance: float = 0,
        costs_time: float = 0,
        amount: Optional[int] = None,
        skills: Optional[List[str]] = None,
        territories: Optional[dict] = None,
        vehicleIds: Optional[List[str]] = None,
        limits: Optional[Dict] = None,
        speedFactor: Optional[float] =0
    ):
        """Initializer.
        """
        self.id = id
        self.profile = profile_name
        self.capacity = capacity
        self.costs = {"fixed": costs_fixed, "distance": costs_distance, "time": costs_time}
        print(self.id)
        print(self.profile)
        print(self.capacity)
        print(self.costs)
        if amount:
            self.amount = amount
            print(self.amount)
        l_shifts = []
        for t in shifts:
            l_shifts.append(vars(t))
        self.shifts = l_shifts
        print(self.shifts)
        if skills:
            self.skills = skills
            print(self.skills)
        if limits:
            self.limits = limits
            print(self.limits)
        if territories:
            self.territories = territories
            print(self.territories)
        l_vehicleIds = []
        if vehicleIds:
            for v in vehicleIds:
                l_vehicleIds.append(v)
            self.vehicleIds = l_vehicleIds
            print(self.vehicleIds)
        if speedFactor:
            self.speedFactor = speedFactor

class Configuration(object):
    """A class to define ``Configuration``
    """
    def __init__(
        self,
        termination: Dict[any,any],
    ):
        """Initializer.
        """
        self.termination = termination

class Option(object):
    """A class to define ``Configuration``
    """
    def __init__(
        self,
        allowHighway: bool,
        speedCap: int
    ):
        """Initializer.
        """
        self.allowHighway = allowHighway
        self.speedCap = speedCap

class VehicleProfile(object):
    """A class to define ``VehicleProfile``
    """

    def __init__(
        self,
        name: str,
        type: str,
        departure_time: Optional[datetime] = None,
        avoid: Optional[TourPlanningAvoidFeatures] = None,
        options: Optional[Option] = None,
        exclude: Optional[Dict] = None,
        traffic: Optional[Dict] = None,
    ):
        self.name = name
        self.type = type
        if departure_time:
            self.departureTime = departure_time.isoformat()
        if avoid:
            self.avoid = avoid
        if options:
            self.options = options
        if exclude:
            self.exclude = exclude
        if traffic:
            self.traffic = traffic

class Fleet(object):
    """A class to define ``Fleet``
    A fleet represented by various vehicle types for serving jobs.
    """

    def __init__(self, vehicle_types: List[VehicleType], vehicle_profiles: List[VehicleProfile],traffic: Optional[str]=None):
        l_types = []
        for t in vehicle_types:
            l_types.append(vars(t))
        self.types = l_types

        l_profiles = []
        for pro in vehicle_profiles:
            l_profiles.append(vars(pro))
        self.profiles = l_profiles
        if traffic:
            self.traffic = traffic


class JobPlaces(object):
    def __init__(
        self,
        duration: int,
        lat: float,
        lng: float,
        lat_SideOfStreetHint: Optional[float] = None,
        lng_SideOfStreetHint: Optional[float] = None,
        matchSideOfStreet_sideOfStreetHint: Optional[str] = None,
        nameHint: Optional[str] =None,        
        tag: Optional[str] = None,
        territoryIds: Optional[List[str]] = None,
        times: Optional[List[List[str]]] = None,
    ):
        self.duration = duration
        location ={}
        location['lat'] = lat
        location['lng'] = lng
        sideOfStreetHint = {}
        if lat_SideOfStreetHint and lng_SideOfStreetHint and matchSideOfStreet_sideOfStreetHint:
            sideOfStreetHint['lat'] = lat_SideOfStreetHint
            sideOfStreetHint['lng'] = lng_SideOfStreetHint
            sideOfStreetHint['matcheSideOfStreet'] = matchSideOfStreet_sideOfStreetHint
            location['sideOfStreetHint'] = sideOfStreetHint
        if nameHint:
            location['nameHint'] = nameHint
        self.location = location
        if tag:
            self.tag = tag
        if times:
            self.times = times
        if territoryIds:
            self.territoryIds = territoryIds

class Cluster(object):
    def __init__(
        self,
        serviceTimeStrategy: Dict[str,int],
    ):
        self.serviceTimeStrategy = serviceTimeStrategy

class Task(object):
    def __init__(
        self,
        places: List[JobPlaces],
        demand: List[int],
        order: Optional[int]=None,
    ):
        l_places = []
        for t in places:
            l_places.append(vars(t))
        self.places = l_places
        l_demand = []
        for t in demand:
            l_demand.append(t)
        self.demand = l_demand
        if order:
            self.order = order

class Job(object):
    def __init__(
        self,
        id: str,
        pickups: Optional[List[Task]]=None,
        deliveries: Optional[List[Task]]=None,
        skills: Optional[List[str]]=None,
        priority: Optional[int] = None,
        customerId: Optional[str] =None,
    ):
        tasks = {}
        self.id = id
        if pickups:
            l_pickups = []
            for t in pickups:
                l_pickups.append(vars(t))
            tasks['pickups'] = l_pickups
        if deliveries:
            l_deliveries = []
            for t in deliveries:
                l_deliveries.append(vars(t))
            tasks['deliveries'] = l_deliveries
        self.tasks = tasks            
        if skills:
            self.skills = skills
        if priority:
            self.priority = priority
        if customerId:
            self.customerId = customerId
    

class Relation(object):
    def __init__(self, type: str, jobs: List, vehicle_id: str):
        self.type = type
        self.jobs = jobs
        self.vehicleId = vehicle_id

class Plan(object):
    def __init__(self, jobs: List[Job], relations: Optional[List[Relation]]=None, clustering: Optional[Cluster]=None):
        l_jobs = []
        for p in jobs:
            l_jobs.append(vars(p))
        self.jobs = l_jobs
        print(self.jobs)

        if relations:
            l_relations = []
            for r in relations:
                l_relations.append(vars(r))
            self.relations = l_relations
            print(self.relations)
        if clustering:        
            self.clustering=clustering

class Objectives(object):
    def __init__(self, type: List[str]):
        self.type = type

