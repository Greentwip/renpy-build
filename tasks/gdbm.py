from renpybuild.model import task

version = "1.18.1"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/gdbm-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("gdbm-{{version}}")

    c.env("CFLAGS", "-fcommon")
    
    c.run("./configure {{ cross_config }} --enable-libgdbm-compat --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
