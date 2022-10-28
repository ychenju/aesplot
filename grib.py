# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr
import numpy as np
from . import grid as apg

class grib1:

    def __init__(self, path, shortName='', typeOfLevel=''):
        '''
        '''
        kwargs = {'engine': 'cfgrib',}
        if typeOfLevel or shortName:
            kwargs['filter_by_keys'] = {}
            if typeOfLevel:
                self.typeOfLevel = shortName
                kwargs['filter_by_keys']['typeOfLevel'] = typeOfLevel
            if shortName:
                self.shortName = shortName
                kwargs['filter_by_keys']['shortName'] = shortName
        self.dataset = xr.open_dataset(path, **kwargs)

    def sel(self, shortName='', value=0, **kwargs):
        '''
        '''
        if shortName:
            if len(list(kwargs.keys())):
                self.val_sub:np.ndarray = self.dataset[shortName].sel(**kwargs).values
                self.lat_sub:np.ndarray = self.dataset[shortName].sel(**kwargs).latitude.values
                self.long_sub:np.ndarray = self.dataset[shortName].sel(**kwargs).longitude.values
            else:
                self.val_sub:np.ndarray = self.dataset[shortName].sel(**{self.typeOfLevel:value}).values
                self.lat_sub:np.ndarray = self.dataset[shortName].sel(**{self.typeOfLevel:value}).latitude.values
                self.long_sub:np.ndarray = self.dataset[shortName].sel(**{self.typeOfLevel:value}).longitude.values
        else:

            if len(list(kwargs.keys())):
                self.val_sub:np.ndarray = self.dataset[self.shortName].sel(**kwargs).values
                self.lat_sub:np.ndarray = self.dataset[self.shortName].sel(**kwargs).latitude.values
                self.long_sub:np.ndarray = self.dataset[self.shortName].sel(**kwargs).longitude.values
            else:
                self.val_sub:np.ndarray = self.dataset[self.shortName].sel(**{self.typeOfLevel:value}).values
                self.lat_sub:np.ndarray = self.dataset[self.shortName].sel(**{self.typeOfLevel:value}).latitude.values
                self.long_sub:np.ndarray = self.dataset[self.shortName].sel(**{self.typeOfLevel:value}).longitude.values
        self.val = np.zeros(self.val_sub.shape)
        self.lat = np.zeros((len(self.lat_sub), len(self.long_sub)))
        self.long = np.zeros((len(self.lat_sub), len(self.long_sub)))
        long2 = np.where(self.long_sub > 180, self.long_sub - 360, self.long_sub)
        argl = np.argsort(long2)
        for j in range(len(self.long_sub)):
            self.val[:,argl[j]] = self.val_sub[:,j]
            self.lat[:,argl[j]] = self.lat_sub[:]
        for l in self.long:
            l[argl[:]] = long2[:]
        return self

    def to_Grids(self, use_key=False):
        '''
        '''
        return apg.Grids(self.lat, self.long, self.val)