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

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
mode                   string                                                          Represents how route is calculated. Example: ``fastest;car;traffic:disabled;motorway:-3``.
range                  string                                                          A range of isoline, unit is defined by parameter range type.
range_type             string                                                          Type of ``range``. Possible values are ``distance``, ``time`` and ``consumption``. For distance the unit is meters. For a time the unit is seconds.For consumption, it is defined by the consumption model.
start                  list                                                            A list of latitude and longitude representing the center of isoline request. Default value is ``None``.
destination            list                                                            A list of latitude and longitude representing the center of isoline request. Isoline will cover all roads from which this point can be reached within a given range. Default value is ``None``. It can not be used in combination with the ``start`` parameter.
arrival                string                                                          Time when travel is expected to end. It can be used only if the parameter ``destination`` is also used. Default value is ``None``.
departure              string                                                          Time when travel is expected to start. It can be used only if the parameter ``start`` is also used. Default value is ``None``.
===================    ============================================================    ===