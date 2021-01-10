#!/bin/bash

set -e


ROOT=$(cd $(dirname $0); pwd)
REFS=$ROOT
BASE="$ROOT"

# Needed to build things.
brew install ccache

# Needed by renpy-build itself.
brew install jinja2-cli

# Needed by gcc.
brew install gmp mpfr mpc

# Needed by hostpython.
brew install openssl bzip2

# Needed for mac
brew install cmake xml2

# Needed for web
brew install quilt

# Neede for pyenv
brew install zlib


# Install the standard set of packages needed to build Ren'Py.
brew install ffmpeg freetype fribidi glew sdl2 sdl2_image sdl2_gfx sdl2_mixer sdl2_ttf jpeg-turbo

mkdir -p "$BASE/tmp"


VENV="$ROOT/tmp/virtualenv.py3"

export RENPY_DEPS_INSTALL=/usr/local\
::/usr\
::/usr/lib\
::usr/local/lib\
::/usr/local/opt/zlib/lib\
::/usr/local/opt/openssl/lib\
::/usr/local/opt/zlib/lib\
::/usr/local/opt/bzip2/lib

. $BASE/nightly/git.sh
. $BASE/nightly/python.sh