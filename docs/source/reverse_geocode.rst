Reverse Geocode
===============
To find the nearest address to specific geocoordinates, you can use `Reverse Geocode API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-reverse-geocode-brief.html>`_.

Example
-------

.. jupyter-execute::

    import os

    from here_location_services import LS

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    rev_gc_response = ls.reverse_geocode(lat=52.53086, lng=13.38469)
    rev_gc_response.items[0]["address"]["label"]


Attributes
----------

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
lat                    float                                                           Latitude of point.
lng                    float                                                           Longitude of point.
limit                  int                                                             Maximum number of results to be returned. Default value is 1.
lang                   string                                                          Language to be used for result rendering from a list of BCP47 compliant Language Codes.
===================    ============================================================    ===