from renpybuild.model import task, annotator
import os

version = "3.9.1"


@annotator
def annotate(c):
    if c.python == "2":
        c.var("pythonver", "python2.7")
    else:
        c.var("pythonver", "python3.8")

    c.include("{{ install }}/include/{{ pythonver }}")


@task(kind="python", pythons="3")
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/Python-{{version}}.tgz")


@task(kind="python", pythons="3", platforms="linux,mac,ios")
def patch_posix(c):
    pass


@task(kind="python", pythons="3", platforms="ios")
def patch_ios(c):
    pass


@task(kind="python", pythons="3", platforms="windows")
def patch_windows(c):
    pass


@task(kind="python", pythons="3", platforms="android")
def patch_android(c):
    pass



@task(kind="python", pythons="3", platforms="linux,mac")
def build_posix(c):
    c.var("version", version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")

        if c.platform == "ios":
            f.write("ac_cv_little_endian_double=yes\n")
            f.write("ac_cv_header_langinfo_h=no\n")
            f.write("ac_cv_func_getentropy=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "{{ CFLAGS  }} -DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H ")

    c.run("""./configure {{ cross_config }} --prefix="{{ install }}" --with-system-ffi --enable-ipv6""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup")

    c.run("""{{ make }} install""")

    c.copy("{{ host }}/bin/python3", "{{ install }}/bin/hostpython3")


@task(kind="python", pythons="2", platforms="ios")
def build_ios(c):
    c.var("version", version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")
        f.write("ac_cv_little_endian_double=yes\n")
        f.write("ac_cv_header_langinfo_h=no\n")
        f.write("ac_cv_func_getentropy=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "{{ CFLAGS }} -DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H ")

    c.run("""./configure {{ cross_config }} --prefix="{{ install }}" --with-system-ffi --disable-toolbox-glue --enable-ipv6""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup")

    c.run("""{{ make }} install""")

    c.copy("{{ host }}/bin/python3", "{{ install }}/bin/hostpython3")


@task(kind="python", pythons="3", platforms="android")
def build_android(c):
    c.var("version", version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")
        f.write("ac_cv_little_endian_double=yes\n")
        f.write("ac_cv_header_langinfo_h=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "{{ CFLAGS }} -DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H -DOPENSSL_THREADS")

    c.env("READELF", "arm-linux-androideabi-readelf")
    c.run("""./configure --target=arm-linux-androideabi --build=x86_64-linux-gnu  {{ cross_config }} --prefix="{{ install }}" --with-system-ffi --enable-ipv6""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup")

    c.run("""{{ make }} install""")

    c.copy("{{ host }}/bin/python3", "{{ install }}/bin/hostpython3")


@task(kind="python", pythons="3", platforms="windows")
def build_windows(c):

    c.var("version", version)

    c.chdir("Python-{{ version }}")

    c.env("MSYSTEM", "MINGW")
    c.env("PYTHON_FOR_BUILD", "{{ host }}/bin/python3")
    c.env("LDFLAGS", "{{ LDFLAGS }} -static-libgcc")

    c.run("""./configure {{ cross_config }} --enable-shared --prefix="{{ install }}" --with-threads --with-system-ffi""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup")

    with open(c.path("Lib/plat-generic/regen"), "w") as f:
        f.write("""\
#! /bin/sh
set -v
CCINSTALL=$($1 -print-search-dirs | head -1 | cut -d' ' -f2)
REGENHEADER=${CCINSTALL}/include/stddef.h
eval $PYTHON_FOR_BUILD ../../Tools/scripts/h2py.py -i "'(u_long)'" $REGENHEADER
""")

    c.run("""{{ make }} install""")
    c.copy("{{ host }}/bin/python3", "{{ install }}/bin/hostpython3")


@task(kind="python", pythons="3")
def pip(c):

    if (c.platform == "android"):
        c.copy("{{ host }}/lib/python3.9/_sysconfigdata__linux_x86_64-linux-gnu.py", "{{ host }}/lib/python3.9/lib-dynload/_sysconfigdata__linux_x86_64-linux-gnu.py")

    c.env("PYTHONPATH", '{{host}}/lib/python3.9/lib-dynload')
    exec_string = "{{ install }}/bin/hostpython3 -s "
    #exec_string = exec_string + """ -c "import sys;"""
    #exec_string = exec_string + """ sys.path.append('{{host}}'); """

    #exec_string = exec_string + """ sys.path.append('{{host}}/lib/python39.zip'); """
    #exec_string = exec_string + """ sys.path.append('{{host}}/lib/python3.9'); """
    #exec_string = exec_string + """ sys.path.append('{{host}}/lib/lib-dynload'); """
    #exec_string = exec_string + """ sys.path.append('{{host}}/lib/python3.9/site-packages'); " """

    ensure_pip = exec_string + " -m ensurepip "

    c.run(ensure_pip)

    
    install_str1 = exec_string + " -m pip install --upgrade future six rsa pyasn1 "
    install_str2 = exec_string + " -m pip install --upgrade urllib3 certifi idna requests "
    c.run(install_str1)
    c.run(install_str2)

# @task(kind="python", pythons="2", always=True)
# def sitecustomize(c):
#     c.run("install {{ source }}/sitecustomize.py {{ install }}/lib/{{ pythonver }}/sitecustomize.py")
#     c.run("{{ install }}/bin/hostpython2 -m compileall {{ install }}/lib/{{ pythonver }}/sitecustomize.py")
