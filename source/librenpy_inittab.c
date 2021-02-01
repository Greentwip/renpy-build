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

void init_librenpy(void) {
    TABLOG("inittab initializaiton");

{% for name in modules %}
    /*if(PyImport_AppendInittab("{{ name }}", PyInit_{{ name.replace(".", "_") }} == -1){
        TABLOG("Error: could not extend in-built modules table");
    }*/

    PyInit_{{ name.replace(".", "_") }}();
{% endfor %}

    TABLOG("inittab end");
    //PyImport_ExtendInittab(inittab);
}
