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
    pushd "$BASE/$2"
        git checkout Python3
        git reset --hard
        git pull
    popd
}

clonepython3(){
    if [ -d "$BASE/$2/.git" ]; then
        pushd "$BASE/$2"
        git checkout Python3
        git reset --hard
        git pull
        popd
    else
        if [ -e "$REFS/$2/.git" ]; then
            git clone -b Python3 $1 "$BASE/$2" --reference "$REFS/$2"
        else
            git clone -b Python3 $1 "$BASE/$2"
        fi
    fi
}

clonepython3_lowercase(){
    if [ -d "$BASE/$2/.git" ]; then
        pushd "$BASE/$2"
        git checkout python3
        git reset --hard
        git pull
        popd
    else
        if [ -e "$REFS/$2/.git" ]; then
            git clone -b Python3 $1 "$BASE/$2" --reference "$REFS/$2"
        else
            git clone -b Python3 $1 "$BASE/$2"
        fi
    fi
}


updatepython3 https://github.com/greentwip/renpy-build
clonepython3_lowercase https://github.com/Greentwip/renpy renpy
clonepython3 https://github.com/greentwip/pygame_sdl2 pygame_sdl2
#update https://github.com/renpy/renpyweb renpyweb
