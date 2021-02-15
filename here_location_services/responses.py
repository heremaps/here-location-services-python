# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains classes for accessing the responses from Location Services RESTful APIs.
"""

import json

from geojson import Feature, FeatureCollection, Point, Polygon


class ApiResponse:
    """Base class for all the responses from Location Services RESTful APIs."""

    def __init__(self, **kwargs):
        self._filters = {}
        self.response = None

    def __str__(self):
        return self.as_json_string()

    def as_json_string(self, encoding: str = "utf8"):
        """Return API response as json string."""
        json_string = json.dumps(self.response, sort_keys=True, ensure_ascii=False).encode(
            encoding
        )
        return json_string.decode()

    def to_geojson(self):
        """Return API response as GeoJSON."""
        feature_collection = FeatureCollection([])
        for item in self.response["items"]:
            f = Feature(
                geometry=Point((item["position"]["lng"], item["position"]["lat"])), properties=item
            )
            feature_collection.features.append(f)
        return feature_collection

    @classmethod
    def new(cls, resp):
        """Instantiate a response object from raw response returned by API."""
        json_data = resp.copy()
        obj = cls(**json_data)
        obj.response = resp
        return obj


class GeocoderResponse(ApiResponse):
    """A class representing the Geocoder API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"items": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))


class ReverseGeocoderResponse(ApiResponse):
    """A class representing the Reverse Geocoder API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"items": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))


class IsolineResponse(ApiResponse):
    """A class representing the Reverse Isoline routing API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"metaInfo": None, "center": None, "isoline": None, "start": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))

    def to_geojson(self):
        """Return API response as GeoJSON."""
        points = []
        for latlons in self.isoline[0]["component"][0]["shape"]:
            latlon = [float(i) for i in latlons.split(",")]
            points.append((latlon[1], latlon[0]))
        feature = Feature(geometry=Polygon([points]))
        return feature


class DiscoverResponse(ApiResponse):
    """A class representing the search discover API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"items": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))


class BrowseResponse(ApiResponse):
    """A class representing the search browse API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"items": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))


class LookupResponse(ApiResponse):
    """A class representing the search lookup API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"items": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs)
