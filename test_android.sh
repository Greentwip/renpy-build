#!/bin/bash

set -e

ROOT="$(dirname $(readlink -f $0))"
PYTHON_VERSION="3"
export RENPY_PYTHON_VER=$PYTHON_VERSION

VENV="$ROOT/tmp/virtualenv.py2"
if [ ! -e $VENV/bin ]; then
    python -m virtualenv $VENV
fi

. $VENV/bin/activate


if [ "$1" == "build" ]; then
    pushd "$ROOT"
        ./build.py --platform android rebuild rapt rapt-sdl2
    popd    
elif [ "$1" == "install-sdk" ]; then
    pushd "$ROOT/renpy/rapt2"
        export PGS4A_NO_TERMS=1
	    python android.py installsdk
    popd
elif [ "$1" != "" ]; then
    pushd "$ROOT/renpy/rapt2"
        ./android.py build "$1" installDebug --launch
    popd
fi



#rm -f "$ROOT/renpy/rapt/Sdk"
#ln -s "/home/tom/ab/android/Sdk" "$ROOT/renpy/rapt/Sdk"
#mkdir -p "$ROOT/renpy/rapt/project"
#cp -a /home/tom/ab/android/local.properties "$ROOT/renpy/rapt/project"




#rm -Rf "$ROOT/renpy/rapt/prototype/renpyandroid/src/main/java" || true
#cp -aL rapt/prototype/renpyandroid/src/main/java $ROOT/renpy/rapt/prototype/renpyandroid/src/main/