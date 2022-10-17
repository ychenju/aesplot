# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from . import auxf as aux
from . import prep as app
from . import toolkit as tk
from typing import Union, Tuple

class Grids:
    
    def __init__(self, *args, **kwargs) -> None:
        try:
            if not 'lat' in kwargs.keys():
                self.lat:np.ndarray = args[0]
            if not 'long' in kwargs.keys():
                self.long:np.ndarray = args[1]
            if len(args) >= 3:
                self._data = args[2]
            else:
                self._data = None
            self.kwargs = {}
            for kw in kwargs.keys():
                if not kw == 'lat' and not kw == 'long':
                    self.kwargs[kw] = kwargs[kw]
                elif kw == 'lat':
                    self.lat = kwargs[kw]
                elif kw == 'long':
                    self.long = kwargs[kw]
        except:
            raise RuntimeError('Cannot generate Grids object')

    @property
    def data(self):
        return self._data

    def __getitem__(self, index:Union[str, Tuple[int, str, slice]]) -> Union[object, np.ndarray]:
        try:
            if isinstance(index, str):
                return self.kwargs[index]
            elif isinstance(index, tuple):
                if len(index) == 2:
                    if isinstance(index[0], int) and isinstance(index[1], int):
                        return Grid(self, *index)
                    elif isinstance(index[0], slice) or isinstance(index[1], slice):
                        kwargs = {}
                        for kw in self.kwargs.keys():
                            kwargs[kw] = self.kwargs[kw][index[0],index[1]]
                        if isinstance(self.data, np.ndarray):
                            return Grids(self.lat[index[0]], self.long[index[1]], self.data[index[0],index[1]], **kwargs)
                        else:
                            return Grids(self.lat[index[0], index[1]], self.long[index[0], index[1]], **kwargs)
                    elif isinstance(index[0], str) or isinstance(index[1], str):
                        return self.kwargs[index[0]], self.kwargs[index[1]]
                else:
                    _r = []
                    for kw in index:
                            _r.append(self.kwargs[kw])
                return _r
        except:
            raise RuntimeError('Inappropriate usage of Grids.__getitem__()')

    def __setitem__(self, index:Union[int, str], value:np.ndarray):
        try:
            if not index:
                self._data = value
            elif isinstance(index, str):
                self.kwargs[index] = value
            return self
        except:
            raise RuntimeError('Inappropriate usage of Grids.__getitem__()')

    def boundaries(self, y:int, x:int):
        xb, yb = (0,0), (0,0)
        if x and not x== self.long.shape[1] - 1:
            xb = (self[y,x-1].long + self[y,x].long)/2, (self[y,x+1].long + self[y,x].long)/2
        elif not x:
            xb = (3*self[y,0].long - self[y,1].long)/2, (self[y,1].long + self[y,0].long)/2
        elif x == self.long.shape[1] - 1:
            xb = (self[y,x-1].long + self[y,x].long)/2, (3*self[y,x].long - self[y,x-1].long)/2
        if y and not y == self.lat.shape[0] - 1:
            yb = (self[y-1,x].lat + self[y,x].lat)/2, (self[y+1,x].lat + self[y,x].lat)/2
        elif not y:
            yb = (3*self[0,x].lat - self[1,x].lat)/2, (self[1,x].lat + self[0,x].lat)/2
        elif y == self.lat.shape[0] - 1:
            yb = (self[y-1,x].lat + self[y,x].lat)/2, (3*self[y,x].lat - self[y-1,x].lat)/2
        return yb, xb

    def cast(self, target:object) -> object:
        '''
        '''

    def join(self, target:object, threshold=0.01, func=lambda x,y: np.nanmean(x,y)) -> object:
        '''
        '''

    def map(self, target:object) -> object:
        _d = np.zeros(list(target.lat.shape)+list(self.lat.shape))
        _md = np.zeros(list(target.lat.shape)+[2], dtype=np.int16)
        for i in range(target.lat.shape[0]):
            for j in range(target.lat.shape[1]):
                _d[i,j,:,:] = aux.dist((self.lat[:,:],self.long[:,:]),(target.lat[i,j],target.long[i,j]))
                _md[i,j] = (np.array([np.argmin(_d[i,j])//target.lat.shape[1], np.argmin(_d[i,j])%target.lat.shape[1]]))
        _r = Grids(target.lat, target.long)
        if isinstance(self._data, np.ndarray):
            _r[0] = np.zeros_like(self.data)
            _r[0][:,:] = self.data[_md[:,:,0],_md[:,:,1]]
        for kw in self.kwargs:
            _r[kw] = np.zeros_like(self[kw])
            _r[kw][:,:] = self[kw][_md[:,:,0],_md[:,:,1]]
        return _r





    def fileout(self, path:str, overw:bool=False) -> None:
        if os.path.exists(path):
            if overw:
                shutil.rmtree(path)
                os.mkdir(path)
        else:
            os.mkdir(path)
        kwargs = {'header': False, 'index': False}
        tk.tocsv(self.lat, path+f'\\LAT.csv', **kwargs)
        tk.tocsv(self.long, path+f'\\LONG.csv', **kwargs)
        if isinstance(self.data, np.ndarray):
            tk.tocsv(self.data, path+f'\\DATA.csv', **kwargs)
        for key in self.kwargs.keys():
            tk.tocsv(self[key], path+f'\\DATA_{key}.csv', **kwargs)

class Grid:

    def __init__(self, grids:Grids, y:int, x:int) -> None:
        self.lat:np.ndarray = grids.lat[y,x]
        self.long:np.ndarray = grids.long[y,x]
        self._data = grids._data
        self.kwargs = {}
        for kw in grids.kwargs.keys():
            self.kwargs[kw] = grids.kwargs[kw]
        self.origin = grids
        self.index = y, x

    @property
    def boundaries(self):
        return self.origin.boundaries(*self.index)

    @property
    def boundariesT(self):
        return self.origin.boundaries(*self.index)[::-1]

class filein(Grids):

    def __init__(self, path:str) -> None:
        paths = os.listdir(path)
        self.lat = aux.cp2d(app.csv(path+r'\LAT.csv', header=None)())
        self.long = aux.cp2d(app.csv(path+r'\LONG.csv', header=None)())
        try:
            self._data = aux.cp2d(app.csv(path+r'\DATA.csv', header=None)())
        except:
            self._data = None
            print('The directory has no \'DATA.csv\', thus self.data will be void')
        self.kwargs = {}    
        for p in paths:
            if p[:5] == 'DATA_':
                self.kwargs[p[5:-4]] = aux.cp2d(app.csv(f'{path}\\{p}', header=None)())