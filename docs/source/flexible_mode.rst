Flexible Mode
=============

Flexible mode provides capabilities such as Custom options, Time Awareness (including Live Traffic), Unlimited Region
but it has a limited Matrix Size.
Given a list of origins and a list of destinations, the service computes the shortest travel times or distances between every pair of origin and destination.
These results make up the entries of the `routing matrix <https://developer.here.com/documentation/matrix-routing-api/8.3.0/dev_guide/topics/concepts/matrix.html>`_.

In order to provide support for custom routing options, time awareness, and routes of arbitrary length,
Flexible Mode cannot benefit from the optimizations that give Region and Profile modes their high performance.
Due to this performance limitation, Flexible Mode requests are limited to:

- at most 15 origins and 100 destinations (15 x 100)
- at most 100 origins and 1 destination (100 x 1)

Formulating a request
---------------------
The flexible mode is utilized when:

the region definition  = WorldRegion
and no profile parameter is specified
The service applies live and historical traffic information unless explicitly disabled by setting departureTime to the special value any.

Below is an example of a 3x3 matrix request with the following origins and destinations:

- San Francisco at (37.76, -122.42)
- New York at (40.63, -74.09)
- Austin at (30.26, -97.74)

Example
-------

.. jupyter-execute::

    import os

    from here_location_services import LS
    from here_location_services.config.matrix_routing_config import (
        WorldRegion,
        MATRIX_ATTRIBUTES,
    )

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
    ]
    region_definition = WorldRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances, MATRIX_ATTRIBUTES.travelTimes]

    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        matrix_attributes=matrix_attributes,
    )
    result.matrix

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
        "truck", "object of :class:`Truck <here_location_services.config.base_config.Truck>`", "Used to define truck options when transport mode is truck"
        "matrix_attributes", "list", "Use values from config: :attr:`MATRIX_ATTRIBUTES <here_location_services.config.matrix_routing_config.MATRIX_ATTRIBUTES>`"


