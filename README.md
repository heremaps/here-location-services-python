# HERE Location Services for Python

[![Tests](https://github.com/heremaps/here-location-services-python/workflows/Tests/badge.svg)](https://github.com/heremaps/here-location-services-python/actions)
[![Documentation Status](https://readthedocs.org/projects/here-location-services-python/badge/?version=latest)](https://here-location-services-python.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/heremaps/here-location-services-python/master?urlpath=lab/tree/docs/notebooks)

A Python client for [HERE Location Services](https://developer.here.com/documentation#services).

## Usage
**[Geocoding using HERE Geocoding & Search API](https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-geocode-brief.html).**
# ![Geocoding Example](https://github.com/heremaps/here-location-services-python/raw/master/images/geocoding.gif)

## Prerequisites

Before you can install `HERE Location Services for Python`, run its test-suite, or use the example notebooks to make sure you meet the following prerequisites:

- A Python installation, 3.6+ recommended, with the `pip` command available to install dependencies.
- A HERE developer account, freely available under [HERE Developer Portal](https://developer.here.com).
- An [API key](https://developer.here.com/documentation/identity-access-management/dev_guide/topics/dev-apikey.html) from the [HERE Developer Portal](https://developer.here.com), in an environment variable named `LS_API_KEY` which you can set like this (with a valid value, of course):
  ```bash
  $ export LS_API_KEY="MY-LS-API-KEY"
  ```
  
## Installation

- Install `HERE Location Services for Python` from [PyPI](https://pypi.org/) using the below command:
  
  ```bash
  $ pip install here-location-services
  ```

- Install `HERE Location Services for Python` from GitHub using the below command:
  
  ```bash
  $ pip install -e git+https://github.com/heremaps/here-location-services-python#egg=here-location-services
  ```

## Run Test Suite

To run the test suite you can do this locally, which should provide a test coverage of 100%:

```bash
$ pip install -r requirements_dev.txt
$ pytest -v --cov=here_location_services tests
```

## Documentation

Documentation is available [here](https://here-location-services-python.readthedocs.io/en/latest/).

Run the below commands to build the docs locally:

```bash
$ pip install -e .
$ pip install -r requirements_dev.txt
$ sh scripts/build_docs.sh
```

## Hello World Example
This is a tiny "Hello World" like example that you can run to geocode the given address right away. Just make sure to use your own real API key.

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

# License
Copyright (C) 2019-2021 HERE Europe B.V.

See the [License](LICENSE) file in the root of this project for license details.