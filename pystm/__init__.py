'''
pystm
=====

Cheap, currently non-threadsafe transactional memory object dictionary.

See also:

  https://docs.python.org/3/reference/datamodel.html#emulating-container-types

'''

import numpy as np

class STM(object):

    _copy_map = {
        type(bool()) : bool,
        type(int()): int,
        type(float()): float,
        type(str()): str,
        type(list()): list,
        np.ndarray: np.array,
        type(type): type
    }

    def __init__(self):
        self._frames = []
        self._vals = {}

    def _copy(self, obj):
        return self._copy_map[type(obj)](obj)

    def __len__(self):
        return len(self._vals)

    def __getitem__(self, key):
        return self._vals[key]

    def __setitem__(self, key, value):
        new = self._copy(value)
        self._frames.append({**self._vals, key: value})
        self._vals[key] = new
        return new

    def __delitem__(self, key):
        self._frames.append({k: dct[k] for k in self._vals if k != key})
        del self._vals[key]

    def __missing__(self, key):
        return self._vals.__missing__(key)

    def __iter__(self):
        return self._vals.__iter__()

    def __reversed__(self):
        return reversed(self._vals.__iter__())  # TypeError

    def __contains__(self, item):
        return item in self._vals

    def keys(self):
        return self._vals.keys()

    def values(self):
        return self._vals.values()

    def items(self):
        return self._vals.items()

    def history(self, key=None):
        if key:
            return [i.get(key, None) for i in self._frames]
        else:
            return self._frames
