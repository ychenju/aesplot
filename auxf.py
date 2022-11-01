# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import filter as apfilter
from typing import Sequence, Tuple

def longfix(lon:float) -> float:
    '''
    Convert the longitude ranging [-180,180] to [0,360]
    '''
    if lon < 0:
        return 360.+lon
    else:
        return lon

def longfix2(lon:float) -> float:
    '''
    Convert the longitude ranging [0,360] to [-180,180]
    '''
    if lon >= 180:
        return lon-360.
    else:
        return lon

def samesign(x:float, y:float) -> bool:
    '''
    Return if the sign of 2 floats are the same
    '''
    return (np.sign(x)*np.sign(y)+1)/2.

def cp2d(attr:np.ndarray) -> np.ndarray:
    '''
    Copy a 2d np.ndarray
    '''
    if not isinstance(attr, np.ndarray):
        attr = np.array(attr)
    r = np.zeros(attr.shape)
    r[:,:] = attr[:,:]
    return r

def cp2dlist(attr:np.ndarray) -> np.ndarray:
    '''
    Copy a 2d list-like object. Slower than cp2d
    '''
    r = []
    for i in range(attr.shape[0]):
        r.append([])
        for j in range(attr.shape[1]):
            list.append(r[-1], attr[i,j])
    return np.array(r)

def isnantable(table:np.ndarray) -> bool:
    '''
    Return if a table is all of nan
    '''
    r = np.array(list(filter(apfilter.isnotnan, table.reshape(-1))))
    if len(r) > 0:
        return False
    else:
        return True

def hasnan(*tables:Tuple[np.ndarray]) -> bool:
    '''
    Return if a table has any nan value
    '''
    for table in tables:
        r = np.array(table).reshape(-1)
        for x in r:
            if np.isnan(x):
                return True
    return False

def dim(table:Sequence) -> int:
    '''
    Return the dimension of the given table
    '''
    _s = np.array(table).shape
    return len(_s)

def is1d(table:Sequence) -> bool:
    '''
    Return if the table is 1d
    '''
    return dim(table) == 1

def is2d(table:Sequence) -> bool:
    '''
    Return if the table is 2d
    '''
    return dim(table) == 2

def dist(coor1:tuple, coor2:tuple) -> float:
    '''
    Return the distance between 2 Cartesian coordinates in Eculidean plane
    '''
    return np.sqrt((coor2[0]-coor1[0])**2 + (coor2[1]-coor1[1])**2)