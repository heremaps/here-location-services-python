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
