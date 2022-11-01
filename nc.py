# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from . import auxf as aux
from . import grid

class nc4tll:

    def __init__(self, path:str) -> None:
        '''
        Load netCDF4 file with coordinates 'time', 'latitude', and 'longitude'
        '''
        self.data = xr.open_dataset(path)
        _long = np.vectorize(aux.longfix2)(self.long)
        _lat = self.lat
        argls = np.argsort(_long)
        self._lats = np.zeros((len(_lat), len(_long)), dtype=np.float32)
        self._longs = np.zeros((len(_lat), len(_long)), dtype=np.float32)
        for j in range(len(_long)):
            self._lats[:,argls[j]] = _lat[:]
        for i in range(len(_lat)):
            self._longs[i,argls[:]] = _long[:]

    @property
    def coords(self):
        '''
        '''
        return self.data.coords

    @property
    def attrs(self):
        '''
        '''
        return self.data.attrs

    @property
    def dims(self):
        '''
        '''
        return self.data.dims

    @property
    def vars(self):
        '''
        '''
        return self.data.data_vars

    @property
    def variables(self):
        '''
        '''
        return self.data.variables

    @property
    def lat(self) -> np.ndarray:
        '''
        Return original 1-D latitude array
        '''
        return self.data.latitude.values

    @property
    def long(self) -> np.ndarray:
        '''
        Return original 1-D longitude array
        '''
        return self.data.longitude.values

    @property
    def time(self):
        '''
        '''
        return self.data.time

    @property
    def times(self):
        '''
        Return the coordinate values 'time.values'
        '''
        return self.data.time.values

    @property
    def lats(self) -> np.ndarray:
        '''
        Return 2-D latitude array
        '''
        return self._lats

    @property
    def longs(self) -> np.ndarray:
        '''
        Return 2-D longitude array
        '''
        return self._longs

    def __call__(self, key:str):
        '''
        Return data array of the given variable
        '''
        return self.data[key].values

    def to_Grids(self, key:str, time_index:int) -> grid.Grids:
        '''
        '''
        return grid.Grids(self.lats, self.longs, self.data[key].values[time_index])