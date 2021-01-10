from renpybuild.model import task

version = "1.0.8"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/bzip2-{{version}}.tar.gz")

    c.chdir("bzip2-{{version}}")
    c.patch("bzip2-no-tests.diff")


@task()
def build(c):
    c.var("version", version)
    c.chdir("bzip2-{{version}}")

    c.run("""{{ make }} AR="{{ AR }}" RANLIB="{{ RANLIB }}" CC="{{ CC }}" CFLAGS="{{ CFLAGS }} -D_FILE_OFFSET_BITS=64" """)
    c.run("""touch bzip2 bunzip2 bzip2recover bzgrep bzmore bzdiff""")


    c.run("""make -f Makefile-libbz2_so PREFIX="{{ install }}" AR="{{ AR }}" RANLIB="{{ RANLIB }}" CC="{{ CC }}" CFLAGS="{{ CFLAGS }} -D_FILE_OFFSET_BITS=64" """)
    c.run("""make install PREFIX="{{ install }}" AR="{{ AR }}" RANLIB="{{ RANLIB }}" CC="{{ CC }}" CFLAGS="{{ CFLAGS }} -D_FILE_OFFSET_BITS=64" """)

