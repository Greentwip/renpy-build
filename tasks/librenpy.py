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


    c.env("CFLAGS", "-I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include -shared")
    c.env("LDFLAGS", "-L{{sysroot_lib}} -L{{install}} -L{{install}}/lib -shared")

    c.env("RENPY_ANDROID", "True")
    c.env("PYGAME_SDL2_ANDROID", "True")

    c.env("PYTHONPATH", "{{host}}/lib/{{pythonver}}/lib-dynload")
    c.env("_PYTHON_SYSCONFIGDATA_NAME", "_sysconfigdata__linux_")
    os.environ["_PYTHON_SYSCONFIGDATA_NAME"] = "_sysconfigdata__linux_"

    c.env("RENPY_STATIC", "True")

    if c.platform == "android":
        c.env("RENPY_DEPS_INSTALL", "{{sysroot_include}}::{{sysroot_lib}}::{{install}}::{{install}}/lib::{{install}}/include")
    else:
        c.env("RENPY_DEPS_INSTALL", "/usr::/usr/lib/x86_64-linux-gnu/")

    c.run("{{ hostpython }} setup.py build")

    print("RENPY GEN STATIC DONE")


@task(kind="python", always=True)
def build(c):
    print("RENPY BUILD")

    renpy_build_cflags = """"""
    renpy_build_cflags += """ -I{{ pygame_sdl2 }} """
    renpy_build_cflags += """ -I{{ pygame_sdl2 }}/src """
    renpy_build_cflags += """ -I{{ renpy }}/module """
    renpy_build_cflags += """ -I{{install}}/include/SDL2 """
    renpy_build_cflags += """ -I{{install}}/include/fribidi """
    renpy_build_cflags += """ -I{{install}}/include/freetype2 """
    renpy_build_cflags += """ -I{{sysroot_include}} -I{{install}}/include -I{{install}}/include/python3.9 """
    #renpy_build_cflags += """ -DCYTHON_PEP489_MULTI_PHASE_INIT=0 """

    c.env("CFLAGS", renpy_build_cflags)

    renpy_build_ldfags = """"""

    renpy_build_ldfags += """ -L{{sysroot_lib}} -L{{install}} -L{{install}}/lib """

    c.env("LDFLAGS", renpy_build_ldfags)

#    if c.python == "3":
#        gen = "gen3-static/"
#    else:
#        gen = "gen-static/"

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

    new_modules = []
    for module in modules:
        if "renpy" in module or "jnius" in module:
            splat_name = module.split(".")
            splat_name = splat_name[-1]
            module = splat_name
        new_modules.append(module)

    #static_objects = [ "IMG_savepng.c", "core.c", "subpixel.c"]
    static_objects = [ "core.c", "subpixel.c"] #IMG_savepng has duplicated SDL_image symbols

    FRIBIDI_SOURCES = """
    fribidi-src/lib/fribidi.c
    fribidi-src/lib/fribidi-arabic.c
    fribidi-src/lib/fribidi-bidi.c
    fribidi-src/lib/fribidi-bidi-types.c
    fribidi-src/lib/fribidi-deprecated.c
    fribidi-src/lib/fribidi-joining.c
    fribidi-src/lib/fribidi-joining-types.c
    fribidi-src/lib/fribidi-mem.c
    fribidi-src/lib/fribidi-mirroring.c
    fribidi-src/lib/fribidi-run.c
    fribidi-src/lib/fribidi-shape.c
    renpybidicore.c
    """.split()

    #static_objects += FRIBIDI_SOURCES #only for arabic
    static_objects += [ "renpysound_core.c", "ffmedia.c" ]
    static_objects += ["egl_none.c"]

    static_objects += [ "ftsupport.c", "ttgsubtable.c" ]

    for source in sources:

        object = str(source.name)[:-2] + ".o"
        objects.append(object)

        c.var("src", source)
        c.var("object", object)
        c.run("{{ CC }} {{ CFLAGS }} -c {{ src }} -o {{ object }}", verbose=True)

    for source in static_objects:
        source_path = c.renpy / "module" / source
        fribidi_include = c.renpy / "module" / "fribidi-src"
        build_path_object = c.renpy / "module" / "build" / "static_temp" / source
        build_path_base = build_path_object.parent

        source_path = str(source_path.absolute())
        build_path_object = str(build_path_object.absolute())
        build_path_base = str(build_path_base.absolute())
        fribidi_include = str(fribidi_include.absolute())

        if not os.path.exists(build_path_base):
            os.makedirs(build_path_base)

        object = build_path_object[:-2] + ".o"

        objects.append(object)

        if "fribidi" in source_path:    
            c.env("CFLAGS", renpy_build_cflags + """ -I""" + fribidi_include)


        c.var("src", source_path)
        c.var("object", object)
        c.run("{{ CC }} {{ CFLAGS }} -c {{ src }} -o {{ object }}", verbose=True)



    c.generate("{{ source }}/librenpy_inittab.c", "{{ tmp }}/inittab.c", modules=new_modules)
    c.run("{{ CC }} {{ CFLAGS }} -c {{ tmp }}/inittab.c -o {{ tmp }}/inittab.o", verbose=True)
    objects.append("{{ tmp }}/inittab.o")

    c.var("objects", " ".join(objects))

    c.run("{{ AR }} r librenpy.a {{ objects }} {{ tmp }}/inittab.o", verbose=True)
    c.run("{{ RANLIB }} librenpy.a", verbose=True)

    c.copy("librenpy.a", "{{ install }}/lib/librenpy.a")
