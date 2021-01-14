from renpybuild.model import task

version = "3.9.0"


@task(kind="host", pythons="3")
def unpack_hostpython(c):
    c.clean()

    c.var("version", version)
    c.run("tar xvf {{source}}/Python-{{version}}.tgz")

    c.chdir("Python-{{ version }}")


@task(kind="host", pythons="3")
def build_host(c):
    c.var("version", version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "-DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H ")
    c.env("CFLAGS", "{{CFLAGS}} -I/usr/local/opt/openssl/include")
    c.env("LDFLAGS", " -L/usr/local/opt/openssl/lib ")
    c.run("""./configure --prefix="{{ host }}" --enable-ipv6""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup")
    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup.Local")

    c.run("""
    export OPENSSL_INCLUDE="-I/usr/local/opt/openssl/include" &&
    export OPENSSL_LD="-L/usr/local/opt/openssl/lib" &&
    export OPENSSL_LIB="-lssl -lcrypto" &&
    export HAVE_X509_VERIFY_PARAM_SET1_HOST="True" &&
    {{make}} 
    """)
    #c.run("""{{ make }}""")
    quit()
    c.run("""{{ make }} install""")
