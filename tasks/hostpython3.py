from renpybuild.model import task

version = "3.8.7"


@task(kind="host", pythons="3")
def unpack_hostpython(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/Python-{{version}}.tgz")

    c.chdir("Python-{{ version }}")


@task(kind="host", pythons="3")
def build_host(c):
    c.var("version", version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "{{ CFLAGS }} -DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H ")

    c.run("""./configure --prefix="{{ host }}" --enable-ipv6""")

    c.generate("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup.local")

    c.run("""{{ make }} install""")
