# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from typing import Union, Sequence

class csv:

    def __init__(self, path:str, **kwargs) -> None:
        self._x = 'default'
        self._y = 'default'
        self._path = path
        self._pdattrs = {}
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]

    def __call__(self, **kwargs) -> np.ndarray:
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]
        _df:pd.DataFrame = pd.read_csv(self._path, **self._pdattrs)
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

    def __getitem__(self, index:Union[int, tuple]) -> np.ndarray:
        if isinstance(index, tuple):
            self._y, self._x = index
        else:
            self._y = index
        _df:pd.DataFrame = pd.read_csv(self._path, **self._pdattrs)
        _ar = np.array(_df.iloc[:,:])
        _y, _x = _ar.shape
        if isinstance(self._x, str):
            self._x = slice(0, _x)
        if isinstance(self._y, str):
            self._y = slice(0, _y)
        return _ar[self._y, self._x]

    def sub(self, index:Union[int, tuple]):
        if isinstance(index, tuple):
            self._y, self._x = index
        else:
            self._y = index
        return self

    def to_csv(self, path:str, **kwargs):
        _df2 = pd.DataFrame(self())
        _df2.to_csv(path, **kwargs)
        return self


class xls(csv):

    def __init__(self, path:str, sheet:str) -> None:
        self._x = 'default'
        self._y = 'default'
        self._path = path
        self._pdattrs = {'sheet_name': sheet}

    def __call__(self, **kwargs) -> np.ndarray:
        for kw in kwargs.keys():
            self._pdattrs[kw] = kwargs[kw]
        _df:pd.DataFrame = pd.read_excel(self._path, **self._pdattrs)
        _ar = np.array(_df.iloc[:,:])
        _y, _x = _ar.shape
        if isinstance(self._x, str):
            self._x = slice(0, _x)
        if isinstance(self._y, str):
            self._y = slice(0, _y)
        return _ar[self._y, self._x]

    def __getitem__(self, index:Union[int, tuple]) -> np.ndarray:
        if isinstance(index, tuple):
            self._y, self._x = index
        else:
            self._y = index
        _df:pd.DataFrame = pd.read_csv(self._path, **self._pdattrs)
        _ar = np.array(_df.iloc[:,:])
        _y, _x = _ar.shape
        if isinstance(self._x, str):
            self._x = slice(0, _x)
        if isinstance(self._y, str):
            self._y = slice(0, _y)
        return _ar[self._y, self._x]

class xlsx(xls):
    pass

def xy(xy:Sequence) -> dict:
    xy = np.array(xy)
    return {'x': xy[0], 'y': xy[1]}

def yx(xy:Sequence) -> dict:
    xy = np.array(xy)
    return {'x': xy[1], 'y': xy[0]}

def xyz(xyz:Sequence) -> dict:
    xyz = np.array(xyz)
    return {'x': xyz[0], 'y': xyz[1], 'z': xyz[2]}

def yxz(xyz:Sequence) -> dict:
    xyz = np.array(xyz)
    return {'x': xyz[1], 'y': xyz[0], 'z': xyz[2]}

def boundaries(lat:Sequence='None', long:Sequence='None', x:Sequence='None', y:Sequence='None', padding:float='None', padding_x:float=0, padding_y:float=0) -> dict:
    _r = {}
    if isinstance(padding, float) or isinstance(padding, int):
        padding_x = padding
        padding_y = padding
    if not isinstance(lat, str):
        _lat = np.array(lat).reshape(-1)
        _r['lat'] = [np.min(_lat)-padding_y, np.max(_lat)+padding_y]
    if not isinstance(long, str):
        _long = np.array(long).reshape(-1)
        _r['long'] = [np.min(_long)-padding_x, np.max(_long)+padding_x]
    if not isinstance(x, str):
        _x = np.array(x).reshape(-1)
        _r['xlim'] = [np.min(_x)-padding_x, np.max(_x)+padding_x]
    if not isinstance(y, str):
        _y = np.array(y).reshape(-1)
        _r['ylim'] = [np.min(_y)-padding_y, np.max(_y)+padding_y]
    return _r