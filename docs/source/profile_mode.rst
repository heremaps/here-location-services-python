Profile Mode
============
Profile mode supports:

- unlimited region
-  Matrix Sizes up to 10,000 x 10,000

Profile mode does not support:

- Custom Options
- Time Awareness (including Live Traffic)

This section refers to calculating matrices with routes of arbitrary length, using one of the supported profiles. If you want to define custom options, see ``Flexible Mode``.

The special variant ``world`` needs to be set as region definition. No additional request options or departure_time can be provided except for matrix_attributes.
Below is an example of a 7 x 7 matrix request with these origins and destinations:

- Berlin at (52.54, 13.40)
- Kyiv at (50.43, 30.52)
- London at (51.50, -0.08)
- Madrid at (40.40, -3.68)
- Moscow at (55.75, 37.60)
- Paris at (48.87, 2.33)
- Rome at (41.90, 12.48)

To calculate a car distance matrix, you can use the code below.
Since the request does not specify the destinations array, the origins are taken as destinations and the resulting matrix is a 7 x 7 matrix.
The region definition is the special variant world. In the request, we use the profile carFast which uses transport mode car and optimizes the route calculations for travel time.
By default, the service calculates a travel times matrix, but since we want to get distances in the response instead of times, the request specifies the matrix_attributes property with the value distances.

Example
-------

.. code-block:: python

    from here_location_services import LS
    from here_location_services.config.matrix_routing_config import (
        BoundingBoxRegion,
        AutoCircleRegion,
        MATRIX_ATTRIBUTES,
        PROFILE,
        WorldRegion
    )

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)  # Create Location Services object using API KEY.

    origins = [
        {"lat": 52.54, "lng": 13.40},
        {"lat": 50.43, "lng": 30.52},
        {"lat": 51.50, "lng": -0.08},
        {"lat": 40.40, "lng": -3.68},
        {"lat": 55.75, "lng": 37.60},
        {"lat": 48.87, "lng": 2.33},
        {"lat": 41.90, "lng": 12.48},
    ]

    profile = PROFILE.carFast
    region_definition = WorldRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances]

    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        matrix_attributes=matrix_attributes,
        async_req=True
    )
    result.to_distnaces_matrix()

Attributes
----------

.. csv-table:: Attributes
    :header: "Attribute", "Type", "Doc"
    :widths: 30, 30, 30

        "origins", "list", "A list of dictionaries containing lat and long for origin points."
        "region_definition", "object", "use one of the:
                                        :class:`CircleRegion <here_location_services.config.matrix_routing_config.CircleRegion>`

                                        :class:`BoundingBoxRegion <here_location_services.config.matrix_routing_config.BoundingBoxRegion>`

                                        :class:`PolygonRegion <here_location_services.config.matrix_routing_config.PolygonRegion>`

                                        :class:`AutoCircleRegion <here_location_services.config.matrix_routing_config.AutoCircleRegion>`

                                        :class:`WorldRegion <here_location_services.config.matrix_routing_config.WorldRegion>`"
        "async_req", "bool", "If set to True reuqests will be sent to asynchronous matrix routing API else It will be sent to synchronous matrix routing API. For larger matrices, or longer routes, or routes in denser road networks, it is recommended to set to True."
        "destinations", "list", "A list of dictionaries containing lat and long for destination points. When no destinations are specified the matrix is assumed to be quadratic with origins used as destinations."
        "profile", "string", "Use values from config: :attr:`PROFILE <here_location_services.config.matrix_routing_config.PROFILE>`"
        "departure_time", ":class:`datetime.datetime` object with timezone", "When it is not specified, it is implicitly assumed to be the current time. The special value ``any`` enforces non time-aware routing."
        "routing_mode", "string", "Use values from config: :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`"
        "transport_mode", "string", "Use values from config: :attr:`ROUTING_TRANSPORT_MODE <here_location_services.config.routing_config.ROUTING_TRANSPORT_MODE>`"
        "avoid_features", "list", "Use values from config: :attr:`AVOID_FEATURES <here_location_services.config.matrix_routing_config.AVOID_FEATURES>`"
        "avoid_areas", "list", "Use object of :class:`AvoidBoundingBox <here_location_services.config.matrix_routing_config.AvoidBoundingBox>` to define avoid areas."
        "truck", "object of :class:`Truck <here_location_services.config.matrix_routing_config.Truck>`", "Used to define truck options when transport mode is truck"
        "matrix_attributes", "list", "Use values from config: :attr:`MATRIX_ATTRIBUTES <here_location_services.config.matrix_routing_config.MATRIX_ATTRIBUTES>`"
