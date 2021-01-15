from renpybuild.model import task, annotator
import os

@annotator
def annotate(c):
    c.include("{{ install }}/include/{{ pythonver }}/pygame_sdl2")


@task(kind="python", pythons="3", platforms="android", always=True)
def gen_static(c):

    c.chdir("{{ pygame_sdl2 }}")
    c.env("PYTHONPATH", "{{host}}/lib/{{pythonver}}/lib-dynload")
    c.env("_PYTHON_SYSCONFIGDATA_NAME", "_sysconfigdata__linux_")
    c.env("CFLAGS", "{{CFLAGS}} -I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include")
    c.env("LDFLAGS", "{{LDFLAGS}} -L{{sysroot_lib}} -L{{install}} -L{{install}}/lib")
    c.env("PYGAME_SDL2_STATIC", "True")
    os.environ['_PYTHON_SYSCONFIGDATA_NAME'] = '_sysconfigdata__linux_'
    c.run("{{ host }}/bin/python3 setup.py generate")


@task(kind="python", pythons="3", platforms="android", always=True)
def install(c):
    c.env("PYTHONPATH", "{{host}}/lib/{{pythonver}}/lib-dynload")

    exec_string = "{{ hostpython }} -s -m ensurepip"
    c.run(exec_string)
    exec_string = "{{ hostpython }} -s -m pip install --upgrade setuptools"

    c.run(exec_string)

    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install --single-version-externally-managed --record files.txt --no-extensions")
    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install_headers")
