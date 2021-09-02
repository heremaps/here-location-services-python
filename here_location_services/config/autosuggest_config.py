# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines all the configs which will be required as inputs to autosuggest API."""

from .base_config import Bunch


class SearchCircle:
    """A class to define ``SearchCircle``

    Results will be returned if they are located within the specified circular area
        defined by its center and radius(in meters).
    """

    def __init__(self, lat: float, lng: float, radius: int):
        self.lat = lat
        self.lng = lng
        self.radius = radius


class PoliticalView(Bunch):
    """A Class to define constant values for political view

    ``RUS``:
    expressing the Russian view on Crimea

    ``SRB``:
    expressing the Serbian view on Kosovo, Vukovar and Sarengrad Islands

    ``MAR``:
    expressing the Moroccan view on Western Sahara
    """


#: Use this config for political_view of Autosuggest API.
#: Example: for ``RUS`` political_view use ``POLITICAL_VIEW.RUS``.
POLITICAL_VIEW = PoliticalView(
    **{
        "RUS": "RUS",
        "SRB": "SRB",
        "MAR": "MAR",
    }
)


class Show(Bunch):
    """A Class to define constant values for showing additional fields to be
    rendered in the response.

    ``phonemes``:
    Renders phonemes for address and place names into the results.

    ``tz``:
    BETA: Renders result items with additional time zone information.
    Please note that this may impact latency significantly.
    """


#: Use this config for show of Autosuggest API.
#: Example: for ``RUS`` show use ``SHOW.phonemes``.
SHOW = Show(**{"phonemes": "phonemes", "tz": "tz"})
