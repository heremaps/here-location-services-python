# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains classes for accessing the responses from Location Services RESTful APIs.
"""

import json

import flexpolyline as fp
from geojson import Feature, FeatureCollection, LineString, Point, Polygon
from pandas import DataFrame


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


class RoutingResponse(ApiResponse):
    """A class representing the search routing API response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"routes": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))

    def to_geojson(self):
        """Return API response as GeoJSON."""
        feature_collection = FeatureCollection([])
        for route in self.response["routes"]:
            for section in route["sections"]:
                polyline = section["polyline"]
                lstring = fp.decode(polyline)
                lstring = [(coord[1], coord[0], coord[2]) for coord in lstring]
                f = Feature(geometry=LineString(lstring), properties=section)
                feature_collection.features.append(f)
        return feature_collection


class MatrixRoutingResponse(ApiResponse):
    """A class representing Matrix routing response data."""

    def __init__(self, **kwargs):
        super().__init__()
        self._filters = {"matrix": None}
        for param, default in self._filters.items():
            setattr(self, param, kwargs.get(param, default))

    def to_geojson(self):
        """Return API response as GeoJSON."""
        raise NotImplementedError("This method is not valid for MatrixRoutingResponse.")

    def to_distnaces_matrix(self):
        """Return distnaces matrix in a dataframe."""
        if self.matrix and self.matrix.get("distances"):
            distances = self.matrix.get("distances")
            dest_count = self.matrix.get("numDestinations")
            nested_distances = [
                distances[i : i + dest_count] for i in range(0, len(distances), dest_count)
            ]
            return DataFrame(nested_distances, columns=range(dest_count))

    def to_travel_times_matrix(self):
        """Return travel times matrix in a dataframe."""
        if self.matrix and self.matrix.get("travelTimes"):
            distances = self.matrix.get("travelTimes")
            dest_count = self.matrix.get("numDestinations")
            nested_distances = [
                distances[i : i + dest_count] for i in range(0, len(distances), dest_count)
            ]
            return DataFrame(nested_distances, columns=range(dest_count))
