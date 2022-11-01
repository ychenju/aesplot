# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
from . import auxf as aux
from . import grid

class nc4base:
    '''
    Basical class of netCDF4
    '''
    def __init__(self, path:str) -> None:
        '''
        '''
        self.data = xr.open_dataset(path)

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

class nc4tll(nc4base):

    def __init__(self, path:str) -> None:
        '''
        Load netCDF4 file with coordinates 'time', 'latitude', and 'longitude' \n
        Able to process: ECMWF_IFS_CY41r2 ECMWF Operational 6-hourly atmospheric surface analysis [netCDF4] datasets
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

class nc4sfll(nc4base):

    def  __init__(self, path:str) -> None:
        '''
        NetCdf4 Single Forecast Latitude Longitude
        Load netCDF4 file with coordinates 'forecast_hour', 'forecast_initial_time', 'latitude', and 'longitude' \n
        Able to process: ECMWF_IFS_CY41r2 ECMWF Operational 6-hourly atmospheric surface analysis [netCDF4] datasets
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
    def forecast_hour(self):
        '''
        '''
        return self.data.forecast_hour

    @property
    def fh(self):
        '''
        Return the coordinate values 'forecast_hour.values'
        '''
        return self.data.forecast_hour.values

    @property
    def forecast_initial_time(self):
        '''
        '''
        return self.data.forecast_initial_time

    @property
    def fit(self):
        '''
        Return the coordinate values 'forecast_initial_time.values'
        '''
        return self.data.forecast_initial_time.values

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

    def to_Grids(self, key:str, forecast_hour_index:int=0, forecast_initial_time_index:int=0) -> grid.Grids:
        '''
        '''
        return grid.Grids(self.lats, self.longs, self.data[key].values[forecast_hour_index, forecast_initial_time_index])