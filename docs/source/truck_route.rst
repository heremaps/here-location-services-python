Truck route Example
========================
Calculate truck route between origin and destination.

.. code-block:: python

    import os

    from here_location_services import LS
    from here_location_services.config.routing_config import ROUTING_RETURN
    from here_map_widget import Map, Marker, GeoJSON

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    result = ls.truck_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        return_results=[
            ROUTING_RETURN.polyline,
            ROUTING_RETURN.elevation,
            ROUTING_RETURN.instructions,
            ROUTING_RETURN.actions,
        ],
    )
    geo_json = result.to_geojson()
    data = geo_json
    geo_layer = GeoJSON(data=data, style={"lineWidth": 5})

    m = Map(api_key=LS_API_KEY, center=[52.5207, 13.4283], zoom=14)
    origin_marker = Marker(lat=52.51375, lng=13.42462)
    dest_marker = Marker(lat=52.52332, lng=13.42800)
    m.add_layer(geo_layer)
    m.add_object(origin_marker)
    m.add_object(dest_marker)
    m


Attributes
----------

============================    =======================================================================================    ===
Attribute                       Type                                                                                       Doc
============================    =======================================================================================    ===
origin                          list                                                                                       A list of ``latitude`` and ``longitude`` of ``origin`` point of route.
destination                     list                                                                                       A list of ``latitude`` and ``longitude`` of ``destination`` point of route.
via                             list                                                                                       A list of tuples of ``latitude`` and ``longitude`` of ``via`` points.
origin_place_options            :class:`PlaceOptions <here_location_services.config.routing_config.PlaceOptions>`          optinal place options for ``origin``.
destination_place_options       :class:`PlaceOptions <here_location_services.config.routing_config.PlaceOptions>`          optional place options for ``destination``.
via_place_options               :class:`PlaceOptions <here_location_services.config.routing_config.PlaceOptions>`          optinal place options for ``via``.
destination_waypoint_options    :class:`WayPointOptions <here_location_services.config.routing_config.WayPointOptions>`    optional way point options for ``destination``.
via_waypoint_options            :class:`WayPointOptions <here_location_services.config.routing_config.WayPointOptions>`    optional way point options for ``via``.
departure_time                  :func:`datetime.datetime`                                                                  optional departure time.
routing_mode                    string                                                                                     optional routing mode is defined in  :attr:`ROUTING_MODE <here_location_services.config.routing_config.ROUTING_MODE>`
alternatives                    int                                                                                        optional number of alternative routes to return aside from the optimal route. default value is ``0`` and maximum is ``6``.
units                           string                                                                                     optional representing units of measurement used in guidance instructions, valid values are ``metric`` and ``imperial``, default value is ``metric``.
lang                            string                                                                                     optional preferred language of the response. The value should comply with the IETF BCP 47, default is ``en-US``.
return_results                  list                                                                                       optional list of strings, values are defined in :attr:`ROUTING_RETURN <here_location_services.config.routing_config.ROUTING_RETURN>`
spans                           list                                                                                       optional list of strings, values are defined in :attr:`ROUTING_SPANS <here_location_services.config.routing_config.ROUTING_SPANS>`
============================    =======================================================================================    ===