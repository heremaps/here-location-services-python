# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""
This module defines all the base classes which will be used for configuration classes of
various APIs.
"""


class Bunch(dict):
    """A class for dot notation implementation of dictionary."""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self
