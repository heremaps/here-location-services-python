Tour Planning
===============
`Tour Planning API  <https://developer.here.com/documentation/tour-planning/2.3.0/dev_guide/index.html>`_ 
The HERE Tour Planning API allows you to dynamically optimize routes for multiple vehicles visiting a set of locations given real-life constraints, such as limited capacity in a vehicle or delivery time windows.

The HERE Tour Planning API supports the following use cases:

- Capacitated vehicle routing problem: You can use Tour Planning API to take your vehicle capacity into account when routing your vehicles.
- Vehicle routing problem with time windows: With Tour Planning API, you can schedule your vehicles to visit depots only when they are available.
- Multi-depot vehicle routing problem: In a simple vehicle routing problem, all vehicles start from the same location. In the multi-depot vehicle routing problem, vehicles start from multiple depots and return to their depots of origin at the end of their assigned tours.
- Open vehicle routing problem: Do you work with drivers who have their vehicles and do not return to a planned location after their drop-offs? With Tour Planning API, you can schedule open vehicle routing where your drivers can return to their homes after work.
- Heterogeneous or mixed fleet VRP: Tour Planning API supports routing multiple types of vehicles with different gas mileage, cost of driving, capacity, and more. For example, your fleet can include passenger vehicles and even specialized trucks with fridges in one route.
- Pick up and delivery vehicle routing problem: With Tour Planning API, you can schedule a vehicle to pick up and deliver an item in one route.
- Vehicle routing problem with priorities: Do you have jobs that must be served, such as today, and others that could also be delayed until, such as until tomorrow, and ideally you would like to prevent those priority jobs from being skipped in cases where fleet capacity or shift durations do not allow to serve all jobs, but at the same time you would like to serve as many non-priority jobs as possible? With Tour Planning API, you can define jobs to be with high priority internally the algorithms will try to avoid skipping those high priority jobs and will skip low priority jobs first in scenarios where it is impossible to serve all jobs due to constraints. The priority of a job does not imply its order in the route, as in the position of a high priority job might be anywhere in the route and not necessarily before lower priority jobs.


Example
-------

.. jupyter-execute::

    import os

    from here_location_services import LS
    from here_location_services.config.tour_planning_config import (
        VEHICLE_MODE,
        Fleet,
        Job,
        JobPlaces,
        Plan,
        Relation,
        VehicleProfile,
        VehicleType,
    )
    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    
    fleet = Fleet(
        vehicle_types=[
            VehicleType(
                id="09c77738-1dba-42f1-b00e-eb63da7147d6",
                profile_name="normal_car",
                costs_fixed=22,
                costs_distance=0.0001,
                costs_time=0.0048,
                capacity=[100, 5],
                skills=["fridge"],
                amount=1,
                shift_start={
                    "time": "2020-07-04T09:00:00Z",
                    "location": {"lat": 52.5256, "lng": 13.4542},
                },
                limits={"maxDistance": 20000, "shiftTime": 21600},
                shift_end={
                    "location": {"lat": 52.5256, "lng": 13.4542},
                    "time": "2020-07-04T18:00:00Z",
                },
                shift_breaks=[
                    {
                        "duration": 1800,
                        "times": [["2020-07-04T11:00:00Z", "2020-07-04T13:00:00Z"]],
                    }
                ],
            )
        ],
        vehicle_profiles=[VehicleProfile(name="normal_car", vehicle_mode=VEHICLE_MODE.car)],
    )

    plan = Plan(
        jobs=[
            Job(
                id="4bbc206d-1583-4266-bac9-d1580f412ac0",
                pickups=[
                    JobPlaces(
                        duration=180,
                        demand=[10],
                        location=(52.53088, 13.38471),
                        times=[["2020-07-04T10:00:00Z", "2020-07-04T12:00:00Z"]],
                    )
                ],
                deliveries=[
                    JobPlaces(
                        duration=300,
                        demand=[10],
                        location=(52.53088, 13.38471),
                        times=[["2020-07-04T14:00:00Z", "2020-07-04T16:00:00Z"]],
                    )
                ],
                skills=["fridge"],
                priority=2,
            )
        ],
        relations=[
            Relation(
                type="sequence",
                jobs=["departure", "4bbc206d-1583-4266-bac9-d1580f412ac0", "arrival"],
                vehicle_id="09c77738-1dba-42f1-b00e-eb63da7147d6_1",
            )
        ],
    )

    # Synchronous Solving
    response = ls.solve_tour_planning(
        fleet=fleet, plan=plan, id="7f3423c2-784a-4983-b472-e14107d5a54a"
    )
    print(response)

    # Asynchronous Solving
    async_response = ls.solve_tour_planning(
        fleet=fleet, 
        plan=plan, 
        id="7f3423c2-784a-4983-b472-e14107d5a54a",
        is_async=True
    )
    print(async_response)

Attributes
----------

===========================   =======================================================================================    ===
Attribute                     Type                                                                                       Doc
===========================   =======================================================================================    ===
fleet                         :class:`Fleet <here_location_services.config.tour_planning_config.Fleet>`                  A fleet represented by various vehicle types for serving jobs.
plan                          :class:`Plan <here_location_services.config.tour_planning_config.Plan>`                    Represents the list of jobs to be served.
id                            string                                                                                     optional A unique identifier of an entity. Avoid referencing any confidential or personal information as part of the Id.
optimization_traffic          string                                                                                     optional "liveOrHistorical" "historicalOnly" "automatic" Specifies what kind of traffic information should be considered for routing
optimization_waiting_time     Dict                                                                                       optional Configures departure time optimization which tries to adapt the starting time of the tour in order to reduce waiting time as a consequence of a vehicle arriving at a stop before the starting time of the time window defined for serving the job.
is_async                      bool                                                                                       optional Solves the problem Asynchronously
===========================   =======================================================================================    ===