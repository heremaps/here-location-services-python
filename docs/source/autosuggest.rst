Autosuggest
===============
`Autosuggest endpoint of HERE Geocoding & Search API  <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-autosuggest-brief.html>`_ improves the user's search experience by allowing submittal of free-form, incomplete and misspelled addresses or place names to the endpoint.

Example
-------

.. jupyter-execute::

    import os

    from here_location_services import LS
    from here_map_widget import Map, Marker, Group

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    autosuggest_response = ls.autosuggest(
        query="bar", 
        limit=5, 
        at=["-13.163068,-72.545128"],
        terms_limit=3,
    )

    print("Query Items:")
    for item in autosuggest_response.queryTerms:
      print(item)

    print("Search Items:")
    for item in autosuggest_response.items:
      print(item) 
    
    results = []
    for item in autosuggest_response.items:
        if item["resultType"] == "place":
            results.append(
                Marker(
                    lat=item["position"]["lat"],
                    lng=item["position"]["lng"],
                    data=item["title"],
                )
            )
    group = Group(volatility=True)
    group.add_objects(results)
    m = Map(
        api_key=LS_API_KEY,
        center=[-13.163068,-72.545128],
        zoom=14,
    )
    m.add_object(group)
    m

Attributes
----------

====================   =======================================================================================    ===
Attribute              Type                                                                                       Doc
====================   =======================================================================================    ===
query                  string                                                                                     A string for free-text query. Example: `res`, `rest`
at                     list                                                                                       optional Specify the center of the search context expressed as list of coordinates. One of `at`, `search_in_circle` or `search_in_bbox` is required. Parameters "at", "search_in_circle" and "search_in_bbox" are mutually exclusive. Only one of them is allowed.
search_in_circle       :class:`SearchCircle <here_location_services.config.autosuggest_config.SearchCircle>`      optional Search within a circular geographic area provided as latitude, longitude, and radius (in meters)
search_in_bbox         tuple                                                                                      optional Search within a rectangular bounding box geographic area provided as tuple of west longitude, south latitude, east longitude, north latitude
in_country             list                                                                                       optional Search within a specific or multiple countries provided as comma-separated ISO 3166-1 alpha-3 country codes. The country codes are to be provided in all uppercase. Must be accompanied by exactly one of `at`, `search_in_circle` or `search_in_bbox`.
limit                  int                                                                                        optional An integer specifiying maximum number of results to be returned.
terms_limit            int                                                                                        optional An integer specifiying maximum number of Query Terms Suggestions to be returned.
lang                   list                                                                                       optional List of strings to select the language to be used for result rendering from a list of BCP 47 compliant language codes.
political_view         string                                                                                     optional Toggle the political view by passing a string from :attr:`POLITICAL_VIEW <here_location_services.config.autosuggest_config.POLITICAL_VIEW>`. 
show                   list                                                                                       optional Select additional fields from :attr:`SHOW <here_location_services.config.autosuggest_config.SHOW>`.  to be rendered in the response.
====================   =======================================================================================    ===