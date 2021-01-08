from renpybuild.model import task

version = "2.36"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/util-linux-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("util-linux-{{version}}")

    c.env("LDFLAGS", "{{LDFLAGS}} -shared")
    c.run("./configure {{ cross_config }} --shared={{install}}/lib --disable-all-programs --enable-libuuid --prefix={{install}}")
    c.run("{{ make }}")

    c.copy(".libs/libcommon.o", ".libs/libcommon.so")
    c.copy(".libs/libtcolors.o", ".libs/libtcolors.so")
    c.copy(".libs/libuuid.o", ".libs/libuuid.so")

    c.run("make install")
