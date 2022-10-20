# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from . import auxf as aux
from . import filter as apfilter
from . import prep as app
from . import toolkit as tk
from . import trigo as atri
from typing import Sequence, Union, Tuple, Callable
from tqdm import tqdm

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

    @property
    def step(self) -> Tuple[float]:
        return np.mean(self.lat[1:,0]-self.lat[:-1,0]), np.mean(self.long[0,1:]-self.long[0,:-1])

    @property
    def resy(self) -> float:
        return atri.lattokm(np.mean(self.lat[1:,0]-self.lat[:-1,0]))

    def cast(self, target:object) -> object:
        '''
        '''

    def join(self, target:object, threshold=0.01, func=lambda x,y: np.nanmean(x,y)) -> object:
        '''
        '''

    def map(self, target:object, verbose:bool=True, dtype=np.float32) -> object:
        _md = np.zeros(list(target.lat.shape)+[2], dtype=np.int16)
        if verbose:
            try:
                with tqdm(range(target.lat.shape[0]), desc='grid.Grids.map()') as _tqdm:
                    for i in _tqdm:
                        for j in range(target.lat.shape[1]):
                            _d = np.zeros(self.lat.shape)
                            _d[:,:] = aux.dist((self.lat[:,:],self.long[:,:]),(target.lat[i,j],target.long[i,j]))
                            _md[i,j] = np.array([np.argmin(_d)//_d.shape[1], np.argmin(_d)%_d.shape[1]])
            except KeyboardInterrupt:
                _tqdm.close()
                raise
            _tqdm.close()
        else:
            for i in range(target.lat.shape[0]):
                for j in range(target.lat.shape[1]):
                    _d = np.zeros(self.lat.shape)
                    _d[:,:] = aux.dist((self.lat[:,:],self.long[:,:]),(target.lat[i,j],target.long[i,j]))
                    _md[i,j] = np.array([np.argmin(_d)//_d.shape[1], np.argmin(_d)%_d.shape[1]])
        _r = Grids(target.lat, target.long)
        if isinstance(self._data, np.ndarray):
            _r._data = np.zeros(target.lat.shape)
            _r._data[:,:] = self._data[_md[:,:,0],_md[:,:,1]]
        for kw in self.kwargs:
            _r[kw] = np.zeros(self[kw].shape)
            _r[kw][:,:] = self[kw][_md[:,:,0],_md[:,:,1]]
        return _r

    def maps(self, targets:Sequence[object], verbose:bool=True, dtype=np.float32) -> object:
        '''
        '''

    def restrict(self, lat:list, long:list, buffer:float=0):
        ddlat = (self.lat[1,0]-self.lat[0,0])/np.abs(self.lat[1,0]-self.lat[0,0])
        ddlong = (self.long[0,1]-self.long[0,0])/np.abs(self.long[0,1]-self.long[0,0])
        latis = [0,self.lat.shape[0]]
        longis = [0,self.long.shape[1]]
        if ddlat > 0:
            if self.lat[-1,0] < lat[0]-buffer or self.lat[0,0] > lat[1]+buffer:
                    raise RuntimeError('grid.Girds.restrict(): No Data in the area given')
            for i in range(self.lat.shape[0]-1):
                if self.lat[i,0] < lat[0]-buffer and self.lat[i+1,0] >= lat[0]-buffer:
                    latis[0] = i+1
                if self.lat[self.lat.shape[0]-i-1,0] > lat[1]+buffer and self.lat[self.lat.shape[0]-i-2,0] <= lat[1]+buffer:
                    latis[1] = self.lat.shape[0]-i-1
        elif ddlat < 0:
            if self.lat[0,0] < lat[0]-buffer or self.lat[-1,0] > lat[1]+buffer:
                    raise RuntimeError('grid.Girds.restrict(): No Data in the area given')
            for i in range(self.lat.shape[0]-1):
                if self.lat[i,0] > lat[1]+buffer and self.lat[i+1,0] <= lat[1]+buffer:
                    latis[0] = i+1
                if self.lat[self.lat.shape[0]-i-1,0] < lat[0]-buffer and self.lat[self.lat.shape[0]-i-2,0] >= lat[0]-buffer:
                    latis[1] = self.lat.shape[0]-i-1
        if ddlong > 0:
            if self.long[0,-1] < long[0]-buffer or self.long[0,0] > long[1]+buffer:
                    raise RuntimeError('grid.Girds.restrict(): No Data in the area given')
            for i in range(self.long.shape[1]-1):
                if self.long[0,i] < long[0]-buffer and self.long[0,i+1] >= long[0]-buffer:
                    longis[0] = i+1
                if self.long[0,self.long.shape[1]-i-1] > long[1]+buffer and self.long[0,self.long.shape[1]-i-2] <= long[1]+buffer:
                    longis[1] = self.long.shape[1]-i-1
        elif ddlong < 0:
            if self.long[0,0] < long[0]-buffer or self.long[0,-1] > long[1]+buffer:
                    raise RuntimeError('grid.Girds.restrict(): No Data in the area given')
            for i in range(self.long.shape[-1]-1):
                if self.long[0,i] > long[1]+buffer and self.long[0,i+1] <= long[1]+buffer:
                    longis[0] = i+1
                if self.long[0,self.long.shape[1]-i-1] < long[0]-buffer and self.long[0,self.long.shape[1]-i-2] >= long[0]-buffer:
                    longis[1] = self.long.shape[1]-i-1
        indices = (slice(*latis), slice(*longis))
        _r = Grids(self.lat[indices], self.long[indices])
        if isinstance(self._data, np.ndarray):
            _r._data = self._data[indices]
        for kw in self.kwargs:
            _r.kwargs[kw] = self.kwargs[kw][indices]
        return _r
    
    def lowres3(self, verbose:bool=False):
        indices = (slice(None,self.lat.shape[0]//3*3), slice(None,self.lat.shape[1]//3*3))
        _r = Grids(self.lat[indices], self.long[indices])
        if isinstance(self._data, np.ndarray):
            _r._data = self._data[indices]
        for kw in self.kwargs:
            _r.kwargs[kw] = self.kwargs[kw][indices]
        if verbose:
            try:
                with tqdm(range(1,_r.lat.shape[0], 3), desc='grid.Grids.lowres3()') as _tqdm:
                    for i in _tqdm:
                        for j in range(1, _r.lat.shape[1], 3):
                            _r.lat[i,j] = np.nanmean(_r.lat[i-1:i+2,j-1:j+2])
                            _r.long[i,j] = np.nanmean(_r.long[i-1:i+2,j-1:j+2])
                            if isinstance(_r._data, np.ndarray):
                                _r._data[i,j] = np.nanmean(_r._data[i-1:i+2,j-1:j+2])
                            for kw in self.kwargs:
                                _r.kwargs[kw][i,j] = np.nanmean(_r.kwargs[kw][i-1:i+2,j-1:j+2])
            except KeyboardInterrupt:
                _tqdm.close()
                raise
            _tqdm.close()
        else:
            for i in range(1,_r.lat.shape[0], 3):
                for j in range(1, _r.lat.shape[1], 3):
                    _r.lat[i,j] = np.nanmean(_r.lat[i-1:i+2,j-1:j+2])
                    _r.long[i,j] = np.nanmean(_r.long[i-1:i+2,j-1:j+2])
                    if isinstance(_r._data, np.ndarray):
                        _r._data[i,j] = np.nanmean(_r._data[i-1:i+2,j-1:j+2])
                    for kw in self.kwargs:
                        _r.kwargs[kw][i,j] = np.nanmean(_r.kwargs[kw][i-1:i+2,j-1:j+2])
        _r.lat = _r.lat[1::3,1::3]
        _r.long = _r.long[1::3,1::3]
        if isinstance(self._data, np.ndarray):
            _r._data = self._data[1::3,1::3]
        for kw in self.kwargs:
            _r.kwargs[kw] = self.kwargs[kw][1::3,1::3]
        return _r

    def pseudolowres(self, res:int):
        _r = Grids(pseudo_lowres(self.lat, res), pseudo_lowres(self.long, res))
        if isinstance(self._data, np.ndarray):
            _r._data = pseudo_lowres(self._data, res)
        for kw in self.kwargs:
            _r.kwargs[kw] = pseudo_lowres(self.kwargs[kw], res)
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

class GridsCopy(Grids):

    def __init__(self, target:Grids) -> None:
        self.lat = target.lat
        self.long = target.long
        self._data = target._data if isinstance(target._data, np.ndarray) else None
        for kw in target.kwargs:
            self.kwargs[kw] = target.kwargs[kw]

def pseudo_lowres(arr: np.ndarray, res:int, verbose:bool=False) -> np.ndarray:
    if res == 1:
        return arr
    d = np.zeros(arr.shape)
    d[:,:] = arr[:,:]
    if verbose:
        try:
            with tqdm(range(res//2, d.shape[0]-res//2), desc='grid.pseudo_lowres()') as _tqdm:
                for i in _tqdm:
                    for j in range(res//2, d.shape[1]-res//2):
                        g = arr[i-res//2:i+res//2+1,j-res//2:j+res//2+1]
                        if np.mean(apfilter.map(apfilter.isnan, g)) < 0.5:
                            d[i,j] = np.nanmean(g)
                        else:
                            d[i,j] = np.nan
        except KeyboardInterrupt:
            _tqdm.close()
            raise
        _tqdm.close()
    else:
        for i in range(res//2, d.shape[0]-res//2):
            for j in range(res//2, d.shape[1]-res//2):
                g = arr[i-res//2:i+res//2+1,j-res//2:j+res//2+1]
                if np.mean(apfilter.map(apfilter.isnan, g)) < 0.5:
                    d[i,j] = np.nanmean(g)
                else:
                    d[i,j] = np.nan
    return d[res//2:-(res//2),res//2:-(res//2)]

def join(*targets:Tuple[Grids], threshold:float=0.0001, func:Callable=lambda x: np.nanmean(x), verbose:bool=False) -> Grids:
    if len(targets) == 1:
        return targets[0]
    _r = [GridsCopy(targets[0])]
    for i in range(len(targets)-1):
        t = targets[i+1]
        _r += join2(_r, t, threshold=threshold, func=func, verbose=verbose)
    return _r

def join2(subj:Grids, obj:Grids, threshold:float=0.0001, func:Callable=lambda x: np.nanmean(x), verbose:bool=False) -> Grids:
    _o = GridsCopy(obj)
    _s = GridsCopy(subj)
    mapchart = np.zeros(list(subj.lat.shape)+[2])
    try:
        if verbose:
            with tqdm(range(subj.lat.shape[0]), desc='grid.join2()') as _tqdm:
                for i in _tqdm:
                    for j in range(subj.lat.shape[1]):
                        _d = np.ones(obj.lat.shape)
                        _d[:,:] = aux.dist((subj.lat[i,j], subj.long[i,j]), (obj.lat[:,:], obj.long[:,:]))
                        if np.min(_d) < threshold:
                            mapchart[i,j] = np.array([np.argmin(_d)//_d.shape[1]+1, np.argmin(_d)%_d.shape[1]]+1)
                            if isinstance(_o._data, np.ndarray):
                                _o._data[mapchart[i,j,0],mapchart[i,j,1]] = func(np.array([_o._data[mapchart[i,j,0],mapchart[i,j,1]],_s._data[i,j]]))
                                _s._data[i,j] = np.nan
                            for kw in _o.kwargs:
                                _o.kwargs[kw][mapchart[i,j,0],mapchart[i,j,1]] = func(np.array([_o.kwargs[kw][mapchart[i,j,0],mapchart[i,j,1]],_s.kwargs[kw][i,j]]))
                                _s.kwargs[kw][i,j] = np.nan
                            _s.lat[i,j] = np.nan
                            _s.long[i,j] = np.nan
        else:
            for i in range(subj.lat.shape[0]):
                for j in range(subj.lat.shape[1]):
                    _d = np.ones(obj.lat.shape)
                    _d[:,:] = aux.dist((subj.lat[i,j], subj.long[i,j]), (obj.lat[:,:], obj.long[:,:]))
                    if np.min(_d) < threshold:
                        mapchart[i,j] = np.array([np.argmin(_d)//_d.shape[1]+1, np.argmin(_d)%_d.shape[1]]+1)
                        if isinstance(_o._data, np.ndarray):
                            _o._data[mapchart[i,j,0],mapchart[i,j,1]] = func(np.array([_o._data[mapchart[i,j,0],mapchart[i,j,1]],_s._data[i,j]]))
                            _s._data[i,j] = np.nan
                        for kw in _o.kwargs:
                            _o.kwargs[kw][mapchart[i,j,0],mapchart[i,j,1]] = func(np.array([_o.kwargs[kw][mapchart[i,j,0],mapchart[i,j,1]],_s.kwargs[kw][i,j]]))
                            _s.kwargs[kw][i,j] = np.nan
                        _s.lat[i,j] = np.nan
                        _s.long[i,j] = np.nan
        return [_o, _s]
    except:
        raise RuntimeError(f'Cannot join: {subj} and {obj}')