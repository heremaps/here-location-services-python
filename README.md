# HERE Location Services for Python

[![Tests](https://github.com/heremaps/here-location-services-python/workflows/Tests/badge.svg)](https://github.com/heremaps/here-location-services-python/actions)
[![Documentation Status](https://readthedocs.org/projects/here-location-services-python/badge/?version=stable)](https://here-location-services-python.readthedocs.io/en/stable/?badge=stable)
[![codecov](https://codecov.io/gh/heremaps/here-location-services-python/branch/master/graph/badge.svg?token=G7Q1DWFI3W)](https://codecov.io/gh/heremaps/here-location-services-python)
[![PyPI - Status](https://img.shields.io/pypi/status/here-location-services)](https://pypi.org/project/here-location-services/)
[![PyPI - Python Version](https://img.shields.io/pypi/v/here-location-services.svg?logo=pypi)](https://pypi.org/project/here-location-services/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/here-location-services)](https://pypi.org/project/here-location-services/)
[![PyPI - License](https://img.shields.io/pypi/l/here-location-services)](https://pypi.org/project/here-location-services/)
[![Downloads](https://pepy.tech/badge/here-location-services)](https://pepy.tech/project/here-location-services)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/here-location-services?logo=conda-forge)](https://anaconda.org/conda-forge/here-location-services)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/here-location-services)](https://anaconda.org/conda-forge/here-location-services)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/here-location-services/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/here-location-services)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/heremaps/here-location-services-python/master?urlpath=lab/tree/docs/notebooks)

A Python client for [HERE Location Services](https://developer.here.com/documentation#services).

## Usage
**[Geocoding using HERE Geocoding & Search API](https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-geocode-brief.html).**
# ![Geocoding Example](https://github.com/heremaps/here-location-services-python/raw/master/images/geocoding.gif)
**[Isolines using HERE Isoline Routing API](https://developer.here.com/documentation/isoline-routing-api/dev_guide/index.html).**
# ![Isolines Example](https://github.com/heremaps/here-location-services-python/raw/master/images/isolines.gif)

## Prerequisites

Before you can install `HERE Location Services for Python`, run its test-suite, or use the example notebooks to make sure you meet the following prerequisites:

- A Python installation, 3.6+ recommended, with the `pip` command available to install dependencies.
- In order to use Location services APIs, authentication is required. 
  There are two ways to authenticate:
  - Authentication using an API key: 
    - For API key-based authentication you will need a HERE developer account, freely available under [HERE Developer Portal](https://developer.here.com).
    - An [API key](https://developer.here.com/documentation/identity-access-management/dev_guide/topics/dev-apikey.html) from the [HERE Developer Portal](https://developer.here.com), in an environment variable named `LS_API_KEY` which you can set like this (with a valid value, of course):
      ```bash
      $ export LS_API_KEY="MY-LS-API-KEY"
      ```
  - OAuth token-based authentication:
    - For OAuth token authentication you will need an account on the HERE Platform.
      To get more details on the HERE Platform account please check our documentation [Get a HERE account](https://developer.here.com/documentation/identity-access-management/dev_guide/topics/obtain-user-credentials.html).
    Once you have the account follow the below steps to get credentials:
    - Go to [HERE Platform Applications and Keys](https://platform.here.com/profile/apps-and-keys) and register a new app.
    - Create a key for the app and download the generated `credentials. properties` file.

    The HERE platform generated app credentials should look similar to the example below:
    ```
    here.user.id = <example_here>
    here.client.id = <example_here>
    here.access.key.id = <example_here>
    here.access.key.secret = <example_here>
    here.token.endpoint.url = <example_here>
    ```
    You can provide your credentials using any of the following methods:
    - Default credentials
    - Environment variables
    - Credentials file

    #### Default credentials
    Place the credentials file into

    For Linux/MacOS: `$HOME/.here/credentials.properties`

    For Windows: `%USERPROFILE%\.here\credentials.properties`
    Code snippet to instantiate LS object:
    ```python
    from here_location_services import LS
    
    # platform credentials will be picked from the default credentials file's location mentioned above
    # and api_key should not be set in env variable LS_API_KEY.
    ls = LS()
    ```

    #### Environment Variables
    You can override default credentials by assigning values to the following environment variables:
    ```
    HERE_USER_ID
    HERE_CLIENT_ID
    HERE_ACCESS_KEY_ID
    HERE_ACCESS_KEY_SECRET
    HERE_TOKEN_ENDPOINT_URL
    ```
    Code snippet to instantiate LS object:
    ```python
    from here_location_services import LS
    from here_location_services import PlatformCredentials
   
    ls = LS(platform_credentials=PlatformCredentials.from_env()) 
    ```
    #### Credentials File
    You can specify any credentials file as an alternative to that found in `~/.here/credentials.properties`. An error is generated if there is no file present at the path, or if the file is not properly formatted.
    Code snippet to instantiate LS object:
    ```python
    from here_location_services import LS
    from here_location_services import PlatformCredentials
    
    platform_credentials = PlatformCredentials.from_credentials_file("<Path_to_file>")
    ls = LS(platform_credentials=platform_credentials) 
    ```
  
## Installation

- Install `HERE Location Services for Python` with conda from the Anaconda [conda-forge channel](https://anaconda.org/conda-forge/here-location-services) using the below command:

    ```bash
    $ conda install -c conda-forge here-location-services
    ```
- Install `HERE Location Services for Python` from [PyPI](https://pypi.org/project/here-location-services/) using the below command:

  ```bash
  $ pip install here-location-services
  ```

- Install `HERE Location Services for Python` from GitHub using the below command:

  ```bash
  $ pip install -e git+https://github.com/heremaps/here-location-services-python#egg=here-location-services
  ```

## Run Test Suite

Run the test suite using below commands:

```bash
$ pip install -r requirements_dev.txt
$ pytest -v --cov=here_location_services tests
```

## Documentation

Documentation is available [here](https://here-location-services-python.readthedocs.io/en/stable/).

Run the below commands to build the docs locally:

```bash
$ pip install -e .
$ pip install -r requirements_dev.txt
$ sh scripts/build_docs.sh
```

## Hello World Example
The following are tiny "Hello World" like examples that you can run to have a successful first XYZ experience right after installation!

#### Using API key
```python
import json
import os

from here_location_services import LS


LS_API_KEY = os.environ.get("LS_API_KEY")  # Get API KEY from environment.
ls = LS(api_key=LS_API_KEY)

address = "Invalidenstr 116, 10115 Berlin, Germany"
geo = ls.geocode(query=address)
print(json.dumps(geo.to_geojson(), indent=2, sort_keys=True))
```
#### Using OAuth token
```python
import json

from here_location_services import LS
from here_location_services import PlatformCredentials

credentials = PlatformCredentials.from_default()
ls = LS(platform_credentials=credentials)

address = "Invalidenstr 116, 10115 Berlin, Germany"
geo = ls.geocode(query=address)
print(json.dumps(geo.to_geojson(), indent=2, sort_keys=True))
```

# License
Copyright (C) 2019-2021 HERE Europe B.V.

See the [License](LICENSE) file at the root of this project for license details.

