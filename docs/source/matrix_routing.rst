Matrix Routing
==============
`Matrix Routing API  v8 <https://developer.here.com/documentation/matrix-routing-api/8.3.0/dev_guide/index.html>`_ is used to calculate routing matrices of up to 10,000 origins and 10,000 destinations.
A routing matrix is a matrix with rows labeled by origins and columns by destinations. Each entry of the matrix is travel time or distance from the origin to the destination.

The Matrix Routing service provides the following features:

- A large number of origins and destinations (up to 10,000)
- Live traffic and historical speed patterns
- Car, Truck, Pedestrian and Bicycle modes
- Truck attributes such as dimensions, weight, tunnel restrictions, and more
- Avoiding areas and routing features, e.g., toll roads, ferries, and motorways.
- The choice between synchronous and asynchronous APIs for flexible result downloads

Calculation of routing matrices in one of the following modes:

- Flexible
- Region
- Profile

The values of the ``region_definition`` and ``profile`` parameters determine which mode is used.
The following table describes the capabilities and limitations of each mode.

.. csv-table:: Modes
    :header: "Mode", "region_definition parameter", "profile parameter provided?", "Custom Options & Time Awareness (incl. live traffic)", "Unlimited region"
    :widths: 30, 30, 30, 30, 30

        "Flexible", "world", "no", "yes", "yes"
        "Region", "one of: Circle, boundingBox, polygon, autoCircle", "no", "yes", "no, origins and destinations must be within a region of max 400 km diameter"
        "Profile", "world", "yes", "no", "yes"

Note that the combination of specifying a profile along with a region_definition not equal to world is not allowed.

.. toctree::
  :maxdepth: 1
  :caption: Routing

  Flexible mode <flexible_mode>
  Region mode <region_mode>
  Profile mode <profile_mode>