# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This is a collection of utilities for using Here Location Services.
"""

import os
import warnings


def get_apikey() -> str:
    """
    Read and return the value of the environment variable ``LS_API_KEY``.

    :return: The string value of the environment variable or an empty string
        if no such variable could be found.
    """
    api_key = os.environ.get("LS_API_KEY")
    if api_key is None:
        warnings.warn("No token found in environment variable LS_API_KEY.")

    return api_key or ""
