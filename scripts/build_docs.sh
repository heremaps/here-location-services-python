#!/usr/bin/env bash

# Copyright (C) 2019-2021 HERE Europe B.V.
# SPDX-License-Identifier: Apache-2.0

# If the search path in conf.py is not set-up this will inspect the installed

export DEST=docs/source
rm -rf $DEST/_build
rm -rf $DEST/_static
rm -rf $DEST/_templates

# Just creating conf.py, Makefile and make.bat once, hence commenting below.

sphinx-apidoc --private --separate --module-first --full -o $DEST here_location_services
sphinx-build -b html -D html_theme=sphinx_rtd_theme $DEST $DEST/_build/html
