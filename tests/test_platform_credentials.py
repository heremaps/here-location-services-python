# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0
"""This module will test platform credentials."""

import tempfile
from pathlib import Path

import pytest

from here_location_services.exceptions import ConfigException
from here_location_services.platform.credentials import PlatformCredentials


def test_from_credentials_file():
    """Test credentials from file."""
    file_path = Path(__file__).parent / Path("data") / Path("dummy_credentials.properties")
    cred = PlatformCredentials.from_credentials_file(file_path)
    assert cred.cred_properties["user"] == "dummy_user_id"
    assert cred.cred_properties["client"] == "dummy_client_id"
    assert cred.cred_properties["key"] == "dummy_access_key_id"
    assert cred.cred_properties["secret"] == "dummy_access_key_secret"
    assert cred.cred_properties["endpoint"] == "dummy_token_endpoint"
    with pytest.raises(ConfigException):
        with tempfile.NamedTemporaryFile() as tmp:
            _ = PlatformCredentials.from_credentials_file(tmp.name)


def test_erronous_credential_file():
    """Test credential file with error."""
    file_path = Path(__file__).parent / Path("data") / Path("erroneous_credential.properties")
    with pytest.raises(ConfigException) as execinfo:
        PlatformCredentials.from_credentials_file(file_path)
    assert execinfo.value.args[0] == "Erroneous "
