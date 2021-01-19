from renpybuild.model import task


@task(kind="python", always=True)
def build(c):
    renpy_args = """
    {{ CC }} {{ CFLAGS }} -DANDROID -D__ANDROID__

    -c -o {{tmp}}/libmemfd_create.o

    {{source}}/memfd_create.c
    """

    renpy_args = renpy_args.replace("\n", "")
    c.run(renpy_args)

    c.run("{{ AR }} r {{install}}/lib/libmemfd_create.a {{tmp}}/libmemfd_create.o", verbose=True)
    c.run("{{ RANLIB }} {{install}}/lib/libmemfd_create.a", verbose=True)


    


