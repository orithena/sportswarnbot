#!/usr/bin/python
# - coding: utf-8 -

import os, codecs

_PRINT = True
_statefile = '/tmp/allemeineentchen.state'

def set(statefile, statefiledir='/tmp'):
    global _statefile
    _statefile = statefiledir + os.path.sep + statefile
    try:
        with codecs.open(_statefile, "a", "utf-8") as f:
            pass
    except Exception as e:
        if _PRINT: print(("Could not create statefile %s: %s" % (_statefile, e)))

def has(s):
    states = []
    try:
        with codecs.open(_statefile, "r", "utf-8") as f:
            states = [ l.strip() for l in f.readlines() ]
    except Exception as e:
        if _PRINT: print(("Could not read statefile %s: %s" % (_statefile, e)))
        return False
    return s.strip() in states
    
def save(s):
    try:
        with codecs.open(_statefile, "a", "utf-8") as f:
            f.write(s.strip() + "\n")
    except Exception as e:
        if _PRINT: print(("Could not write statefile %s: %s" % (_statefile, e)))
