from renpybuild.model import task

version = "5.2.5"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar -xzf {{source}}/xz-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("xz-{{version}}")
    c.env("LDFLAGS", "{{LDFLAGS}} -shared -lz -lm")

    c.run("./configure {{ cross_config }} --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
