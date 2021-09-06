# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to
    Destination Weather API."""

from .base_config import Bunch


class DestWeatherProduct(Bunch):
    """A class to define constant attributes for ``product`` parameter identifying the
        type of report to obtain.

    ``observation``:
    current weather conditions from the eight closest locations to the specified location

    ``forecast_7days``:
    morning, afternoon, evening and night weather forecasts for the next seven days.

    ``forecast_7days_simple``:
    daily weather forecasts for the next seven days

    ``forecast_hourly``:
    hourly weather forecasts for the next seven days

    ``alerts``:
    forecasted weather alerts for the next 24 hours

    ``nws_alerts``:
    all active watches and warnings for the US and Canada
    """


product = {
    "observation": "observation",
    "forecast7days": "forecast7days",
    "forecast7daysSimple": "forecast7daysSimple",
    "forecastHourly": "forecastHourly",
    "alerts": "alerts",
    "nwsAlerts": "nwsAlerts",
}

#: Use this config for ``products``` of Destination Weather API.
#: Example: for ``forecastHourly`` product use ``DEST_WEATHER_PRODUCT.forecastHourly``.
DEST_WEATHER_PRODUCT = DestWeatherProduct(**product)


class DestWeatherUnits(Bunch):
    """A class to define constant attributes for ``units`` parameter identifying
        units of measurement used.

    ``metric``:
    Follow metric system of measurements. Default.

    ``imperial``:
    Follow imperial system of measurements

    """


units = {
    "metric": "metric",
    "imperial": "imperial",
}

#: Use this config for ``units``` of Destination Weather API.
#: Example: for ``metric`` units use ``DEST_WEATHER_UNITS.metric``.
DEST_WEATHER_UNITS = DestWeatherUnits(**units)


class WeatherSeverity(Bunch):
    """A class to define the severity of the weather event

    ``insignificant``:
    Event doesn't have significance by nature

    ``no_alerts``:
    There are no alerts for the location

    ``minor``:
    Minor Severity, the event is potentially dangerous but not usual

    ``medium``:
    Medium Severity, the event is dangerous

    ``high``:
    High Severity, The event is very dangerous

    ``emergency``:
    Emergency. Take immediate action to protect life.
    """


weather_severity = {
    "insignificant": 0,
    "no_alerts": 1,
    "minor": 2,
    "medium": 3,
    "high": 4,
    "emergency": 5,
}

#: Use this config for ``weather_severity``` of get weather alerts endpoint.
#: Example: for ``high severity`` events use ``WEATHER_SEVERITY.high``.
WEATHER_SEVERITY = WeatherSeverity(**weather_severity)


class WeatherType(Bunch):
    """A class to define the type of the weather event"""


weather_type = {
    "extremely_high_temperature": 1,
    "extremely_low_temperature": 2,
    "fog": 3,
    "ice": 4,
    "rain": 5,
    "snow": 6,
    "thunderstorm": 7,
    "wind": 8,
    "air_quality": 9,
    "volcanic_ashfall": 10,
    "avalanche": 11,
    "tsunami": 12,
    "dust_storm": 13,
    "earthquake": 14,
    "fire_danger": 15,
    "flood": 16,
    "high_waves": 17,
    "gigh_uv_index": 18,
    "low_water": 19,
    "smoke": 20,
    "volcano": 21,
    "ice_in_waterway": 22,
    "coastal_event": 23,
    "civil_danger": 24,
    "evacuation": 25,
    "hazardous_material": 26,
    "radiological_hazard": 27,
    "shelter_in_place": 28,
    "warning": 29,
}

#: Use this config for ``weather_type``` of get weather alerts endpoint of Destination Weather API.
#: Example: for ``fog`` weather type use ``WEATHER_TYPE.fog``.
WEATHER_TYPE = WeatherType(**weather_type)
