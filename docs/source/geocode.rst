Geocode
=========
`HERE Geocoding & Search API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-geocode-brief.html>`_ is used to find the geo-coordinates of a known address, place, locality or administrative area, even if the query is incomplete or partly incorrect. It also returns a complete postal address string and address details.

Example
-------

.. code-block:: python

    import os

    from here_location_services import LS
    from here_map_widget import Map, GeoJSON

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    address = "Invalidenstr 116, 10115 Berlin, Germany"
    gc_response = ls.geocode(query=address)

    data = gc_response.to_geojson()
    geo_layer = GeoJSON(data=data)

    m = Map(api_key=LS_API_KEY, center=[52.53086, 13.38469], zoom=12)
    m.add_layer(geo_layer)
    m


Attributes
----------

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
query                  string                                                          An input address query.
limit                  int                                                             Maximum number of results to be returned. Default value is 20.
lang                   string                                                          Language to be used for result rendering from a list of BCP47 compliant Language Codes.
===================    ============================================================    ===