from renpybuild.model import task
python_version = "3.9"

import os

@task(kind="python")
def clean(c):
    c.clean()


@task(kind="python", always=True)
def gen_static(c):
    print("// GEN STATIC //")
    c.var("python_version", python_version)

    c.chdir("{{ renpy }}/module")

    c.env("RENPY_ANDROID", "True")
    c.env("PYGAME_SDL2_ANDROID", "True")

    c.env("CFLAGS", "-I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include -shared")
    c.env("LDFLAGS", "-L{{sysroot_lib}} -L{{install}} -L{{install}}/lib -shared")

    c.env("{{CFLAGS}}", "{{CFLAGS}} -DANDROID")

    #c.env("PYGAME_SDL2_CFLAGS", "{{CFLAGS}}")
    #c.env("PYGAME_SDL2_LDFLAGS", "{{LDFLAGS}}")

    c.env("PY_OVERRIDEN_CROSS_BUILD", "True")

    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")
    c.env("_PYTHON_SYSCONFIGDATA_NAME", "_sysconfigdata__linux_")

    #c.env("RENPY_EXTRA_LIB_DIRS", "-l{{sysroot_lib}} -l{{install}} -l{{install}}/lib")
    #c.env("PY_DISTUTILS_EXT_LIB_DIRS", "-l{{sysroot_lib}} -l{{install}} -l{{install}}/lib")

    if c.platform == "android":
        c.env("RENPY_DEPS_INSTALL", "{{sysroot_include}}::{{sysroot_lib}}::{{install}}::{{install}}/lib::{{install}}/include")
    else:
        c.env("RENPY_DEPS_INSTALL", "/usr::/usr/lib/x86_64-linux-gnu/")

    c.run("{{ hostpython }} setup.py build")

    quit()


@task(kind="python", always=True)
def build(c):
    print("RENPY BUILD")

    c.env("CFLAGS", """"-I{{ pygame_sdl2 }}" "-I{{ pygame_sdl2 }}/src" "-I{{ renpy }}/module" """)

    if c.python == "3":
        gen = "gen3-static/"
    else:
        gen = "gen-static/"

    modules = [ ]
    sources = [ ]

    def read_setup(dn):

        with open(dn / "Setup") as f:
            for l in f:
                l = l.partition("#")[0]
                l = l.strip()

                if not l:
                    continue

                parts = l.split()

                modules.append(parts[0])

                for i in parts[1:]:
                    i = i.replace("gen/", gen)
                    sources.append(dn / i)

    read_setup(c.pygame_sdl2)
    read_setup(c.renpy / "module")

    if c.platform == "android":
        read_setup(c.path("{{ pytmp }}/pyjnius"))

    if c.platform == "ios":
        read_setup(c.path("{{ install }}/pyobjus"))

    objects = [ ]

    for source in sources:

        object = str(source.name)[:-2] + ".o"
        objects.append(object)

        c.var("src", source)
        c.var("object", object)
        c.run("{{ CC }} {{ CFLAGS }} -c {{ src }} -o {{ object }}", verbose=True)

    c.generate("{{ source }}/librenpy_inittab.c", "inittab.c", modules=modules)
    c.run("{{ CC }} {{ CFLAGS }} -c inittab.c -o inittab.o", verbose=True)
    objects.append("inittab.o")

    c.var("objects", " ".join(objects))

    c.run("{{ AR }} r librenpy.a {{ objects }} inittab.o", verbose=True)
    c.run("{{ RANLIB }} librenpy.a", verbose=True)

    c.copy("librenpy.a", "{{ install }}/lib/librenpy.a")
