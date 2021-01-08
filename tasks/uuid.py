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

    c.run("./configure {{ configure_cross }} --disable-all-programs --enable-libuuid --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
