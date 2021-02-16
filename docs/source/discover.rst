Discover
========
`Discover endpoint of HERE Geocoding & Search API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-discover-brief.html>`_ simplifies searching for places. The user submits a free-form text request that returns candidate items (places and addresses related) in the order of intent matching relevance.

Example
-------

.. code-block:: python

    import os

    from here_location_services import LS
    from here_map_widget import Map, GeoJSON

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    disc_response = ls.discover(query="coffee", center=[52.53086, 13.38469], radius=1000)

    data = disc_response.to_geojson()
    geo_layer = GeoJSON(data=data)

    m = Map(api_key=LS_API_KEY, center=[52.53086, 13.38469], zoom=15)
    m.add_layer(geo_layer)
    m


Attributes
----------

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
query                  string                                                          free-text query to search places.
center                 list                                                            A list of latitude and longitude representing the center for search query. Default value is ``None``.
radius                 int                                                             A radius in meters along with center for searching places. Default value is ``None``.
country_codes          list                                                            A list of  ISO 3166-1 alpha-3 country codes. Default value is ``None``.
bounding_box           list                                                            A bounding box, provided as west longitude, south latitude, east longitude, north latitude. Default value is ``None``.
limit                  int                                                             Maximum number of results to be returned. Default value is ``None``.
lang                   string                                                          Language to be used for result rendering from a list of BCP47 compliant Language Codes. Default value is ``None``.
===================    ============================================================    ===