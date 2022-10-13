# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from . import wrfp as wp
from typing import Tuple

class CNnc:
    
    def __init__(self, path:str) -> None:
        self.ncfile = xr.open_dataset(path)
        self.lat = np.array(self['lat'])
        self.lon = np.array(self['lon'])

    def __getitem__(self, key:str):
        return np.array(self.ncfile[key])

    def llbc(self) -> Tuple[np.ndarray]:
        '''
        Broadcast the 1d lat,long data to WRF-type 2d lat,long data
        '''
        xlong = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        xlat = np.zeros((self.lat.shape[0], self.lon.shape[0]))
        for j, y in enumerate(self.lat):
            for i, x in enumerate(self.lon):
                xlat[i][j] = y
                xlong[i][j] = x
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

    def to_wp_frames(self) -> Tuple(wp.frame):
        _llbc = self.llbc()
        return [wp.voidFrame(*_llbc, time=None).set('TMP', tmp_conv(self.tmps[i])) for i in range(len(self.tmps))]


def tmp_conv(tmp:float) -> float:
    '''
    convert the CN netCDF data temperature unit to Kelvin
    '''
    return tmp/10.+273.15

# lat-lon broadcasting
def llbc(data:CNnc):
    '''
    Broadcast the 1d lat,long data to WRF-type 2d lat,long data
    '''
    lon = np.array(data['lon'])
    lat = np.array(data['lat'])
    # print(lon.shape)
    # print(lat.shape)
    xlong = np.zeros((lat.shape[0], lon.shape[0]))
    xlat = np.zeros((lat.shape[0], lon.shape[0]))
    for i, x in enumerate(lat):
        for j, y in enumerate(lon):
            xlat[i][j] = x
            xlong[i][j] = y
    return xlat, xlong