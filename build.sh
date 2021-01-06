#!/bin/bash

set -e

PYTHON_VERSION="$1"
export RENPY_PYTHON_VER="$PYTHON_VERSION"

./build.py