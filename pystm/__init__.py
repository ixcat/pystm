'''
pystm
=====

Cheap, currently non-threadsafe transactional memory object dictionary.

See also:

  https://docs.python.org/3/reference/datamodel.html#emulating-container-types

'''


class STM(object):

    absent = None

    class Absent(object):
        def __repr__(self):
            return 'STM.Absent'

    def __init__(self):
        if STM.absent is None:
            STM.absent = STM.Absent()

        self._frames = []
        self._vals = {}

    def _copy(self, obj):
        return {
            type(type):
                lambda v:
                    v if not isinstance(type(v), type(None))
                    else None
        }[type(type(obj))](obj)

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
        self._frames.append({k: self._vals[k] for k in self._vals if k != key})
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
        '''
        return full history or history for one key
        TODO: return key-like history for N keys if requested
        '''
        if key:
            return [i.get(key, STM.absent) for i in self._frames]
        else:
            return self._frames

    def push(self, dct, interested, extra=[]):
        '''
        Assign (and thus save) keys from dct which we are interested in

        Intended as an alternate use case from direct use -
        e.g. rather than using STM directly, use to trace history::

            >>> m = STM()
            >>> v = 1
            >>> interested = ['v']
            >>> m.push(locals(), interested)

        '''

        new = {**self._vals, **{k: self._copy(dct[k]) for k in dct
                                if k in interested}}
        for e in extra:
            new[e[0]] = e[1]

        self._frames.append(dict(new))
        self._vals = new
