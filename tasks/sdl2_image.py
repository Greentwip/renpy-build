from renpybuild.model import task

version = "2.0.5"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/SDL2_image-{{version}}.tar.gz")


@task()
def build(c):
    c.var("version", version)
    c.chdir("SDL2_image-{{version}}")

    c.env("CFLAGS", "-I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include")
    c.env("LDFLAGS", "-L{{sysroot_lib}} -L{{install}} -L{{install}}/lib -lSDL2")
    c.env("CFLAGS", "{{CFLAGS}} -DANDROID")
    c.env("CFLAGS", "{{CFLAGS}} -D__ANDROID__")
    c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED")

    if c.platform == "windows":
        c.env("ac_cv_lib_jpeg_jpeg_CreateDecompress", "yes")

    c.run("""./configure {{ cross_config }} --prefix="{{ install }}" --disable-sdltest --disable-tif --disable-imageio --enable-webp --disable-xcf --disable-svg """)
    #c.run("""./configure --help """)

    
    c.run("""{{ make }}""")
    c.run("""{{ make }} install""")

