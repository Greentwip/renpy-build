Ren'Py Build
============

The purpose of the Ren'Py build system is to provide a single system that
can build the binary components of Ren'Py and all its dependencies, in
the same manner that is used to make official Ren'Py releases.

Requirements
-------------

macOS, Xcode, XCode command line tools, Python 3.9 and pyenv

Preparing
---------

To install Python 3 via pyenv you need to run:
brew install openssl
brea install bzip2 
brew install zlib

And finally:
brew install pyenv

Before getting into code you have to ensure and install pyenv and
run the following:

    pyenv install 3.9.0
    pyenv global 3.9.0

And then don't forget to run (and append to ~./zshrc)
eval "$(pyenv init -)"

Note: There seems to be a bug while installing with pyenv on mac, zlib can't be found.

Refer to this:
https://github.com/pyenv/pyenv/wiki/Common-build-problems#build-failed-error-the-python-zlib-extension-was-not-compiled-missing-the-zlib

Most likely you would run:
CCFLAGS="-I$(brew --prefix openssl)/include  -I$(brew --prefix bzip2)/include -I$(brew --prefix zlib)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib"  pyenv install 3.9.0

Which has openssl, bzip and zlib paths from brew.

To get ready to build, run the following
command to clone renpy-build::

    git clone https://github.com/renpy/renpy-build

Change into the renpy-build directory, and run::

    ./prepare_mac.sh

This will first install all the packages required to build Ren'Py, and
then it will clone Ren'Py and pygame_sdl2. It will also create a python
virtual environment with the tools in it. If this completes successfully,
you are ready to build.

Finally, a number of files need to be downloaded from third parties. These
are listed in tars/README.rst.

Building
---------
Check build.py and uncomment the build platforms you want to build.
Right now we're focused on armeabi_v7a, other platforms might fail to build

        Platform("linux", "x86_64")
        Platform("linux", "i686")
        Platform("linux", "armv7l")

        Platform("windows", "x86_64")
        Platform("windows", "i686")

        Platform("mac", "x86_64")

        Platform("android", "x86_64")
        Platform("android", "arm64_v8a")
        Platform("android", "armeabi_v7a")

        Platform("ios", "arm64")
        Platform("ios", "armv7s")
        Platform("ios", "x86_64")



