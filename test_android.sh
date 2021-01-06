#!/bin/bash

set -e

ROOT="$(dirname $(readlink -f $0))"
PYTHON_VERSION="$4"
export RENPY_PYTHON_VER="$PYTHON_VERSION"

pushd "$ROOT"
if [ "$2" == "build" ]; then
    ./build.py --platform android rebuild rapt rapt-sdl2
fi
popd


#rm -f "$ROOT/renpy/rapt/Sdk"
#ln -s "/home/tom/ab/android/Sdk" "$ROOT/renpy/rapt/Sdk"
#mkdir -p "$ROOT/renpy/rapt/project"
#cp -a /home/tom/ab/android/local.properties "$ROOT/renpy/rapt/project"

pushd "$ROOT/renpy/rapt2"
if [ "$3" == "install-sdk" ]; then
    export PGS4A_NO_TERMS=1
	python android.py installsdk
fi
popd

#rm -Rf "$ROOT/renpy/rapt/prototype/renpyandroid/src/main/java" || true
#cp -aL rapt/prototype/renpyandroid/src/main/java $ROOT/renpy/rapt/prototype/renpyandroid/src/main/

if [ "$1" != "" ]; then
    $ROOT/renpy/renpy.sh $ROOT/renpy/launcher android_build "$1" installDebug --launch
fi
