from renpybuild.model import task

version = "8.0"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/readline-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("readline-{{version}}")

    c.run("./configure {{ cross_config }} bash_cv_wcwidth_broken=yes --prefix={{install}}")
    c.run("{{ make }}")
    c.run("make install")
