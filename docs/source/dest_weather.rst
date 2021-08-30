Destination Weather
====================
`Destination Weather API  <https://platform.here.com/services/details/hrn:here:service::olp-here:destination-weather-3/overview>`_ provides weather forecasts and reports on current weather conditions. It also provides information on severe weather alerts along a specified route or a single car location.

Example
-------

.. jupyter-execute::

    import os
    from here_location_services import LS
    from here_map_widget import Map, MarkerCluster, ObjectLayer
    from here_location_services.config.dest_weather_config import DEST_WEATHER_PRODUCT


    LS_API_KEY = os.environ.get("LS_API_KEY")
    ls = LS(api_key=LS_API_KEY)

    result1 = ls.get_dest_weather(
        at=[19.1503, 72.8530],
        products=[DEST_WEATHER_PRODUCT.observation]
    )

    results = []
    m = Map(
        api_key=LS_API_KEY,
        center=[19.1621, 73.0008],
        zoom=7,
    )
    for observation in result1.places[0]["observations"]:
        results.append(
                dict(
                    lat=observation["place"]["location"]["lat"],
                    lng=observation["place"]["location"]["lng"],
                    data=observation["description"] + " " + str(observation["temperature"]) + "C",
                )
            )

    provider = MarkerCluster(data_points=results, show_bubble=True)
    layer = ObjectLayer(provider=provider)
    m.add_layer(layer)
    m

Attributes
----------

====================   ===============================================================================================================       ===
Attribute              Type                                                                                                                  Doc
====================   ===============================================================================================================       ===
products               list of :class:`DestWeatherProduct <here_location_services.config.dest_weather_config.DestWeatherProduct>`            A string for free-text query. Example: `res`, `rest`
at                     list                                                                                                                  optional Specify the center of the search context expressed as list of coordinates. One of `at`, `search_in_circle` or `search_in_bbox` is required. Parameters "at", "search_in_circle" and "search_in_bbox" are mutually exclusive. Only one of them is allowed.
query                  str                                                                                                                   optional Search within a circular geographic area provided as latitude, longitude, and radius (in meters)
hourly_date            :func:`datetime.datetime`                                                                                             optional Search within a rectangular bounding box geographic area provided as tuple of west longitude, south latitude, east longitude, north latitude
one_observation        bool                                                                                                                  optional Search within a specific or multiple countries provided as comma-separated ISO 3166-1 alpha-3 country codes. The country codes are to be provided in all uppercase. Must be accompanied by exactly one of `at`, `search_in_circle` or `search_in_bbox`.
language               str                                                                                                                   optional An integer specifiying maximum number of results to be returned.
units                  :class:`DestWeatherUnits <here_location_services.config.dest_weather_config.DestWeatherUnits>`                        optional An integer specifiying maximum number of Query Terms Suggestions to be returned.
====================   ===============================================================================================================       ===