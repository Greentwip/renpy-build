#!/bin/bash

update () {
    if [ -d "$BASE/$2/.git" ]; then
        pushd "$BASE/$2"
        git reset --hard
        git pull
        popd
    else
        if [ -e "$REFS/$2/.git" ]; then
            git clone $1 "$BASE/$2" --reference "$REFS/$2"
        else
            git clone $1 "$BASE/$2"
        fi
    fi
}

updatepython3(){
    git clone -b Python3 $1 "$BASE/$2" --reference "$REFS/$2"
}

updatepython3 https://github.com/greentwip/renpy-build
update https://github.com/renpy/renpy renpy
update https://github.com/renpy/pygame_sdl2 pygame_sdl2
update https://github.com/renpy/renpyweb renpyweb
