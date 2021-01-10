#!/bin/bash

set -e


ROOT=$(cd $(dirname $0); pwd)
REFS=$ROOT
BASE="$ROOT"

# Needed to build things.
brew install ccache
brew install python

# Needed by renpy-build itself.
brew install jinja2-cli

# Needed by gcc.
brew install gmp
brew install mpfr
brew install mpc

# Needed by hostpython.
brew install openssl
brew install bzip2

# Needed for mac
brea install cmake
brew install xml2

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

brew install freetype
brew install fribidi
brew install glew
brew install sdl2
brew install sdl2_image 
brew install sdl2_gfx 
brew install sdl2_mixer
brew install sdl2_ttf
brew install jpeg-turbo

mkdir -p "$BASE/tmp"

# Set up the environment variables.
pip install --upgrade pip
pip install virtualenv


VENV="$ROOT/tmp/virtualenv.py3"

. $BASE/nightly/git.sh
. $BASE/nightly/python.sh