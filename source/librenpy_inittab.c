#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void TABLOG(char* string){
    char msg2[200000];
    char* mblog = "\nMBLOG: ";

    for(int i = 0; i<200000; ++i){
        msg2[i] = '\0';
    }

    /*size_t max_bytes_string = strlen(string);
    size_t max_bytes_text = strlen(mblog);*/
    snprintf(msg2, 200000, "%s%s", mblog, string); 
    FILE *file = fopen("inittab.log", "a"); 
    fprintf(file, "%s", msg2); 
    fclose(file); 
}

{% for name in modules %}
PyMODINIT_FUNC PyInit_{{ name.replace(".", "_") }} (void);
{% endfor %}

static struct _inittab inittab[]  = {
{% for name in modules %}
    { "{{ name }}", PyInit_{{ name.replace(".", "_") }} },
{% endfor %}
    { NULL, NULL },
};

void init_librenpy(void) {
    PyImport_ExtendInittab(inittab);
}

