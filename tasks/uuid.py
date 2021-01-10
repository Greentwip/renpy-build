from renpybuild.model import task

version = "1.0.3"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/libuuid-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("libuuid-{{version}}")
    c.env("LDFLAGS", "{{LDFLAGS}} -shared -lz -lm")

    c.run("./configure {{ cross_config }}  --prefix={{install}}")
    c.run("{{ make }}")
    c.run("{{ make }} install")
