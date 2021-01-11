#!/bin/bash

set -e

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

# Needed for pyenv
brew install zlib

# Needed for some build scripts
brew install coreutils


# Install the standard set of packages needed to build Ren'Py.
brew install ffmpeg freetype fribidi glew sdl2 sdl2_image sdl2_gfx sdl2_mixer sdl2_ttf jpeg-turbo

. $BASE/nightly/git.sh
