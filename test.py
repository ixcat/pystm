#! /usr/bin/env python

'''
test module for pystm
'''

from collections import OrderedDict

from code import interact

import numpy as np

from pystm import STM

def test_one():
    print('test_one')
    stm = STM()
    v = True
    stm['foo'] = v

    stm['foo'] = 'baz'
    print(stm.history('foo'))

    del stm['foo']
    print(stm.history('foo'))

    stm['foo'] = None
    print(stm.history('foo'))

    stm['foo'] = [1, 2]
    print(stm.history('foo'))

    stm['foo'] = OrderedDict([tuple(stm['foo'])])
    print(stm.history('foo'))

    return stm


def test_two():
    print('test_two')
    stm = STM()

    a = stm['a'] = np.array(((10,) * 10), np.int64)
    stm['a'] = stm['a'] + 5
    a = stm['a']
    del stm['a']
    stm['a'] = a * 5

    print(stm.history('a'))

    return stm


def test_push():
    print('test_three')

    stm = STM()
    interested = ['x']
    x = 1

    stm.push(locals(), interested)
    print(stm.history())
    x = 2

    stm.push(locals(), interested)
    print(stm.history())


if __name__ == '__main__':
    t1 = test_one()
    t2 = test_two()
    t_push = test_push()
    interact('stm', local=globals())
