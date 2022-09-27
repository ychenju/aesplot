# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr

class csv:

    def __init__(self, path, **kwargs):
        self._x = 'default'
        self._y = 'default'
        self._path = path
        self._pdattrs = {}
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]

    def __call__(self, **kwargs):
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]
        _df = pd.read_csv(self._path, **self._pdattrs)
        _ar = np.array(_df.iloc[:,:])
        _y, _x = _ar.shape
        if isinstance(self._x, str):
            self._x = slice(0, _x)
        if isinstance(self._y, str):
            self._y = slice(0, _y)
        return _ar[self._y, self._x]

    def nhd(self):
        self._pdattrs['header'] = None
        return self

    def __getitem__(self, index):
        if isinstance(index, tuple):
            self._y, self._x = index
        else:
            self._y = index
        return self

    def to_csv(self, path, **kwargs):
        _df2 = pd.DataFrame(self())
        _df2.to_csv(path, **kwargs)


class xls(csv):

    def __init__(self, path, sheet):
        self._x = 'default'
        self._y = 'default'
        self._path = path
        self._pdattrs = {'sheet_name': sheet}

    def __call__(self, **kwargs):
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]
        _df = pd.read_excel(self._path, **self._pdattrs)
        _ar = np.array(_df.iloc[:,:])
        _y, _x = _ar.shape
        if isinstance(self._x, str):
            self._x = slice(0, _x)
        if isinstance(self._y, str):
            self._y = slice(0, _y)
        return _ar[self._y, self._x]

class xlsx(xls):
    pass

def xy(xy):
    xy = np.array(xy)
    return {'x': xy[0], 'y': xy[1]}

def yx(xy):
    xy = np.array(xy)
    return {'x': xy[1], 'y': xy[0]}

def xyz(xyz):
    xyz = np.array(xyz)
    return {'x': xyz[0], 'y': xyz[1], 'z': xyz[2]}

def yxz(xyz):
    xyz = np.array(xyz)
    return {'x': xyz[1], 'y': xyz[0], 'z': xyz[2]}
