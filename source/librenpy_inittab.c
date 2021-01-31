#include "Python.h"

{% for name in modules %}
PyMODINIT_FUNC PyInit_{{ name.replace(".", "_") }} (void);
{% endfor %}

void init_librenpy(void) {

{% for name in modules %}
    PyImport_AppendInittab("{{ name }}", PyInit_{{ name.replace(".", "_") }});
{% endfor %}
    //PyImport_ExtendInittab(inittab);
}
