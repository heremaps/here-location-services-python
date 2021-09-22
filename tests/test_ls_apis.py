# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

from argparse import Namespace
from datetime import datetime

import pytest
import requests
from geojson import Point

from here_location_services.config.dest_weather_config import DEST_WEATHER_PRODUCT
from here_location_services.config.isoline_routing_config import (
    ISOLINE_ROUTING_TRANSPORT_MODE,
    RANGE_TYPE,
)
from here_location_services.config.matrix_routing_config import WorldRegion
from here_location_services.config.tour_planning_config import (
    Fleet,
    Job,
    JobPlaces,
    Plan,
    Relation,
    VehicleProfile,
    VehicleType,
)
from here_location_services.exceptions import ApiError
from here_location_services.matrix_routing_api import MatrixRoutingApi
from here_location_services.utils import get_apikey

LS_API_KEY = get_apikey()


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_tour_planning(tour_planning_api):
    """Test tour planning api."""
    fleet = Fleet(
        vehicle_types=[
            VehicleType(
                id="09c77738-1dba-42f1-b00e-eb63da7147d6",
                profile="normal_car",
                costs_fixed=22,
                costs_distance=0.0001,
                costs_time=0.0048,
                capacity=[100, 5],
                skills=["fridge"],
                amount=1,
                shift_start={
                    "time": "2020-07-04T09:00:00Z",
                    "location": {"lat": 52.5256, "lng": 13.4542},
                },
                limits={"maxDistance": 20000, "shiftTime": 21600},
                shift_end={
                    "location": {"lat": 52.5256, "lng": 13.4542},
                    "time": "2020-07-04T18:00:00Z",
                },
                shift_breaks=[
                    {
                        "duration": 1800,
                        "times": [["2020-07-04T11:00:00Z", "2020-07-04T13:00:00Z"]],
                    }
                ],
            )
        ],
        vehicle_profiles=[VehicleProfile(name="normal_car", vehicle_mode="car")],
    )

    plan = Plan(
        jobs=[
            Job(
                id="4bbc206d-1583-4266-bac9-d1580f412ac0",
                pickups=[
                    JobPlaces(
                        duration=180,
                        demand=[10],
                        location=(52.53088, 13.38471),
                        times=[["2020-07-04T10:00:00Z", "2020-07-04T12:00:00Z"]],
                    )
                ],
                deliveries=[
                    JobPlaces(
                        duration=300,
                        demand=[10],
                        location=(52.53088, 13.38471),
                        times=[["2020-07-04T14:00:00Z", "2020-07-04T16:00:00Z"]],
                    )
                ],
                skills=["fridge"],
                priority=2,
            )
        ],
        relations=[
            Relation(
                type="sequence",
                jobs=["departure", "4bbc206d-1583-4266-bac9-d1580f412ac0", "arrival"],
                vehicle_id="09c77738-1dba-42f1-b00e-eb63da7147d6_1",
            )
        ],
    )
    resp = tour_planning_api.solve_tour_planning(
        fleet=fleet, plan=plan, id="7f3423c2-784a-4983-b472-e14107d5a54a"
    )
    assert type(resp) == requests.Response
    assert resp.status_code == 200


@pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
def test_destination_weather(destination_weather_api):
    """Test Destination Weather api."""
    resp = destination_weather_api.get_dest_weather(
        products=[DEST_WEATHER_PRODUCT.observation], query="Chicago"
    )
    assert type(resp) == requests.Response
    assert resp.status_code == 200


# @pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
# def test_weather_alerts(destination_weather_api):
#     """Test Destination Weather api."""
#     resp = destination_weather_api.get_weather_alerts(
#         geometry=Point(coordinates=[15.256, 23.456]),
#         start_time=datetime.now(),
#     )
#     assert type(resp) == requests.Response
#     assert resp.status_code == 200


# @pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
# def test_autosuggest(autosuggest_api):
#     """Test autosuggest api."""
#     resp = autosuggest_api.get_autosuggest(query="res", limit=5, at=["52.93175,12.77165"])
#     assert type(resp) == requests.Response
#     assert resp.status_code == 200


# @pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
# def test_geocoding(geo_search_api):
#     """Test geocoding api."""
#     address = "Goregaon West, Mumbai 400062, India"
#     resp = geo_search_api.get_geocoding(query=address)
#     assert type(resp) == requests.Response
#     assert resp.status_code == 200


# @pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
# def test_reverse_geocoding(geo_search_api):
#     """Test reverse geocoding."""
#     resp = geo_search_api.get_reverse_geocoding(lat=19.1646, lng=72.8493)
#     assert type(resp) == requests.Response
#     assert resp.status_code == 200


# @pytest.mark.skipif(not LS_API_KEY, reason="No api key found.")
# def test_isonline_routing(isoline_routing_api):
#     """Test isonline routing api."""
#     result = isoline_routing_api.get_isoline_routing(
#         origin=[52.5, 13.4],
#         range="3000",
#         range_type=RANGE_TYPE.distance,
#         transport_mode=ISOLINE_ROUTING_TRANSPORT_MODE.car,
#     )

#     coordinates = result.json()["isolines"][0]["polygons"][0]["outer"]
#     assert coordinates[0]


# def test_mock_api_error(mocker):
#     """Mock Test for geocoding api."""
#     mock_response = Namespace(status_code=300)
#     mocker.patch(
#         "here_location_services.matrix_routing_api.requests.post",
#         return_value=mock_response,
#     )
#     origins = [
#         {"lat": 37.76, "lng": -122.42},
#         {"lat": 40.63, "lng": -74.09},
#         {"lat": 30.26, "lng": -97.74},
#     ]
#     region_definition = WorldRegion()
#     mat = MatrixRoutingApi(api_key="dummy")
#     with pytest.raises(ApiError):
#         _ = mat.matrix_route(
#             origins=origins,
#             region_definition=region_definition,
#         )
