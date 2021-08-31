# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module contains classes for accessing `HERE Destination Weather API <https://developer.here.com/documentation/destination-weather/dev_guide/topics/overview.html>`_.
"""  # noqa E501

from datetime import datetime
from typing import Dict, List, Optional

from here_location_services.platform.auth import Auth

from .apis import Api
from .exceptions import ApiError


class DestinationWeatherApi(Api):
    """A class for accessing HERE routing APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        proxies: Optional[dict] = None,
        country: str = "row",
    ):
        super().__init__(api_key, auth=auth, proxies=proxies, country=country)
        self._base_url = f"https://weather.{self._get_url_string()}"

    def get_dest_weather(
        self,
        products: List[str],
        at: Optional[List] = None,
        query: Optional[str] = None,
        zipcode: Optional[str] = None,
        hourly_date: Optional[datetime] = None,
        one_observation: Optional[bool] = None,
        language: Optional[str] = None,
        units: Optional[str] = None,
    ):
        """Retrieves weather reports, weather forecasts, severe weather alerts and moon and sun rise and set information.

        See further information `Here Destination Weather API <https://developer.here.com/documentation/destination-weather/dev_guide/topics/overview.html>_`.

        :param products: List of :class:`DestWeatherProduct` identifying the type of
            report to obtain.
        :param at: A list of ``latitude`` and ``longitude`` specifying the area covered
            by the weather report.
        :param query: Free text query. Examples: "125, Berliner, berlin", "Beacon, Boston"
        :param zipcode: ZIP code of the location. This parameter is supported only for locations in
            the United States of America.
        :param hourly_date: Date for which hourly forecasts are to be retrieved.
        :param one_observation: Boolean, if set to true, the response only includes the closest
            location. Only available when the `product` parameter is set to
            `DEST_WEATHER_PRODUCT.observation`.
        :param language: Defines the language used in the descriptions in the response.
        :param units: Defines whether units or imperial units are used in the response.
        :return: :class:`requests.Response` object.
        :raises ApiError: If ``status_code`` of API response is not 200.
        """  # noqa E501

        path = "v3/report"
        url = f"{self._base_url}/{path}"
        params: Dict[str, str] = {
            "products": ",".join([str(i) for i in products]),
        }
        if at:
            params["location"] = ",".join([str(i) for i in at])
        if query:
            params["q"] = query
        if zipcode:
            params["zipCode"] = zipcode
        if hourly_date:
            params["hourlyDate"] = hourly_date.strftime("%Y-%m-%dT%H:%M:%S")
        if one_observation:
            params["oneObservation"] = "true" if one_observation else "false"
        if language:
            params["lang"] = language
        if units:
            params["units"] = units

        resp = self.get(url, params=params, proxies=self.proxies)
        if resp.status_code == 200:
            return resp
        else:
            raise ApiError(resp)