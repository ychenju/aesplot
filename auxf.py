# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from . import filter as apfilter
from typing import Sequence, Tuple

def longfix(lon:float) -> float:
    if lon < 0:
        return 360.+lon
    else:
        return lon

def samesign(x:float, y:float) -> bool:
    return (np.sign(x)*np.sign(y)+1)/2.

def cp2d(attr:np.ndarray) -> np.ndarray:
    r = []
    for i in range(attr.shape[0]):
        r.append([])
        for j in range(attr.shape[1]):
            list.append(r[-1], attr[i,j])
    return np.array(r)

def isnantable(table:np.ndarray) -> bool:
    r = np.array(list(filter(apfilter.isnotnan, table.reshape(-1))))
    if len(r) > 0:
        return False
    else:
        return True

def hasnan(*tables:Tuple[np.ndarray]) -> bool:
    for table in tables:
        r = np.array(table).reshape(-1)
        for x in r:
            if np.isnan(x):
                return True
    return False

def dim(table:Sequence) -> int:
    _s = np.array(table).shape
    return len(_s)

def is1d(table:Sequence) -> bool:
    return dim(table) == 1

def is2d(table:Sequence) -> bool:
    return dim(table) == 2