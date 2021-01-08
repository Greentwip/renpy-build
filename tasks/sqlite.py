from renpybuild.model import task

version = "3330000"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/sqlite-autoconf-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("sqlite-autoconf-{{version}}")

    c.run("./configure {{ configure_cross }} --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
