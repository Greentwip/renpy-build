from renpybuild.model import task
import shutil
import time
import os


@task(kind="platform-python", platforms="android", always=True)
def copy(c):

    if c.path("{{ raptver }}/prototype/local.properties").exists():
        c.copy("{{ raptver }}/prototype/local.properties", "{{tmp}}/local.properties")

    if c.path("{{ raptver }}/Sdk").exists():
        c.copytree("{{ raptver }}/Sdk", "{{tmp}}/Sdk")

    c.copytree("{{ root }}/rapt", "{{ raptver }}")

    if c.path("{{tmp}}/local.properties").exists():
        c.copy("{{tmp}}/local.properties", "{{ raptver }}/prototype/local.properties")    

    if c.path("{{tmp}}/Sdk").exists():
        c.copytree("{{tmp}}/Sdk", "{{ raptver }}/Sdk")    

    with open(c.path("{{ raptver }}/prototype/build.txt"), "w") as f:
        f.write(time.ctime())

    try:
        shutil.rmtree(c.path("{{ raptver }}/prototype/renpyandroid/src/main/java/org/libsdl"))
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(c.path("{{ raptver }}/prototype/renpyandroid/src/main/java/org/jnius"))
    except FileNotFoundError:
        pass

    os.unlink(c.path("{{ raptver }}/prototype/app/build.gradle"))
    os.unlink(c.path("{{ raptver }}/prototype/app/src/main/AndroidManifest.xml"))
    os.unlink(c.path("{{ raptver }}/prototype/app/src/main/res/values/strings.xml"))
    os.unlink(c.path("{{ raptver }}/prototype/renpyandroid/src/main/AndroidManifest.xml"))
    os.unlink(c.path("{{ raptver }}/prototype/renpyandroid/src/main/res/values/strings.xml"))
    os.unlink(c.path("{{ raptver }}/prototype/renpyandroid/src/main/java/org/renpy/android/Constants.java"))

    #if c.path("{{ raptver }}/prototype/local.properties").exists():
    #    os.unlink(c.path("{{ raptver }}/prototype/local.properties"))

    #c.rmtree("{{ raptver }}/prototype/app/src/main/res/mipmap-mdpi")
    #c.rmtree("{{ raptver }}/prototype/app/src/main/res/mipmap-hdpi")
    #c.rmtree("{{ raptver }}/prototype/app/src/main/res/mipmap-xhdpi")
    #c.rmtree("{{ raptver }}/prototype/app/src/main/res/mipmap-xxhdpi")
    #c.rmtree("{{ raptver }}/prototype/app/src/main/res/mipmap-xxxhdpi")

    c.rmtree("{{ raptver }}/prototype/renpyandroid/build/")
    c.rmtree("{{ raptver }}/prototype/app/build/")

    target = c.get_var("{{jniLibs}}")

    if not os.path.exists(target):
        os.makedirs(target)


    c.copy("{{install}}/lib/libavfilter.so", "{{ jniLibs }}/libavfilter.so")
    c.copy("{{install}}/lib/libavformat.so", "{{ jniLibs }}/libavformat.so")
    c.copy("{{install}}/lib/libavcodec.so", "{{ jniLibs }}/libavcodec.so")
    c.copy("{{install}}/lib/libavresample.so", "{{ jniLibs }}/libavresample.so")
    c.copy("{{install}}/lib/libswresample.so", "{{ jniLibs }}/libswresample.so")
    c.copy("{{install}}/lib/libswscale.so", "{{ jniLibs }}/libswscale.so")
    c.copy("{{install}}/lib/libavutil.so", "{{ jniLibs }}/libavutil.so")



@task(kind="host-python", always=True)
def android_module(c):
    c.run("""install -d {{ install }}/lib/{{ pythonver }}/site-packages/android""")
    c.run("""install {{ runtime }}/android/__init__.py {{ install }}/lib/{{ pythonver }}/site-packages/android""")
    c.run("""install {{ runtime }}/android/apk.py {{ install }}/lib/{{ pythonver }}/site-packages/android""")
