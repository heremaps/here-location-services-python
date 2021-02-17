# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

"""Project setup file."""

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get the core dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

# get extra dependencies
with open(path.join(here, "requirements_dev.txt"), encoding="utf-8") as f:
    dev_reqs = f.read().strip().split("\n")

packages = find_packages(exclude=["docs", "tests"])
version = {}
with open("{}/__version__.py".format(packages[0])) as f:
    exec(f.read(), version)

download_url = (
    "https://github.com/heremaps/here-location-services-python"
    "/archive/" + version["__version__"] + ".zip"
)


setup(
    version=version["__version__"],
    url="https://here.com",
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={"dev": dev_reqs},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
