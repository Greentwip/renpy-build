#!/bin/bash

set -e


ROOT=$(cd $(dirname $0); pwd)
REFS=$ROOT
BASE="$ROOT"

# Needed to build things.
brew install ccache python

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
brew install ffmpeg \
--with-chromaprint \
--with-fdk-aac \
--with-fontconfig \
--with-freetype \
--with-frei0r \
--with-game-music-emu \
--with-libass \
--with-libbluray \
--with-libbs2b \
--with-libcaca \
--with-libgsm \
--with-libmodplug \
--with-libsoxr \
--with-libssh \
--with-libvidstab \
--with-libvorbis \
--with-libvpx \
--with-opencore-amr \
--with-openh264 \
--with-openjpeg \
--with-openssl \
--with-opus \
--with-rtmpdump \
--with-rubberband \
--with-sdl2 \
--with-snappy \
--with-speex \
--with-tesseract \
--with-theora \
--with-tools \
--with-two-lame \
--with-wavpack \
--with-webp \
--with-x265 \
--with-xz \
--with-zeromq \
--with-zimg

brew install freetype fribidi glew sdl2 sdl2_image sdl2_gfx sdl2_mixer sdl2_ttf jpeg-turbo

mkdir -p "$BASE/tmp"

# Set up the environment variables.
pip install --upgrade pip
pip install virtualenv


VENV="$ROOT/tmp/virtualenv.py3"

. $BASE/nightly/git.sh
. $BASE/nightly/python.sh