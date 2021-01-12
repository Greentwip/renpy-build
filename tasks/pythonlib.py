from renpybuild.model import task
import os

import shutil
python_version = "3.9"

def pyo_copy(src, dst):
    """
    Copies the pyo and pem files from `src` to `dst`.

    `src` and `dst` may be either directories or files.
    """

    if src.is_dir():
        for i in src.iterdir():
            pyo_copy(i, dst / i.name)
        return

    if not (str(src).endswith(".pyo") or str(src).endswith(".pem")):
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def copytree(c, from_path, to_path):
    recursive_overwrite(c.expand(from_path), c.expand(to_path))


@task(kind="host-python", pythons="3", always=True)
def python3(c):
    c.var("python_version", python_version)
    c.env("PYTHONPATH", "{{host}}/lib/python{{python_version}}/lib-dynload")

    search = [
        c.path("{{ install }}/lib/{{ pythonver }}"),
        c.path("{{ install }}/lib/{{ pythonver }}/site-packages"),
        c.path("{{ pytmp }}/pyjnius"),
        c.path("{{ pytmp }}/pyobjus"),
        ]

    dist = c.path("{{ distlib }}/{{ pythonver }}")

    c.clean("{{ distlib }}/{{ pythonver }}")

    #os.makedirs("{{ install }}/dist/{{ pythonver }}/compiled")

    #compile_string = " {{ hostpython }} -OO -m compileall "
    #compile_string = compile_string + " -d {{ install }}/dist/{{ pythonver }}/compiled "
    #compile_string = compile_string + " {{ install }}/lib/{{ pythonver }}/site-packages " 
    

 #   c.run(compile_string)


#   for i in PYTHON27_MODULES.split():

#        for d in search:
#            src = d / i
#            if src.exists():
#                break
#        else:
#            raise Exception(f"Can't find {i}.")#

#        dst = dist / i
#        pyo_copy(src, dst)
#        shutil.rmtree(to_path)

    copytree(c, "{{ install }}/lib/{{ pythonver }}/", "{{distlib}}/{{pythonver}}")
    copytree(c, "{{ install }}/lib/{{ pythonver }}/site-packages", "{{distlib}}/{{pythonver}}")

    c.copy("{{ runtime }}/site.py", "{{ distlib }}/{{ pythonver }}/site.py")
    #c.run("{{ hostpython }} -OO -m compileall {{ distlib }}/{{ pythonver }}/site.py")

    c.run("mkdir -p {{ distlib }}/{{ pythonver }}/lib-dynload")
    with open(c.path("{{ distlib }}/{{ pythonver }}/lib-dynload/empty.txt"), "w") as f:
        f.write("lib-dynload needs to exist to stop an exec_prefix error.\n")

