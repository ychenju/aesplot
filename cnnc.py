# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from . import wrfp as wp
from . import grid
from typing import Tuple
from tqdm import tqdm

class CNnc:
    
    def __init__(self, path:str) -> None:
        self.ncfile = xr.open_dataset(path)
        self.lat = np.array(self['lat'])
        self.lon = np.array(self['lon'])

    def __getitem__(self, key:str) -> np.ndarray:
        return np.array(self.ncfile[key])

    def llbc(self, verbose:bool=False) -> Tuple[np.ndarray]:
        xlong = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        xlat = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        if verbose:
            try:
                with tqdm(enumerate(self.lat), desc='cnnc.CNnc.llbc():') as _tqdm:
                    for j, y in _tqdm:
                        for i, x in enumerate(self.lon):
                            xlat[j][i] = y
                            xlong[j][i] = x
            except KeyboardInterrupt:
                _tqdm.close()
                raise
            _tqdm.close()
        else:
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
        _r = grid.Grids(*_llbc, tmp_conv(self.tmps[month-1]))
        return _r


def tmp_conv(tmp:float) -> float:
    return tmp/10.+273.15

def llbc(data:CNnc, verbose:bool=False) -> Tuple[np.ndarray]:
    xlong = np.zeros((data.lat.shape[0], data.lon.shape[0]))
    xlat = np.zeros((data.lat.shape[0], data.lon.shape[0]))
    if verbose:
        try:
            with tqdm(enumerate(data.lat), desc='cnnc.llbc():') as _tqdm:
                for j, y in _tqdm:
                    for i, x in enumerate(data.lon):
                        xlat[j][i] = y
                        xlong[j][i] = x
        except KeyboardInterrupt:
            _tqdm.close()
            raise
        _tqdm.close()
    else:
        for j, y in enumerate(data.lat):
            for i, x in enumerate(data.lon):
                xlat[j][i] = y
                xlong[j][i] = x
    return xlat, xlong