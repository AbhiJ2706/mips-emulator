#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>


static struct State {
    int *mem_addr;
    uint64_t size;
};

static PyObject *UnalignedAccessError = NULL;
static PyObject *OutOfBoundsError = NULL;
static struct State *ps = NULL;

static PyObject *method_rqmem(PyObject *self) {

    uint64_t amt_mem = 1048576;

    int *memory = NULL;

    while (!memory) {
        memory = malloc(amt_mem * sizeof(int));
        if (memory) break;
        else amt_mem = amt_mem / 2;
    }

    ps->mem_addr = memory;
    ps->size = amt_mem;

    PyObject* py = PyTuple_New(2);

    PyTuple_SET_ITEM(py, 0, Py_BuildValue("k", memory));
    PyTuple_SET_ITEM(py, 1, Py_BuildValue("k", amt_mem));

    return py;
}

static PyObject *method_swmem(PyObject *self, PyObject *args) {
    uint64_t *addr = 0;
    int val = 0;

    if(!PyArg_ParseTuple(args, "ki", &addr, &val)) {
        return NULL;
    }
    if ((uint64_t) addr % 4 != 0) {
        char *exc_str = malloc(100 * sizeof(char));
        sprintf(exc_str, "Unaligned access- addresses must be multiples of 4. Address accessed: %" PRIu64, (uint64_t) addr);
        PyErr_SetString(UnalignedAccessError, exc_str);
        return NULL;
    } else if ((uint64_t) addr < (uint64_t) ps->mem_addr || (uint64_t) addr >= (uint64_t) (ps->mem_addr + ps->size)) {
        char *exc_str = malloc(175 * sizeof(char));
        sprintf(exc_str, "Out of bounds- addresses must be within the bounds to the arena. Address: %" PRIu64 ", Bounds: %" PRIu64 " %" PRIu64, (uint64_t) addr, (uint64_t) ps->mem_addr, (uint64_t) ps->mem_addr + ps->size);
        PyErr_SetString(OutOfBoundsError, exc_str);
        return NULL;
    }

    *addr = val;

    return PyLong_FromLong(val);
}

static PyObject *method_lwmem(PyObject *self, PyObject *args) {
    uint64_t *addr = 0;

    if(!PyArg_ParseTuple(args, "k", &addr)) {
        return NULL;
    }
    if ((uint64_t) addr % 4 != 0) {
        char *exc_str = malloc(100 * sizeof(char));
        sprintf(exc_str, "Unaligned access- addresses must be multiples of 4. Address accessed: %" PRIu64, (uint64_t) addr);
        PyErr_SetString(UnalignedAccessError, exc_str);
        return NULL;
    } else if ((uint64_t) addr < (uint64_t) ps->mem_addr || (uint64_t) addr >= (uint64_t) (ps->mem_addr + ps->size)) {
        char *exc_str = malloc(175 * sizeof(char));
        sprintf(exc_str, "Out of bounds- addresses must be within the bounds to the arena. Address: %" PRIu64 ", Bounds: %" PRIu64 " %" PRIu64, (uint64_t) addr, (uint64_t) ps->mem_addr, (uint64_t) ps->mem_addr + ps->size);
        PyErr_SetString(OutOfBoundsError, exc_str);
        return NULL;
    }

    return PyLong_FromLong(*addr);
}

static PyObject *method_fmem(PyObject *self, PyObject *args) {
    uint64_t *addr = 0;

    if(!PyArg_ParseTuple(args, "k", &addr)) {
        return NULL;
    }

    free(addr);

    return PyLong_FromLong(1);
}

static PyMethodDef MMMethods[] = {
    {"rqmem", method_rqmem, METH_VARARGS, "Python interface to request space for the stack"},
    {"lwmem", method_lwmem, METH_VARARGS, "Python interface to load a value from the stack"},
    {"swmem", method_swmem, METH_VARARGS, "Python interface to save a value to the stack"},
    {"fmem", method_fmem, METH_VARARGS, "Python interface to free the stack"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef mmmodule = {
    PyModuleDef_HEAD_INIT,
    "stackmem",
    "Python interface for stack memory interfacing",
    -1,
    MMMethods
};

PyMODINIT_FUNC PyInit_stackmem(void) {
    PyObject *module = PyModule_Create(&mmmodule);

    UnalignedAccessError = PyErr_NewException("stackmem.UnalignedAccessError", NULL, NULL);
    PyModule_AddObject(module, "UnalignedAccessError", UnalignedAccessError);
    OutOfBoundsError = PyErr_NewException("stackmem.OutOfBoundsError", NULL, NULL);
    PyModule_AddObject(module, "UnalignedAccessError", OutOfBoundsError);

    ps = malloc(sizeof(struct State));
    ps->mem_addr = NULL;
    ps->size = 0;

    return module;
}



int main() {
    FILE *fp = fopen("write.txt", "w");
    fputs("Real Python!", fp);
    fclose(fp);
    return 1;
}

