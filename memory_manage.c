#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


static PyObject *method_rqmem(PyObject *self) {

    uint64_t amt_mem = 1048576;

    int *memory = NULL;

    while (!memory) {
        memory = malloc(amt_mem * sizeof(int));
        if (memory) break;
        else amt_mem = amt_mem / 2;
    }

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

    *addr = val;

    return PyLong_FromLong(val);
}

static PyObject *method_lwmem(PyObject *self, PyObject *args) {
    uint64_t *addr = 0;

    if(!PyArg_ParseTuple(args, "k", &addr)) {
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
    return PyModule_Create(&mmmodule);
}



int main() {
    FILE *fp = fopen("write.txt", "w");
    fputs("Real Python!", fp);
    fclose(fp);
    return 1;
}

