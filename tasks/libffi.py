from renpybuild.model import task

version = "3.3"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/libffi-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("libffi-{{version}}")

    c.run("""./autogen.sh""")
    c.run("""autoreconf -vif""")

    c.env("CFLAGS", " -static ")
    c.env("LDFLAGS", " -static ")

    c.run("""./configure --disable-builddir --disable-shared --enable-static {{ ffi_cross_config }} --prefix="{{ install }}" """)
    
    c.run("""{{ make }}""")
    c.run("""make install """)
