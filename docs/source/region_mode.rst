Region Mode
===========
This section refers to calculating matrices with custom options using a limited-sized region.
The region is limited to the max. 400km diameter.
By restricting the calculation to a specific region of at most 400 km diameter, it is possible to specify different options to take into account during calculation. The service applies live and historical traffic information unless explicitly disabled by setting `departure_time` to the special value `any`.

Region Mode supports:

- Custom options
- Time Awareness (including Live Traffic), using a snapshot of time at departure
- Matrix Sizes up to 10,000 x 10,000
- Region limited to max. 400km diameter

BoundingBox region definition
-----------------------------

Below is an example of a simple 3 x 3 matrix in Berlin, Germany with these origins and destinations:

- Alexanderplatz at (52.52103, 13.41268)
- Brandenburg Gate at (52.51628, 13.37771)
- Tempelhof Field at (52.47342, 13.40357)

To calculate a car distance matrix, you can use the below code.
Since the request does not specify a destinations list, the origins are taken as destinations and the resulting matrix is a 3 x 3 matrix.
The region definition is a bounding box around the points with a small margin added to be able to properly route in the vicinity of the points.
By default, the service calculates a travel times matrix, but since we want to get distances in the response instead of times, the request specifies the ``matrix_attributes`` property with the value ``distances``.

Example
-------

.. code-block:: python

    from here_location_services import LS
    from here_location_services.config.matrix_routing_config import (
        BoundingBoxRegion,
        AutoCircleRegion,
        MATRIX_ATTRIBUTES,
        WorldRegion,
    )

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)  # Create Location Services object using API KEY.

    origins = [
        {"lat": 52.52103, "lng": 13.41268},
        {"lat": 52.51628, "lng": 13.37771},
        {"lat": 52.47342, "lng": 13.40357},
    ]
    region_definition = BoundingBoxRegion(north=52.53, south=52.46, west=13.35, east=13.42)
    matrix_attributes = [MATRIX_ATTRIBUTES.distances]

    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        matrix_attributes=matrix_attributes,
        async_req=True,
    )
    result.matrix

AutoCircle region definition
----------------------------

Instead of defining a bounding box around the origins, you can request for a circle to be automatically derived.
The request below is for the same as the one above, but using the AutoCircle feature. Since the margin field is not provided,
the service uses a default value of 10 kilometers.

Example
-------

.. code-block:: python

    from here_location_services import LS
    from here_location_services.config.matrix_routing_config import (
        BoundingBoxRegion,
        AutoCircleRegion,
        MATRIX_ATTRIBUTES,
        WorldRegion,
    )

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)  # Create Location Services object using API KEY.

    origins = [
        {"lat": 52.52103, "lng": 13.41268},
        {"lat": 52.51628, "lng": 13.37771},
        {"lat": 52.47342, "lng": 13.40357},
    ]
    region_definition = AutoCircleRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances]

    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        matrix_attributes=matrix_attributes,
        async_req=True
    )

    result.response


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
