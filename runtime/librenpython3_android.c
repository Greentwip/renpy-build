#include "SDL.h"
#include "SDL_image.h"
#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <jni.h>
#include "android/log.h"
#include "jniwrapperstuff.h"

void init_librenpy(void);

/* Environment Handling *******************************************************/
extern char **environ;

/**
 * This is true if the environment is malfunctioning and we need to work
 * around that.
 */
static int environ_workaround = 0;


static void init_environ() {
    setenv("TEST_ENV_VAR", "The test worked.", 1);

    if (*environ) {
        return;
    }

    environ_workaround = 1;
    environ = calloc(50, sizeof(char *));
}

static void setenv_workaround(const char *c_variable, const char *c_value) {
    setenv(c_variable, c_value, 1);

    char buf[2048];
    char **e = environ;

    if (environ_workaround) {
        snprintf(buf, 2048, "%s=%s", c_variable, c_value);

        while (*e) {
            e++;
        }

        *e = strdup(buf);
    }
}

JNIEXPORT void JNICALL JAVA_EXPORT_NAME(PythonSDLActivity_nativeSetEnv) (
        JNIEnv*  env, jobject thiz,
        jstring variable,
        jstring value) {

    jboolean iscopy;
    const char *c_variable = (*env)->GetStringUTFChars(env, variable, &iscopy);
    const char *c_value  = (*env)->GetStringUTFChars(env, value, &iscopy);

    setenv_workaround(c_variable, c_value);
}

/* The Androidembed module ****************************************************/

SDL_Window *window = NULL;

#define LOG(x) __android_log_write(ANDROID_LOG_INFO, "python", (x))
#define LOGE(x) __android_log_write(ANDROID_LOG_ERROR, "pythonerror", (x))

static PyObject *androidembed_log(PyObject *self, PyObject *args) {
    char *logstr = NULL;
    if (!PyArg_ParseTuple(args, "s", &logstr)) {
        return NULL;
    }
    LOG(logstr);
    Py_RETURN_NONE;
}

static PyObject *androidembed_error_log(PyObject *self, PyObject *args) {
    char *logstr = NULL;
    if (!PyArg_ParseTuple(args, "s", &logstr)) {
        return NULL;
    }
    LOGE(logstr);
    Py_RETURN_NONE;
}

static PyObject *androidembed_close_window(PyObject *self, PyObject *args) {
    char *logstr = NULL;
    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }

    if (window) {
		SDL_DestroyWindow(window);
		window = NULL;
    }

    Py_RETURN_NONE;
}


