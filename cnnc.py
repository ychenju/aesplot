# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from . import wrfp as wp
from . import grid
from typing import Tuple

class CNnc:
    
    def __init__(self, path:str) -> None:
        self.ncfile = xr.open_dataset(path)
        self.lat = np.array(self['lat'])
        self.lon = np.array(self['lon'])

    def __getitem__(self, key:str) -> np.ndarray:
        return np.array(self.ncfile[key])

    def llbc(self) -> Tuple[np.ndarray]:
        xlong = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        xlat = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        for j, y in enumerate(self.lat):
            for i, x in enumerate(self.lon):
                xlat[j][i] = y
                xlong[j][i] = x
        return xlat, xlong

class month_mean_temp(CNnc):
    
    def __init__(self, path:str) -> None:
        self.ncfile = xr.open_dataset(path)
        self.lat = np.array(self['lat'])
        self.lon = np.array(self['lon'])
        self.tmps = np.array(self['tmp'])

    def to_wp_frame(self) -> wp.frame:
        _llbc = self.llbc()
        _r = wp.voidFrame(*_llbc, time=None)
        for i in range(len(self.tmps)):
            _r.set(f'TMP_{i+1}', tmp_conv(self.tmps[i]))
        return _r

    def to_wp_frames(self) -> Tuple[wp.frame]:
        _llbc = self.llbc()
        return [wp.voidFrame(*_llbc, time=None).set('TMP', tmp_conv(self.tmps[i])) for i in range(len(self.tmps))]

    def to_grids(self, month:int) -> grid.Grids:
        _llbc = self.llbc()
        _r = grid.Grids(*_llbc, self.tmps[month-1])
        return _r


def tmp_conv(tmp:float) -> float:
    return tmp/10.+273.15

def llbc(data:CNnc) -> Tuple[np.ndarray]:
    lon = np.array(data['lon'])
    lat = np.array(data['lat'])
    xlong = np.zeros((lat.shape[0], lon.shape[0]))
    xlat = np.zeros((lat.shape[0], lon.shape[0]))
    for i, x in enumerate(lat):
        for j, y in enumerate(lon):
            xlat[i][j] = x
            xlong[i][j] = y
    return xlat, xlong