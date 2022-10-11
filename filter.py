# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import auxf as aux
from typing import Callable

def filter(filtee:np.ndarray, sifter:np.ndarray, func:Callable) -> np.ndarray:
    r = aux.cp2d(filtee)
    for i,x in enumerate(filtee):
        for j,y in enumerate(x):
            r[i,j] = func(y, sifter[i,j])
    return np.array(r)

def map(func:Callable, filtee:np.ndarray) -> np.ndarray:
    r = np.zeros(filtee.shape)
    r[:,:] = np.vectorize(func)(filtee)[:,:]
    return r

def nansync(x, f):
        if np.isnan(f):
            return np.nan
        else:
            return x

def falsetonan(x, f):
        if f:
            return x
        else:
            return np.nan

def isnan(f) -> bool:
        if np.isnan(f):
            return 1
        else:
            return 0

def isnotnan(f) -> bool:
        if np.isnan(f):
            return 0
        else:
            return 1