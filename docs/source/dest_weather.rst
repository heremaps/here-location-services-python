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
products               list of :class:`DestWeatherProduct <here_location_services.config.dest_weather_config.DestWeatherProduct>`            List of strings identifying the type of report to obtain.
at                     list                                                                                                                  optional A list of ``latitude`` and ``longitude`` specifying the area covered by the weather report.
query                  str                                                                                                                   optional Free text query. Examples: "125, Berliner, berlin", "Beacon, Boston"
zipcode                str                                                                                                                   optional ZIP code of the location. This parameter is supported only for locations in the United States of America.
hourly_date            :func:`datetime.datetime`                                                                                             optional Date for which hourly forecasts are to be retrieved.
one_observation        bool                                                                                                                  optional Boolean, if set to true, the response only includes the closest location. Only available when the `product` parameter is set to `DEST_WEATHER_PRODUCT.observation`.
language               str                                                                                                                   optional Defines the language used in the descriptions in the response.
units                  :class:`DestWeatherUnits <here_location_services.config.dest_weather_config.DestWeatherUnits>`                        optional Defines whether units or imperial units are used in the response.
====================   ===============================================================================================================       ===

Getting Weather Alerts
----------------------
Can be used to get information on severe weather alerts along a specified route or a single car location.

.. jupyter-execute::

    import os
    from here_location_services import LS
    from geojson import Point
    from datetime import datetime

    LS_API_KEY = os.environ.get("LS_API_KEY")
    ls = LS(api_key=LS_API_KEY)
    result = ls.get_weather_alerts(
        geometry=Point(coordinates=[15.256, 23.456]),
        start_time=datetime.now(),
        width=3000,
    )

    print(result)


Attributes
----------

====================   ===============================================================================================================       ===
Attribute              Type                                                                                                                  Doc
====================   ===============================================================================================================       ===
geometry               Point or LineString                                                                                                   Point or LineString defining the route or a single location
start_time             :func:`datetime.datetime`                                                                                             Start time of the event
id                     str                                                                                                                   optional Unique weather alert id.
weather_severity       :class:`WeatherSeverity <here_location_services.config.dest_weather_config.WeatherSeverity>`                          optional Defines the severity of the weather event
weather_type           :class:`WeatherType <here_location_services.config.dest_weather_config.WeatherType>`                                  optional Defines the type of the weather event
country                str                                                                                                                   optional String for ISO-3166-1 2-letter country code.
end_time               :func:`datetime.datetime`                                                                                             optional End time of the event. If not present, warning is valid until it is not removed from the feed by national weather institutes (valid until warning is present in the response)
width                  int                                                                                                                   optional int.
====================   ===============================================================================================================       ===
