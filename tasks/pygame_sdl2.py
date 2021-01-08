from renpybuild.model import task, annotator
python_version = "3.9"


@annotator
def annotate(c):
    c.include("{{ install }}/include/{{ pythonver }}/pygame_sdl2")


@task(kind="host-python", always=True)
def gen_static(c):
    c.var("python_version", python_version)

    c.chdir("{{ pygame_sdl2 }}")
    c.env("PYGAME_SDL2_STATIC", "1")
    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")

    c.run("{{ hostpython }} setup.py generate")


@task(kind="python", always=True)
def install(c):
    c.var("python_version", python_version)

    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")

    exec_string = "{{ hostpython }} -s -m pip install --upgrade setuptools"
    
    c.run(exec_string)

    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install --single-version-externally-managed --record files.txt --no-extensions")
    c.run("{{ hostpython }} {{ pygame_sdl2 }}/setup.py install_headers")
