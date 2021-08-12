Isoline Routing
===============
`Isoline Routing API <https://developer.here.com/documentation/routing/dev_guide/topics/request-isoline.html>`_ is used to calculate the area that a driver can reach within a given time or distance.

Example
-------

.. jupyter-execute::

    import os
    from datetime import datetime

    from here_location_services import LS
    from here_map_widget import Map, Marker, GeoJSON
    from here_location_services.config.isoline_routing_config import RANGE_TYPE, ISOLINE_ROUTING_TRANSPORT_MODE

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    iso_response = ls.calculate_isoline(
        origin=[52.53086, 13.38469],
        range="1800",
        departure_time=datetime.now(),
        range_type=RANGE_TYPE.time,
        transport_mode=ISOLINE_ROUTING_TRANSPORT_MODE.car,
    )

    data = iso_response.to_geojson()
    geo_layer = GeoJSON(data=data)

    iso_marker = Marker(lat=52.53086, lng=13.38469)

    m = Map(api_key=LS_API_KEY, center=[52.53086, 13.38469], zoom=9)
    m.add_layer(geo_layer)
    m.add_object(iso_marker)
    m

Attributes
----------

============================================================   =======================================================================================    ===
Attribute                                                      Type                                                                                       Doc
============================================================   =======================================================================================    ===
range                                                          string                                                                                     A string representing a range of isoline, unit is defined by parameter ``range_type``.
range_type                                                     string                                                                                     A string representing a type of ``range``. Possible values are defined in :attr:`RANGE_TYPE <here_location_services.config.isoline_routing_config.RANGE_TYPE>` .
transport_mode                                                 string                                                                                     Represents transport mode to be used for the calculation of isolines. Values are defined in :attr:`ISOLINE_ROUTING_TRANSPORT_MODE <here_location_services.config.isoline_routing_config.ISOLINE_ROUTING_TRANSPORT_MODE>`.
origin                                                         list                                                                                       optional A list of ``latitude`` and ``longitude`` for centers of the isoline request. The Isoline(s) will cover the region which can be reached from this point within given range. Cannot be used in combination with ``destination`` parameter.
departure_time                                                 :func:`datetime.datetime`                                                                  optional departure time.
destination                                                    list                                                                                       optional A list of ``latitude`` and ``longitude`` for centers of the isoline request. The Isoline(s) will cover the region within the specified range that can reach this point. It cannot be used in combination with ``origin`` parameter.
arrival_time                                                   :func:`datetime.datetime`                                                                  optional arrival time.
routing_mode                                                   string                                                                                     optional routing mode is defined in  :attr:`ROUTING_MODE <here_location_services.config.isoline_routing_config.ROUTING_MODE>`
shape_max_points                                               int                                                                                        optional An integer to Limit the number of points in the resulting isoline geometry. If the isoline consists of multiple components, the sum of points from all components is considered. This parameter doesn't affect performance.
optimised_for                                                  string                                                                                     optional A string to specify how isoline calculation is optimized. Specify values from config: :attr:`OPTIMISED_FOR <here_location_services.config.isoline_routing_config.OPTIMISED_FOR>`
avoid_features                                                 list                                                                                       optional specify values from config: :attr:`ISOLINE_ROUTING_AVOID_FEATURES <here_location_services.config.isoline_routing_config.ISOLINE_ROUTING_AVOID_FEATURES>` to avoid features during isoline calculation.
truck                                                          object of :class:`Truck <here_location_services.config.base_config.Truck>`                 optional used to define truck options when transport mode is truck.
origin_place_options                                           :class:`PlaceOptions <here_location_services.config.base_config.PlaceOptions>`             optional place options for ``origin``.
origin_waypoint_options                                        :class:`WayPointOptions <here_location_services.config.base_config.WayPointOptions>`       optional waypoint options for ``origin``.
destination_place_options                                      :class:`PlaceOptions <here_location_services.config.base_config.PlaceOptions>`             optional place options for ``destination``.
destination_waypoint_options                                   :class:`WayPointOptions <here_location_services.config.base_config.WayPointOptions>`       optional waypoint options for ``destination``.
============================================================   =======================================================================================    ===