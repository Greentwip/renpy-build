#!/bin/bash

set -e

pip install --upgrade pip
pip install -r $ROOT/requirements.txt

# Delete the generated files.
rm -Rf renpy/module/gen-static
rm -Rf renpy/module/gen3-static
rm -Rf renpy/module/gen
rm -Rf renpy/module/gen3

rm -Rf pygame_sdl2/gen-static
rm -Rf pygame_sdl2/gen3-static
rm -Rf pygame_sdl2/gen
rm -Rf pygame_sdl2/gen3
popd
