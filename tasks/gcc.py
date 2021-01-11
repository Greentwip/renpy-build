from renpybuild.model import task
import zipfile

binutils_version = "2.33.1"
gcc_version = "9.2.0"
ndk_version = "22"

@task(kind="host", platforms="mac")
def unpack(c):
    c.clean()

    c.var("binutils_version", binutils_version)
    c.var("gcc_version", gcc_version)

    c.run("tar xvf {{ tars }}/binutils-{{ binutils_version }}.tar.gz")
    c.run("tar xvf {{ tars }}/gcc-{{ gcc_version }}.tar.gz")


@task(kind="host", platforms="mac")
def build(c):
    c.var("binutils_version", binutils_version)
    c.var("gcc_version", gcc_version)

    if c.path("{{ install }}/bin/{{ host_platform }}-gcc").exists():
        return
        
    c.chdir("binutils-{{ binutils_version }}")

    c.run("./configure --prefix={{ install }}")
    c.run("{{ make }}")
    c.run("make install")

    c.chdir("{{ build }}")

    c.path("{{ build }}/gcc-{{ gcc_version }}/build").mkdir()
    c.chdir("{{ build }}/gcc-{{ gcc_version }}/build")

    c.run("""
    ../configure
    --prefix={{ install }}/
    --enable-languages=c,c++
    --with-multiarch
    --disable-multilib
    --disable-bootstrap

    """, verbose=True)

    c.run("{{ make }}")
    c.run("make install")

