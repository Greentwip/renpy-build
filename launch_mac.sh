#!/bin/bash

set -e

ROOT=$(cd $(dirname $0); pwd)
REFS=$ROOT
BASE="$ROOT"

VENV="$ROOT/tmp/virtualenv.py3"

export RENPY_DEPS_INSTALL=/usr/local\
::/usr\
::/usr/lib\
::usr/local/lib\
::/usr/local/opt/zlib/lib\
::/usr/local/opt/openssl/lib\
::/usr/local/opt/zlib/lib\
::/usr/local/opt/bzip2/lib

. $BASE/nightly/launch.sh

