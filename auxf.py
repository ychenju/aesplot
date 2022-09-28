# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import filter as apfilter

def longfix(lon: float):
    if lon < 0:
        return 360.+lon
    else:
        return lon

def samesign(x, y):
    return (np.sign(x)*np.sign(y)+1)/2.

def cp2d(attr: np.ndarray):
    r = []
    for i in range(attr.shape[0]):
        r.append([])
        for j in range(attr.shape[1]):
            r[-1].append(attr[i,j])
    return np.array(r)

def isnantable(table: np.ndarray):
    r = np.array(list(filter(apfilter.isnotnan, table.reshape(-1))))
    if len(r) > 0:
        return False
    else:
        return True