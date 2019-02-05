#! /usr/bin/env python

'''
test module for pystm
'''


from code import interact

import numpy as np

from pystm import STM

def test_one():
    stm = STM()
    v = True
    stm['foo'] = v
    
    stm['foo'] = 'baz'
    print(stm.history('foo'))

    del stm['foo']
    print(stm.history('foo'))

    stm['foo'] = None
    print(stm.history('foo'))

    stm['foo'] = [1,2]

    print(stm.history('foo'))
    return stm

def test_two():
    stm = STM()
    
    a = stm['a'] = np.array(((10,) * 10), np.int64)
    a = stm['a'] = stm['a'] + 5
    stm['a'] *= 5

    return stm


if __name__ == '__main__':
    t1 = test_one()
    t2 = test_two()
    interact('stm', local=globals())
