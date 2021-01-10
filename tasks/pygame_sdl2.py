from renpybuild.model import task, annotator
python_version = "3.9"
import os

@annotator
def annotate(c):
    c.include("{{ install }}/include/{{ pythonver }}/pygame_sdl2")


@task(kind="python", pythons="3", platforms="android", always=True)
def gen_static(c):
    c.var("python_version", python_version)

    c.chdir("{{ pygame_sdl2 }}")
    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")
    c.env("_PYTHON_SYSCONFIGDATA_NAME", "_sysconfigdata__linux_")
    c.env("CFLAGS", "{{CFLAGS}} -I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include -shared")
    c.env("LDFLAGS", "{{LDFLAGS}} -shared -L{{sysroot_lib}} -L{{install}} -L{{install}}/lib")

    os.environ['_PYTHON_SYSCONFIGDATA_NAME'] = '_sysconfigdata__linux_'
 
    c.run("{{ host }}/bin/python3 setup.py generate")


@task(kind="python", pythons="3", platforms="android", always=True)
def install(c):
    c.var("python_version", python_version)

    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")

    exec_string = "{{ hostpython }} -s -m ensurepip"
    c.run(exec_string)
    exec_string = "{{ hostpython }} -s -m pip install --upgrade setuptools"

    c.run(exec_string)

    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install --single-version-externally-managed --record files.txt --no-extensions")
    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install_headers")
