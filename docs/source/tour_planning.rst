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
