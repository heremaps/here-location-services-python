Browse
======
`Browse endpoint of HERE Geocoding & Search API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-browse-brief.html>`_ provides a structured search by filtering items by category and name at a given geo-position and radius. Items returned are places, streets or localities, ranked by increasing distance.

Example
-------

.. jupyter-execute::

    import os

    from here_location_services import LS
    from here_location_services.config.search_config import PLACES_CATEGORIES
    from here_map_widget import Map, GeoJSON

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    browse_response = ls.browse(
        center=[52.53086, 13.38469],
        bounding_box=[13.08836, 52.33812, 13.761, 52.6755],
        categories=[PLACES_CATEGORIES.restaurant],
    )

    data = browse_response.to_geojson()
    geo_layer = GeoJSON(data=data, show_bubble=True, point_style={"radius": 6})

    m = Map(api_key=LS_API_KEY, center=[52.53086, 13.38469], zoom=15)
    m.add_layer(geo_layer)
    m


Attributes
----------

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
center                 list                                                            A list of latitude and longitude representing the center for search query.
radius                 int                                                             A radius in meters along with center for searching places. Default value is ``None``.
country_codes          list                                                            A list of  ISO 3166-1 alpha-3 country codes. Default value is ``None``.
bounding_box           list                                                            A bounding box, provided as west longitude, south latitude, east longitude, north latitude. Default value is ``None``.
categories             list                                                            A list of strings of category ids, defined as config :attr:`PLACES_CATEGORIES <here_location_services.config.search_config.PLACES_CATEGORIES>`
limit                  int                                                             Maximum number of results to be returned. Default value is ``None``.
name                   string                                                          Full-text filter on POI names/titles. Default value is ``None``.
lang                   string                                                          Language to be used for result rendering from a list of BCP47 compliant Language Codes. Default value is ``None``.
===================    ============================================================    ===