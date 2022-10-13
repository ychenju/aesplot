# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from osgeo import gdal
import numpy as np
from typing import Tuple

class MODIS:
    SCALE_FACTOR = {
        'Lai_500m': 0.1,
    }

    FILL_VALUE_LOW = {
        'Lai_500m': 249,
    }

class raster:

    def __init__(self, path:str, name='') -> None:
        self.raster = gdal.Open(path)
        self.array = self.raster.ReadAsArray()
        self.name = name
        self.geotransform = self.raster.GetGeoTransform()

    @property
    def rows(self) -> int:
        return self.raster.RasterYSize

    @property
    def cols(self) -> int:
        return self.raster.RasterXSize

    @property
    def bands(self) -> int:
        return self.raster.RasterCount

    @property
    def proj(self):
        return self.raster.GetProjection()

    @property
    def values(self) -> np.ndarray:
        return self.array*MODIS.SCALE_FACTOR[self.name] if self.name else self.array

    @property
    def scale_factor(self) -> float:
        return MODIS.SCALE_FACTOR[self.name]

    @property
    def fill_value_low(self) -> int:
        return MODIS.FILL_VALUE_LOW[self.name]

    @property
    def effective(self) -> np.ndarray:
        return np.where(self.values < self.fill_value_low, self.values, np.nan)

    @property
    def oriX(self) -> float:
        return self.geotransform[0]

    @property
    def oriY(self) -> float: 
        return self.geotransform[3]

    @property
    def pxWidth(self) -> float:
        return self.geotransform[1]

    @property
    def pxHeight(self) -> float:
        return self.geotransform[5]

    @property
    def rotX(self) -> float:
        return self.geotransform[2]

    @property
    def rotY(self) -> float:
        return self.geotransform[4]

    def tolat(self, y:int) -> float:
        return y*self.pxHeight + self.oriY - self.pxHeight/2

    def tolong(self, x:int) -> float:
        return x*self.pxWidth + self.oriX - self.pxWidth/2

    def tocoor(self, x:int, y:int) -> Tuple[float]:
        return self.tolong(x), self.tolat(y)

    @property
    def long(self):
        return np.array([self.tolong(x) for x in range(self.cols)])

    @property
    def lat(self):
        return np.array([self.tolat(x) for x in range(self.rows)])

    def llbc(self, inv:bool=False) -> Tuple[np.ndarray]:
        xlong = np.zeros((self.lat.shape[0], self.long.shape[0]))
        xlat = np.zeros((self.lat.shape[0], self.long.shape[0]))
        for i, y in enumerate(self.lat):
            for j, x in enumerate(self.long):
                xlat[i][j] = y
                xlong[i][j] = x
        self.lls = (xlat, xlong)
        if inv:
            return xlong, xlat
        return xlat, xlong

    def __call__(self) -> float:
        return self.values