from renpybuild.model import task

version = "6.2"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/ncurses-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("ncurses-{{version}}")

    c.run("./configure {{ cross_config }} --without-ada --enable-widec --without-debug --without-cxx-binding --disable-stripping --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