static PyMethodDef AndroidEmbedMethods[] = {
	    {"log", androidembed_log, METH_VARARGS, "Log on android platform."},
	    {"error_log", androidembed_error_log, METH_VARARGS, "Log on android platform."},
	    {"close_window", androidembed_close_window, METH_VARARGS, "Close the initial window."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef renpythonModDef =
{
    PyModuleDef_HEAD_INIT,
    "androidembed", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    AndroidEmbedMethods
};


PyMODINIT_FUNC PyInit_androidembed(void) {
    return PyModule_Create(&renpythonModDef);
    //(void) Py_InitModule("androidembed", AndroidEmbedMethods);
}

/*static struct _inittab inittab[] = {
               { "androidembed",  PyInit_androidembed },
               { NULL, NULL },
};
*/
/* Python Startup *************************************************************/

int start_python(void) {
    char *private = getenv("ANDROID_PRIVATE");

    chdir(private);

    /* The / is required to stop python from doing a search that causes
     * a crash on ARC.
     */
    char python[2048];
    snprintf(python, 2048, "%s/python", private);

    
    //Py_SetPath(private);

    Py_SetProgramName(python);
    Py_SetPythonHome(private);

    char *args[] = { python, "main.py", NULL };

    Py_OptimizeFlag = 2;
    Py_IgnoreEnvironmentFlag = 1;
    Py_NoUserSiteDirectory = 1;

    /* Add a built-in module, before Py_Initialize */
    if (PyImport_AppendInittab("androidembed", PyInit_androidembed) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    init_librenpy();

    char python_zip[2048];
    snprintf(python_zip, 2048, "%s/python39.zip", private);

    char python_standard_libs[2048];
    snprintf(python_standard_libs, 2048, "%s/python39", private);


    char platlibdir[2048];
    snprintf(platlibdir, 2048, "%s/lib", private);


    /*setenv("PATH", private, 1);
    setenv("PYTHONPATH", python_path, 1);
    setenv("PREFIX", private, 1);
    setenv("EXEC_PREFIX", private, 1);
    setenv("VPATH", private, 1);
    setenv("PYTHONPLATLIBDIR", private, 1);
    */
    setenv("ANDROID_PATH", private, 1);
    setenv("ANDROID_PYTHONPATH", private, 1);
    setenv("ANDROID_PREFIX", private, 1);
    setenv("ANDROID_EXEC_PREFIX", private, 1);
    setenv("ANDROID_VPATH", private, 1);
    setenv("ANDROID_PYTHONPLATLIBDIR", platlibdir, 1);
    setenv("ANDROID_PYTHONPROGRAMNAME", python, 1);
    setenv("ANDROID_STANDARDLIBS_PATH", python_standard_libs, 1);
    //Py_SetPath(private);

    /*LOGE("PATH");
    LOGE(getenv("PATH"));
    LOGE("PYTHONPATH");
    LOGE(getenv("PYTHONPATH"));
    LOGE("PREFIX");
    LOGE(getenv("PREFIX"));
    LOGE("EXEC_PREFIX");
    LOGE(getenv("EXEC_PREFIX"));*/

    LOGE("INIT");
    Py_Initialize();

    LOGE("THREADS");
    PyEval_InitThreads();


    char python_command[2048];
    snprintf(python_command, 2048, "import sys\nsys.path.append(\"%s\")\n", python_zip);

    LOGE("SYS");
    PyRun_SimpleString(python_command);

    char print_command[2048];
    snprintf(print_command, 2048, "import androidembed\nandroidembed.error_log(\"%s\")", "sys.path");

    LOGE("PRINT");
    PyRun_SimpleString(print_command);

    PyEval_ReleaseThread(PyThreadState_Get());

    LOGE("All fine");
    
    //int result = Py_Main(2, args);


    //return result;

    return 0;
}


void call_prepare_python(void) {
	JNIEnv* env = (JNIEnv*) SDL_AndroidGetJNIEnv();
	jobject activity = (jobject) SDL_AndroidGetActivity();
	jclass clazz = (*env)->GetObjectClass(env, activity);
	jmethodID method_id = (*env)->GetMethodID(env, clazz, "preparePython", "()V");
	(*env)->CallVoidMethod(env, activity, method_id);
	(*env)->DeleteLocalRef(env, activity);
	(*env)->DeleteLocalRef(env, clazz);
}

int SDL_main(int argc, char **argv) {
	SDL_Surface *surface;
	SDL_RWops *rwops = NULL;
	SDL_Surface *presplash = NULL;
	SDL_Surface *presplash2 = NULL;
	SDL_Rect pos;
	SDL_Event event;

	Uint32 pixel;

	init_environ();
    setenv_workaround("RENPY_PLATFORM", PLATFORM "-" ARCH);
    SDL_SetHint(SDL_HINT_ANDROID_BLOCK_ON_PAUSE, "0");

	if (SDL_Init(SDL_INIT_EVERYTHING) < 0) {
	    return 1;
	}

	IMG_Init(IMG_INIT_JPG|IMG_INIT_PNG);

	window = SDL_CreateWindow("presplash", 0, 0, 0, 0, SDL_WINDOW_FULLSCREEN_DESKTOP| SDL_WINDOW_SHOWN);
	surface = SDL_GetWindowSurface(window);
	pixel = SDL_MapRGB(surface->format, 128, 128, 128);

	rwops = SDL_RWFromFile("android-presplash.png", "r");

	if (!rwops) {
		rwops = SDL_RWFromFile("android-presplash.jpg", "r");
	}

	if (!rwops) goto done;

	presplash = IMG_Load_RW(rwops, 1);

    if (!presplash) goto done;

	presplash2 = SDL_ConvertSurfaceFormat(presplash, SDL_PIXELFORMAT_RGB888, 0);
	Uint8 *pp = (Uint8 *) presplash2->pixels;

#if SDL_BYTEORDER == SDL_LIL_ENDIAN
	pixel = SDL_MapRGBA(surface->format, pp[2], pp[1], pp[0], 255);
#else
	pixel = SDL_MapRGBA(surface->format, pp[0], pp[1], pp[2], 255);
#endif

	SDL_FreeSurface(presplash2);

done:

    {
        Uint32 start = SDL_GetTicks();

        while (SDL_GetTicks() < start + 520) {
            surface = SDL_GetWindowSurface(window);

            SDL_FillRect(surface, NULL, pixel);

            if (presplash) {
                pos.x = (surface->w - presplash->w) / 2;
                pos.y = (surface->h - presplash->h) / 2;
                SDL_BlitSurface(presplash, NULL, surface, &pos);
                SDL_UpdateWindowSurface(window);
            }

            SDL_WaitEventTimeout(&event, 10);
        }
    }

    SDL_GL_MakeCurrent(NULL, NULL);

    if (presplash) {
        SDL_FreeSurface(presplash);
    }

	call_prepare_python();

	return start_python();
}
