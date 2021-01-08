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

    c.env("LDFLAGS", "{{LDFLAGS}} -shared -lz -lm")

    c.run("./configure {{ cross_config }} --shared={{install}}/lib --prefix={{install}}")
    c.run("{{ make }}")

    c.copy(".libs/sqlite3.o", ".libs/libsqlite3.so")

    c.run("make install")
