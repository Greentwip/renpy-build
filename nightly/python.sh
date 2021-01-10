#!/bin/bash

set -e

if [ ! -e $VENV/bin ]; then
    python -m virtualenv $VENV
fi

. $VENV/bin/activate

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
