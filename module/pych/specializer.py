"""
    The Specializer is responsible for loading up sourcecode,
    specializing code-templates to Externs and possibly other
    things down the road.
"""
import logging
import os

import numpy as np

TYPE2SOURCE = {
    "c": {
        None:       "void",
        bool:       "bool",
        int:        "int",
        long:       "long",
        float:      "double",
        str:        "char*",
        unicode:    "char*",
        np.ndarray: "py_ndarray*"
    },
    "chapel": {
        None:       "void",
        bool:       "bool",
        int:        "int",
        long:       "int(64)",
        float:      "real(64)",
        str:        "string",
        unicode:    "string",
        np.ndarray: "ndarray"
    }
}

def get_specializer(slang):

    if slang.lower() == "c":
        return CSpecializer
    elif slang.lower() == "chapel":
        return ChapelSpecializer
    else:
        return None

class BaseSpecializer(object):
    """The actual Specializer class handling eveyrhting."""

    def __init__(self, sourcecode_path):
        self.sourcecode_path = sourcecode_path
        self.sources = {}

    def load(self, filename):
        """
        Reads content of 'filename' into sources dict and returns the
        content.
        """
        if filename not in self.sources:
            path = "%s/%s" % (self.sourcecode_path, filename)
            self.sources[filename] = open(path).read()

        return self.sources[filename]

    def specialize(self, externs, prefix=True):
        raise Exception("Not implemented.")

class CSpecializer(BaseSpecializer):

    def __init__(self, sourcecode_path):
        super(CSpecializer, self).__init__(sourcecode_path)

    def specialize(self, externs, prefix=True):
        """Specialize the inline-c code-template to the given externs."""

        # Grab the "template"
        source = ""
        if prefix:
            source = self.load(os.sep.join(["inline.prefix.c"]))

        tmpl = self.load(os.sep.join(["inline.func.c"]))
        for extern in externs:

            # Create the function signature
            args = ["%s %s" % (TYPE2SOURCE["c"][atype], aname)
                for aname, atype in
                zip(extern.anames, extern.atypes)
            ]

            func_text = {
                "rtype":   TYPE2SOURCE["c"][extern.rtype],
                "args":    ", ".join(args),
                "ename":   extern.ename,
                "fbody":   extern.doc
            }
            source += tmpl % func_text

        return source

class ChapelSpecializer(BaseSpecializer):

    def __init__(self, sourcecode_path):
        super(ChapelSpecializer, self).__init__(sourcecode_path)

    def specialize(self, externs, prefix=True):
        """Specialize the inline-chapel code-template to the given externs."""

        # Grab the "template"
        source = ""
        if prefix:
            source = self.load(os.sep.join(["inline.prefix.chpl"]))

        tmpl = self.load(os.sep.join(["inline.func.chpl"]))
        for extern in externs:
            # Create the function signature
            args = ["%s: %s" % (aname, TYPE2SOURCE["chapel"][atype])
                for aname, atype in
                zip(extern.anames, extern.atypes)
            ]

            func_text = {
                "rtype":   TYPE2SOURCE["chapel"][extern.rtype],
                "args":    ", ".join(args),
                "ename":   extern.ename,
                "fbody":   extern.doc
            }
            source += tmpl % func_text

        return source

