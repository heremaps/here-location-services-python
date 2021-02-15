# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""This module defines API exceptions."""


class ApiError(Exception):
    """Exception raised for API HTTP response status codes not in [200...300).

    The exception value will be the response object returned by :mod:`requests`
    which provides access to all its attributes, eg. :attr:`status_code`,
    :attr:`reason` and :attr:`text`, etc.
    """

    def __str__(self):
        """Return a string from the HTTP response causing the exception.

        The string simply lists the repsonse's status code, reason and text
        content, separated with commas.
        """
        resp = self.args[0]
        return f"{resp.status_code}, {resp.reason}, {resp.text}"
