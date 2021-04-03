# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

import json
import os
from datetime import datetime

import pytest
import pytz
from geojson import FeatureCollection

from here_location_services import LS
from here_location_services.config.matrix_routing_config import (
    AVOID_FEATURES,
    MATRIX_ATTRIBUTES,
    PROFILE,
    SHIPPED_HAZARDOUS_GOODS,
    AutoCircleRegion,
    AvoidBoundingBox,
    BoundingBoxRegion,
    CircleRegion,
    PolygonRegion,
    Truck,
    WorldRegion,
)
from here_location_services.config.routing_config import AVOID_FEATURES as ROUTING_AVOID_FEATURES
from here_location_services.config.routing_config import (
    ROUTE_COURSE,
    ROUTE_MATCH_SIDEOF_STREET,
    ROUTING_MODE,
    ROUTING_RETURN,
    ROUTING_SPANS,
    ROUTING_TRANSPORT_MODE,
    PlaceOptions,
    Scooter,
    WayPointOptions,
)
from here_location_services.config.search_config import PLACES_CATEGORIES
from here_location_services.exceptions import ApiError
from here_location_services.responses import GeocoderResponse
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_geocoding():
    """Test geocoding api. """
    address = "200 S Mathilda Sunnyvale CA"
    ls = LS(api_key=LS_API_KEY)
    resp = ls.geocode(query=address, limit=2)
    assert isinstance(resp, GeocoderResponse)
    assert resp.__str__()
    assert resp.as_json_string()
    geo_json = resp.to_geojson()
    assert geo_json.type == "FeatureCollection"
    assert geo_json.features
    pos = resp.items[0]["position"]
    assert len(resp.items) == 1
    assert pos == {"lat": 37.37634, "lng": -122.03405}


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_geocoding_exception():
    """Test geocoding api exception."""
    address = "Goregaon West, Mumbai 400062, India"

    ls = LS(api_key="dummy")
    with pytest.raises(ApiError):
        ls.geocode(query=address)
    with pytest.raises(ValueError):
        ls.geocode(query="")
        ls.geocode(query="   ")


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_reverse_geocoding():
    """Test reverse geocoding."""
    ls = LS(api_key=LS_API_KEY)
    resp = ls.reverse_geocode(lat=19.1646, lng=72.8493)
    address = resp.items[0]["address"]["label"]
    assert "Goregaon" in address
    resp1 = ls.reverse_geocode(lat=19.1646, lng=72.8493, limit=4)
    assert len(resp1.items) == 4


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_reverse_geocoding_exception():
    """Test reverse geocoding api exception."""
    ls = LS(api_key=LS_API_KEY)
    with pytest.raises(ValueError):
        ls.reverse_geocode(lat=91, lng=90)
    with pytest.raises(ValueError):
        ls.reverse_geocode(lat=19, lng=190)
    ls = LS(api_key="dummy")
    with pytest.raises(ApiError):
        ls.reverse_geocode(lat=19.1646, lng=72.8493)


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_isonline_routing():
    """Test isonline routing api."""
    ls = LS(api_key=LS_API_KEY)
    result = ls.calculate_isoline(
        start=[52.5, 13.4],
        range="900",
        range_type="time",
        mode="fastest;car;",
        departure="2020-05-04T17:00:00+02",
    )

    coordinates = result.isoline[0]["component"][0]["shape"]
    assert coordinates[0]
    geo_json = result.to_geojson()
    assert geo_json.type == "Feature"
    assert geo_json.geometry.type == "Polygon"

    result2 = ls.calculate_isoline(
        destination=[52.5, 13.4],
        range="900",
        range_type="time",
        mode="fastest;car;",
        arrival="2020-05-04T17:00:00+02",
    )
    coordinates = result2.isoline[0]["component"][0]["shape"]
    assert coordinates[0]

    with pytest.raises(ValueError):
        ls.calculate_isoline(
            start=[52.5, 13.4],
            range="900",
            range_type="time",
            mode="fastest;car;",
            destination=[52.5, 13.4],
        )
    with pytest.raises(ApiError):
        ls2 = LS(api_key="dummy")
        ls2.calculate_isoline(
            start=[52.5, 13.4],
            range="900",
            range_type="time",
            mode="fastest;car;",
        )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_isonline_routing_exception():
    """Test isonline exceptions."""
    ls = LS(api_key=LS_API_KEY)
    with pytest.raises(ValueError):
        ls.calculate_isoline(
            range="900",
            range_type="time",
            mode="fastest;car;",
        )
    with pytest.raises(ValueError):
        ls.calculate_isoline(
            range="900",
            range_type="time",
            mode="fastest;car;",
            arrival="2020-05-04T17:00:00+02",
            start=[52.5, 13.4],
        )
    with pytest.raises(ValueError):
        ls.calculate_isoline(
            range="900",
            range_type="time",
            mode="fastest;car;",
            departure="2020-05-04T17:00:00+02",
            destination=[52.5, 13.4],
        )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_discover():
    ls = LS(api_key=LS_API_KEY)
    result = ls.discover(query="starbucks", center=[19.1663, 72.8526], radius=10000, lang="en")
    assert len(result.items) == 20

    result2 = ls.discover(
        query="starbucks",
        center=[19.1663, 72.8526],
        country_codes=["IND"],
        limit=2,
    )
    assert len(result2.items) == 2

    result3 = ls.discover(
        query="starbucks",
        bounding_box=[13.08836, 52.33812, 13.761, 52.6755],
    )
    assert len(result3.items) == 20

    with pytest.raises(ValueError):
        ls.discover(
            query="starbucks",
            center=[52.5, 13.4],
            bounding_box=[13.08836, 52.33812, 13.761, 52.6755],
        )

    with pytest.raises(ApiError):
        ls2 = LS(api_key="dummy")
        ls2.discover(query="starbucks", center=[19.1663, 72.8526], radius=10000, limit=10)


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_browse():
    ls = LS(api_key=LS_API_KEY)
    result = ls.browse(
        center=[19.1663, 72.8526],
        radius=9000,
        limit=5,
        categories=[
            PLACES_CATEGORIES.historical_monument,
            PLACES_CATEGORIES.museum,
            PLACES_CATEGORIES.park_recreation_area,
            PLACES_CATEGORIES.leisure,
            PLACES_CATEGORIES.shopping_mall,
        ],
        lang="en",
    )
    assert len(result.items) == 5

    result2 = ls.browse(
        center=[19.1663, 72.8526],
        name="starbucks",
        country_codes=["IND"],
        limit=10,
        categories=[PLACES_CATEGORIES.restaurant],
        lang="en",
    )
    assert len(result2.items) == 10

    result3 = ls.browse(
        center=[19.1663, 72.8526],
        name="starbucks",
        bounding_box=[13.08836, 52.33812, 13.761, 52.6755],
        categories=[PLACES_CATEGORIES.restaurant],
        lang="en",
    )
    assert len(result3.items) == 13

    with pytest.raises(ApiError):
        ls2 = LS(api_key="dummy")
        ls2.browse(
            center=[19.1663, 72.8526],
            radius=9000,
            limit=5,
            categories=[
                PLACES_CATEGORIES.historical_monument,
                PLACES_CATEGORIES.museum,
                PLACES_CATEGORIES.park_recreation_area,
                PLACES_CATEGORIES.leisure,
                PLACES_CATEGORIES.shopping_mall,
            ],
        )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_ls_lookup():
    ls = LS(api_key=LS_API_KEY)
    result = ls.lookup(
        location_id="here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2",
        lang="en",
    )
    assert result.response["title"] == "Frankfurt-Hahn Airport"

    with pytest.raises(ApiError):
        ls2 = LS(api_key="dummy")
        ls2.lookup(location_id="here:pds:place:276u0vhj-b0bace6448ae4b0fbc1d5e323998a7d2")


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_credentials_exception():
    """Test exception if environment variable ``LS_API_KEY`` is not present."""
    api_key = os.environ.get("LS_API_KEY")
    del os.environ["LS_API_KEY"]
    with pytest.raises(Exception):
        _ = LS()
    os.environ["LS_API_KEY"] = api_key


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_car_route():
    """Test routing API for car route."""
    ls = LS(api_key=LS_API_KEY)
    avoid_areas = [AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)]
    avoid_features = [ROUTING_AVOID_FEATURES.tollRoad]
    result = ls.car_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000)],
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
        avoid_areas=avoid_areas,
        avoid_features=avoid_features,
        exclude=["IND", "NZL", "AUS"],
    )
    assert result.response["routes"][0]["sections"][0]["departure"]["place"]["location"] == {
        "lat": 52.5137479,
        "lng": 13.4246242,
        "elv": 76.0,
    }
    assert result.response["routes"][0]["sections"][1]["departure"]["place"]["location"] == {
        "lat": 52.5242323,
        "lng": 13.4301462,
        "elv": 80.0,
    }
    assert type(result.to_geojson()) == FeatureCollection


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_car_route_extra_options():
    """Test routing API for car route."""
    place_options = PlaceOptions(
        course=ROUTE_COURSE.west,
        sideof_street_hint=[52.512149, 13.304076],
        match_sideof_street=ROUTE_MATCH_SIDEOF_STREET.always,
        radius=10,
        min_course_distance=10,
    )
    assert json.loads(place_options.__str__()) == {
        "course": 270,
        "sideOfStreetHint": "52.512149,13.304076",
        "matchSideOfStreet": "always",
        "namehint": None,
        "radius": 10,
        "minCourseDistance": 10,
    }
    via_waypoint_options = WayPointOptions(stop_duration=0, pass_through=True)
    assert json.loads(via_waypoint_options.__str__()) == {"stopDuration": 0, "passThrough": True}
    dest_waypoint_options = WayPointOptions(stop_duration=10, pass_through=False)
    ls = LS(api_key=LS_API_KEY)
    _ = ls.car_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000), (52.123, 13.22), (52.343, 13.444)],
        origin_place_options=place_options,
        destination_place_options=place_options,
        via_place_options=place_options,
        via_waypoint_options=via_waypoint_options,
        destination_waypoint_options=dest_waypoint_options,
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
    )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_bicycle_route():
    """Test routing API for car route."""
    ls = LS(api_key=LS_API_KEY)
    avoid_areas = [AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)]
    avoid_features = [ROUTING_AVOID_FEATURES.tollRoad]
    _ = ls.bicycle_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000)],
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
        avoid_areas=avoid_areas,
        avoid_features=avoid_features,
        exclude=["IND", "NZL", "AUS"],
    )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_truck_route():
    """Test routing API for truck route."""
    ls = LS(api_key=LS_API_KEY)
    truck = Truck(
        shipped_hazardous_goods=[SHIPPED_HAZARDOUS_GOODS.explosive],
        gross_weight=100,
        weight_per_axle=10,
        height=10,
        width=10,
        length=10,
        tunnel_category="B",
        axle_count=4,
    )
    avoid_areas = [AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)]
    avoid_features = [ROUTING_AVOID_FEATURES.tollRoad]
    _ = ls.truck_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000)],
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
        truck=truck,
        avoid_areas=avoid_areas,
        avoid_features=avoid_features,
        exclude=["IND", "NZL", "AUS"],
    )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_scooter_route():
    """Test routing API for scooter route."""
    ls = LS(api_key=LS_API_KEY)
    scooter = Scooter(allow_highway=True)
    _ = ls.scooter_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000)],
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
        scooter=scooter,
        exclude=["IND", "NZL", "AUS"],
    )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_pedestrian_route():
    """Test routing API for pedestrian route."""
    ls = LS(api_key=LS_API_KEY)
    _ = ls.pedestrian_route(
        origin=[52.51375, 13.42462],
        destination=[52.52332, 13.42800],
        via=[(52.52426, 13.43000)],
        return_results=[ROUTING_RETURN.polyline, ROUTING_RETURN.elevation],
        departure_time=datetime.now(),
        spans=[ROUTING_SPANS.names],
        exclude=["IND", "NZL", "AUS"],
    )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_matrix_route_exception():
    """Test exceptions for Matrix routing."""
    ls = LS(api_key=LS_API_KEY)
    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
        {"lat": 40.63, "lng": -74.09},
    ]
    region_definition = CircleRegion(radius=1000, center={"lat": 37.76, "lng": -122.42})
    matrix_attributes = [MATRIX_ATTRIBUTES.distances, MATRIX_ATTRIBUTES.travelTimes]
    profile = PROFILE.carFast
    truck = Truck(
        shipped_hazardous_goods=[SHIPPED_HAZARDOUS_GOODS.explosive],
        gross_weight=100,
        weight_per_axle=10,
        height=10,
        width=10,
        length=10,
        tunnel_category="B",
        axle_count=4,
    )
    with pytest.raises(ValueError):
        ls.matrix(
            origins=origins,
            region_definition=region_definition,
            profile=profile,
            matrix_attributes=matrix_attributes,
        )

    with pytest.raises(ValueError):
        ls.matrix(
            origins=origins,
            region_definition=region_definition,
            matrix_attributes=matrix_attributes,
            transport_mode=ROUTING_TRANSPORT_MODE.car,
            truck=truck,
        )


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_matrix_route():
    """Test Matrix routing."""
    ls = LS(api_key=LS_API_KEY)
    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
    ]
    region_definition = WorldRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances, MATRIX_ATTRIBUTES.travelTimes]
    avoid_areas = AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)
    assert json.loads(avoid_areas.__str__()) == {
        "type": "boundingBox",
        "north": 68.1766451354,
        "south": 7.96553477623,
        "west": 97.4025614766,
        "east": 35.4940095078,
    }
    truck = Truck(
        shipped_hazardous_goods=[SHIPPED_HAZARDOUS_GOODS.explosive],
        gross_weight=100,
        weight_per_axle=10,
        height=10,
        width=10,
        length=10,
        tunnel_category="B",
        axle_count=4,
    )
    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        destinations=origins,
        routing_mode=ROUTING_MODE.fast,
        departure_time=datetime.now(tz=pytz.utc),
        transport_mode=ROUTING_TRANSPORT_MODE.truck,
        avoid_features=[AVOID_FEATURES.tollRoad],
        avoid_areas=[avoid_areas],
        truck=truck,
        matrix_attributes=matrix_attributes,
    )
    mat = result.matrix
    assert mat["numOrigins"] == 3
    assert mat["numDestinations"] == 3
    assert len(mat["distances"]) == 9

    profile = PROFILE.carShort
    result2 = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        matrix_attributes=matrix_attributes,
        profile=profile,
    )
    mat2 = result2.matrix
    assert mat2["numOrigins"] == 3
    assert mat2["numDestinations"] == 3
    with pytest.raises(NotImplementedError):
        result2.to_geojson()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_matrix_route_async():
    """Test Matrix routing."""
    ls = LS(api_key=LS_API_KEY)
    origins = [
        {"lat": 37.76, "lng": -122.42},
        {"lat": 40.63, "lng": -74.09},
        {"lat": 30.26, "lng": -97.74},
    ]
    region_definition = WorldRegion()
    matrix_attributes = [MATRIX_ATTRIBUTES.distances, MATRIX_ATTRIBUTES.travelTimes]
    avoid_areas = AvoidBoundingBox(68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)
    truck = Truck(
        shipped_hazardous_goods=[SHIPPED_HAZARDOUS_GOODS.explosive],
        gross_weight=100,
        weight_per_axle=10,
        height=10,
        width=10,
        length=10,
        tunnel_category="B",
        axle_count=4,
    )
    result = ls.matrix(
        origins=origins,
        region_definition=region_definition,
        async_req=True,
        destinations=origins,
        routing_mode=ROUTING_MODE.fast,
        departure_time="any",
        transport_mode=ROUTING_TRANSPORT_MODE.truck,
        avoid_features=[AVOID_FEATURES.tollRoad],
        avoid_areas=[avoid_areas],
        truck=truck,
        matrix_attributes=matrix_attributes,
    )
    mat = result.matrix
    assert mat["numOrigins"] == 3
    assert mat["numDestinations"] == 3
    assert len(mat["distances"]) == 9


def test_matrix_routing_config():
    """Test Matrix routing config objects."""
    circle = CircleRegion(radius=1000, center={"lat": 37.76, "lng": -122.42})
    assert json.loads(circle.__str__()) == {
        "type": "circle",
        "center": {"lat": 37.76, "lng": -122.42},
        "radius": 1000,
    }

    bbox = BoundingBoxRegion(0, 0, 0, 0)
    assert json.loads(bbox.__str__()) == {
        "type": "boundingBox",
        "north": 0,
        "south": 0,
        "west": 0,
        "east": 0,
    }

    poly = PolygonRegion(outer=[1, 1, 1, 1, 1, 1])
    assert json.loads(poly.__str__()) == {"type": "polygon", "outer": [1, 1, 1, 1, 1, 1]}

    autocircle = AutoCircleRegion(margin=100)
    assert json.loads(autocircle.__str__()) == {"type": "autoCircle", "margin": 100}
