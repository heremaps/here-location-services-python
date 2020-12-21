Lookup
======
Every place or location object known by HERE has a location identifier or "ID". `Lookup API <https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-lookup-brief.html>`_ is used to look up a place by its HERE ID.

Example
-------

.. code-block:: python

    import os

    from here_location_services import LS

    LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
    ls = LS(api_key=LS_API_KEY)

    lookup = ls.lookup(location_id="here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2")

    lookup.response


Attributes
----------

===================    ============================================================    ===
Attribute              Type                                                            Doc
===================    ============================================================    ===
location_id            string                                                          A HERE location ``ID`` to lookup.
lang                   string                                                          Language to be used for result rendering from a list of BCP47 compliant Language Codes. Default value is ``None``.
===================    ============================================================    ===