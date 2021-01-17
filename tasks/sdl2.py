from renpybuild.model import task, annotator
import shutil

version = "2.0.14"


@annotator
def annotate(c):
    c.include("{{ install }}/include/SDL2")


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/SDL2-{{version}}.tar.gz")

    if c.platform == "ios":
        c.chdir("SDL2-{{version}}")
        c.patch("sdl2-ios-configure.diff")
        c.run("./autogen.sh")


@task()
def build(c):
    c.var("version", version)
    c.chdir("SDL2-{{version}}")

    if c.platform == "ios":
        c.env("CFLAGS", "{{ CFLAGS }} -fobjc-arc")

    c.env("ac_cv_header_libunwind_h", "no")
    c.env("CFLAGS", "-I{{sysroot_include}} -I{{sysroot_lib}} -I{{install}}/include")
    c.env("LDFLAGS", "-L{{sysroot_lib}} -L{{install}} -L{{install}}/lib ")
    c.env("CFLAGS", "{{CFLAGS}} -DANDROID")
    c.env("CFLAGS", "{{CFLAGS}} -D__ANDROID__")
    c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED")

    config_string = """
    ./configure {{ cross_config }} 
    --prefix="{{ install }}"
    --disable-wasapi
    --disable-render-metal
    --disable-jack
{% if c.platform == "android" %}
    --disable-video-opengles
    --enable-video-opengles2
    --disable-video-wayland
    --disable-video-x11
    --disable-oss
    --disable-alsa
    --disable-esd
    --disable-pulseaudio
    --disable-arts
    --disable-nas
    --disable-sndio
    --disable-fusionsound
{% endif %}
    """

    config_string = config_string.replace("\n", "")
    c.run(config_string)

    c.run("""{{ make }}""")
    c.run("""{{ make }} install""")
    #quit()

@task(kind="arch-python", platforms="android", always=True)
def rapt(c):
    c.var("version", version)
    c.chdir("SDL2-{{version}}")

    c.run("""{{ CXX }} -std=c++11 -shared -o libhidapi.so src/hidapi/android/hid.cpp -llog""")
    c.run("""{{ STRIP }} --strip-unneeded libhidapi.so""")

    c.run("""install -d {{ jniLibs }}""")
    c.run("""install libhidapi.so {{ jniLibs }}""")
    c.run("""install {{ cross }}/android-ndk-r22/sources/cxx-stl/llvm-libc++/libs/{{ jni_arch }}/libc++_shared.so {{ jniLibs }}""")

    c.copytree("android-project/app/src/main/java/org/libsdl", "{{ raptver }}/prototype/renpyandroid/src/main/java/org/libsdl")
    c.copytree("android-project/app/src/main/java/org/libsdl", "{{ raptver }}/project/renpyandroid/src/main/java/org/libsdl")
