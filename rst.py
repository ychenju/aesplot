# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import osgeo.gdal as gdal
import numpy as np
from typing import Tuple
from . import grid as apg
from tqdm import tqdm

def gettifs(path:str) -> list:
    '''
    '''
    paths = os.listdir(path)
    fullpaths = [path + '\\' + p for p in paths if p[-4:] == '.tif']
    return fullpaths

def rstlist(path:str, name:str='') -> list:
    '''
    '''
    return [raster(gettifs(path)[i], name) for i in range(len(gettifs(path)))]

class MODIS:
    SCALE_FACTOR = {
        'Lai_500m': 0.1,
    }

    FILL_VALUE_LOW = {
        'Lai_500m': 249,
    }

class raster:

    def __init__(self, path:str, name:str='') -> None:
        '''
        '''
        self.raster = gdal.Open(path)
        self.array = self.raster.ReadAsArray()
        self.name = name
        self.geotransform = self.raster.GetGeoTransform()

    @property
    def rows(self) -> int:
        '''
        '''
        return self.raster.RasterYSize

    @property
    def cols(self) -> int:
        '''
        '''
        return self.raster.RasterXSize

    @property
    def bands(self) -> int:
        '''
        '''
        return self.raster.RasterCount

    @property
    def proj(self):
        '''
        '''
        return self.raster.GetProjection()

    @property
    def values(self) -> np.ndarray:
        '''
        '''
        return self.array*MODIS.SCALE_FACTOR[self.name] if self.name else self.array

    @property
    def scale_factor(self) -> float:
        '''
        '''
        return MODIS.SCALE_FACTOR[self.name]

    @property
    def fill_value_low(self) -> int:
        '''
        '''
        return MODIS.FILL_VALUE_LOW[self.name]

    @property
    def effective(self) -> np.ndarray:
        '''
        '''
        return np.where(self.array < self.fill_value_low, self.values, np.nan)

    @property
    def oriX(self) -> float:
        '''
        '''
        return self.geotransform[0]

    @property
    def oriY(self) -> float: 
        '''
        '''
        return self.geotransform[3]

    @property
    def pxWidth(self) -> float:
        '''
        '''
        return self.geotransform[1]

    @property
    def pxHeight(self) -> float:
        '''
        '''
        return self.geotransform[5]

    @property
    def rotX(self) -> float:
        '''
        '''
        return self.geotransform[2]

    @property
    def rotY(self) -> float:
        '''
        '''
        return self.geotransform[4]

    def tolat(self, y:int) -> float:
        '''
        '''
        return y*self.pxHeight + self.oriY - self.pxHeight/2

    def tolong(self, x:int) -> float:
        '''
        '''
        return x*self.pxWidth + self.oriX - self.pxWidth/2

    def tocoor(self, x:int, y:int) -> Tuple[float]:
        '''
        '''
        return self.tolong(x), self.tolat(y)

    @property
    def long(self) -> np.ndarray:
        '''
        This is the 1d lat. Use llbc() to get 2d
        '''
        return np.array([self.tolong(x) for x in range(self.cols)])

    @property
    def lat(self) -> np.ndarray:
        '''
        This is the 1d long. Use llbc() to get 2d
        '''
        return np.array([self.tolat(x) for x in range(self.rows)])

    def llbc(self, inv:bool=False, verbose:bool=False, dtype=np.float32) -> Tuple[np.ndarray]:
        '''
        Broadcast the 1d lat,long data to WRF-type 2d lat,long data
        '''
        xlong = np.zeros((self.lat.shape[0], self.long.shape[0]), dtype=dtype)
        xlat = np.zeros((self.lat.shape[0], self.long.shape[0]), dtype=dtype)
        if verbose:
            try:
                with tqdm(self.lat, desc='rst.raster.llbc():') as _tqdm:
                    for i, y in enumerate(_tqdm):
                        for j, x in enumerate(self.long):
                            xlat[i][j] = y
                            xlong[i][j] = x
            except KeyboardInterrupt:
                _tqdm.close()
                raise
            _tqdm.close()
        else:
            for i, y in enumerate(self.lat):
                for j, x in enumerate(self.long):
                    xlat[i][j] = y
                    xlong[i][j] = x
        self.lls = (xlat, xlong)
        if inv:
            return xlong, xlat
        return xlat, xlong

    def __call__(self) -> float:
        '''
        '''
        return self.values

def raster_to_grid(raster:raster, kind='effective', data='', verbose:bool=False, dtype=np.float32) -> apg.Grids:
    '''
    raster to grid:

    kind: the target np.ndarray to put in the Grids object, 
    can be 'effective', 'values' or 'array'  

    data:
    if not set, the data will appear as Grids._data
    if set, the data will be in Grids.kwargs[data]
    '''
    if not data:
        if kind.lower() == 'effective':
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), raster.effective)
        elif kind.lower() == 'values':
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), raster.values)
        elif kind.lower() == 'array':
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), raster.array)
    else:
        if kind.lower() == 'effective':
            kwargs = {data: raster.effective}
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), **kwargs)
        elif kind.lower() == 'values':
            kwargs = {data: raster.values}
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), **kwargs)
        elif kind.lower() == 'array':
            kwargs = {data: raster.array}
            return apg.Grids(*raster.llbc(verbose=verbose, dtype=dtype), **kwargs)