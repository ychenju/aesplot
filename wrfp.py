# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xarray as xr
import numpy as np
import shutil
from . import auxf as aux
from . import basemap as apb
from . import fig as apf
from . import filter as apfilter
from . import img as ap
from . import prep as app
from . import stat
from . import toolkit as tk
from . import ascl
from . import ts as apts
from typing import Sequence, Tuple, Union

class wrfout:

    ncfile = None

    def __init__(self, path:str):
        self.ncfile = xr.open_dataset(path)
    
    def extract(self, *keys:Tuple[str]):
        return frame(self.ncfile, *keys)   

    def __getitem__(self, key:str) -> np.ndarray:
        return np.array(self.ncfile[key]).squeeze()
    
FRAME_DEFAULT_FLAGS = {
    'CUT': False,
    'LEN':  0,
    'REMOVEWATER': False,
    'RES': 1.,
}

class frame:

    lat = None
    long = None
    time = None

    def __init__(self, source:wrfout, *keys:Tuple[str]):
        self._data = {}    
        self._flag = {}
        for flag in FRAME_DEFAULT_FLAGS.keys():
            self._flag[flag] = FRAME_DEFAULT_FLAGS[flag]
        self._chara = {}   
        self.lat =  aux.cp2d(np.array(source['XLAT']).squeeze())
        self.long = aux.cp2d(np.array(source['XLONG']).squeeze())
        self.time = np.array(source['XTIME']).squeeze()
        self.label = '__'
        for key in keys:
            self._data[key] = aux.cp2d(np.array(source[key]).squeeze())
    
    def load(self, source:wrfout, *keys:Tuple[str]):    
        for key in keys:
            self._data[key] = aux.cp2d(np.array(source.ncfile[key]).squeeze())
        return self

    def params(self):   
        _l = [x for x in self._data]
        print(_l)
        return _l
    
    def get(self, key:str): 
        return self._data[key]
    
    def __getitem__(self, key:str):
        return self._data[key]
    
    def getall(self):  
        return self._data

    def set(self, key:str, value):  
        self._data[key] = value
        return self
    
    def __setitem__(self, key:str, value):
        self._data[key] = value
        return self
    
    def delete(self, key:str):  
        del self._data[key]
        return self
    
    def __delitem__(self, key:str):
        del self._data[key]
        return self

    def getflag(self, key:str):
        return self._flag[key]

    def setflag(self, key:str, value):
        self._flag[key] = value
        return self

    def getchara(self, key:str):
        return self._chara[key]

    def removewater(self):
        if not ('LANDMASK' in self._data.keys()):
            raise RuntimeError("'LANDMASK' has not been loaded to the data frame")
        ori = self.lat
        for k in filter(lambda _x: _x != 'LANDMASK', self.getall().keys()):
            if self[k].shape == ori.shape:
                self[k] = apfilter.filter(self[k], self['LANDMASK'], apfilter.falsetonan)
        self['XLAT_RW'] = apfilter.filter(self.lat, self['LANDMASK'], apfilter.falsetonan)
        self['XLONG_RW'] = apfilter.filter(self.long, self['LANDMASK'], apfilter.falsetonan)
        self._flag['REMOVEWATER'] = True
        return self

    def planefit(self, key:str) -> Tuple[np.ndarray]:
        if self._flag['REMOVEWATER']:
            _T1, _Tr = stat.planefit(self._data['XLONG_RW'], self._data['XLAT_RW'], self._data[key])
        else:
            _T1, _Tr = stat.planefit(self.long, self.lat, self._data[key])
        self._data['PF_'+key+'_1'] = _T1
        self._data['PF_'+key+'_r'] = _Tr
        return _T1, _Tr

    def sigma(self, key:str, fit:bool=True) -> float:
        if aux.isnantable(self._data[key]):
            self._chara[key+'_SIGMA'] = np.nan
            return np.nan
        if fit:
            if self._flag['REMOVEWATER']:
                _sig = stat.sigma(self._data['XLONG_RW'], self._data['XLAT_RW'], self._data[key])
            else:
                _sig = stat.sigma(self.long, self.lat, self._data[key])
        else:
            _sig = stat.sigmawithoutfit(self._data[key])
        self._chara[key+'_SIGMA'] = _sig
        return _sig

    def sigma_alt(self, key:str, threshold:Union[int, float]=10) -> float:
        if aux.isnantable(self._data[key]):
            self._chara[key+'_SIGMA'] = np.nan
            return np.nan
        if not issmallgrid(self, threshold=threshold):
            if self._flag['REMOVEWATER']:
                _sig = stat.sigma(self._data['XLONG_RW'], self._data['XLAT_RW'], self._data[key])
            else:
                _sig = stat.sigma(self.long, self.lat, self._data[key])
        else:
            _sig = stat.sigmawithoutfit(self._data[key])
        self._chara[key+'_SIGMA'] = _sig
        return _sig

    def getsigma(self, key:str) -> float:
        return self._chara[key+'_SIGMA']

    def quickshow(self, key:str) -> ap.image:
        _img = ap.image()
        _img.addbasemap(apb.coast(**app.boundaries(self.lat, self.long)).lls(10))
        _img.add(apf.contourf(**app.xyz([self.long, self.lat, self[key]])).format(cmap='jet'))
        _img.labels(title=key)
        _img.colorbar()
        _img.show()
        return _img

    def show(self, key:str, f=lambda x:x, **kwargs) -> ap.image:
        _image_attrs = {'title': key}
        _basemap_attrs = app.boundaries(self.lat, self.long)
        _lls_attrs = {'inv': 10}
        _figure_attrs = app.xyz([self.long, self.lat, f(self[key])])
        _format_attrs = {'cmap': 'jet'}
        for kw in kwargs.keys():
            if kw in ('inv', 'latref', 'latref2', 'longref', 'longref2'):
                _lls_attrs[kw] = kwargs[kw]
            elif kw in ('cmap', 'levels'):
                _format_attrs[kw] = kwargs[kw]
            elif kw in ('x', 'y', 'z', 'clabels'):
                _figure_attrs[kw] = kwargs[kw]
            elif kw in ('proj', 'long', 'lat', 'res', 'clcolor', 'cllw', 'clbgs'):
                _basemap_attrs[kw] = kwargs[kw]
            elif kw in ('font', 'saveas', 'figsize', 'dpi', 'title'):
                _image_attrs[kw] = kwargs[kw]
            elif kw[:6] == 'image_':
                _image_attrs[kw[6:]] = kwargs[kw]
            elif kw[:8] == 'basemap_':
                _basemap_attrs[kw[8:]] = kwargs[kw]
            elif kw[:7] == 'figure_':
                _figure_attrs[kw[7:]] = kwargs[kw]
            elif kw[:4] == 'lls_':
                _lls_attrs[kw[4:]] = kwargs[kw]
            elif kw[:7] == 'format_':
                _format_attrs[kw[7:]] = kwargs[kw]
        _img = ap.image(**_image_attrs)
        _img.addbasemap(apb.coast(**_basemap_attrs).lls(**_lls_attrs))
        _img.add(apf.contourf(**_figure_attrs).format(**_format_attrs))
        _img.formatting(**_image_attrs)
        _img.colorbar()
        _img.show()
        return _img

    def maxof(self, key:str) -> float:
        return np.array(np.ndarray.reshape(self[key], -1)).max()

    def minof(self, key:str) -> float:
        return np.array(np.ndarray.reshape(self[key], -1)).min()

    def get3x3(self, key:str, x:int, y:int) -> np.ndarray:
        r = np.zeros(3,3)
        r[:,:] = self[key][x-1:x+2,y-1:y+2]
        return r

    def mean3x3(self):
        r = voidFrame(self.lat, self.long, self.time)
        for key in self.getall().keys():
            if aux.is2d(self[key]):
                d = np.zeros(self[key].shape)
                d[:,:] = self[key][:,:]
                for i in range(1, d.shape[0]-1):
                    for j in range(1, d.shape[1]-1):
                        if np.mean(apfilter.map(apfilter.isnan, self.get3x3(key,i,j))) < 0.5:
                            d[i+1,j+1] = np.nanmean(self.get3x3(key,i,j))
                        else:
                            d[i+1,j+1] = np.nan
                r[key] = d
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        r.label = self.label + 'MEAN3__'
        return r

    def getnxn(self, key:str, x:int, y:int, res:int) -> np.ndarray:
        r = np.zeros((res,res))
        r[:,:] = self[key][x-res//2:x+res//2+1,y-res//2:y+res//2+1]
        return r

    def meannxn(self, res:int):
        r = voidFrame(self.lat, self.long, self.time)
        for key in self.getall().keys():
            if aux.is2d(self[key]):
                d = np.zeros(self[key].shape)
                d[:,:] = self[key][:,:]
                for i in range(res//2, d.shape[0]-res//2):
                    for j in range(res//2, d.shape[1]-res//2):
                        if np.mean(apfilter.map(apfilter.isnan, self.getnxn(key,i,j,res))) < 0.5:
                            d[i+1,j+1] = np.nanmean(self.getnxn(key,i,j,res))
                        else:
                            d[i+1,j+1] = np.nan
                r[key] = np.array(d)
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        r.label = self.label + f'MEAN{res}__'
        return r

    def crop(self, interv:int=3, fromx:int=1, tox:int=-1, fromy:int=1, toy:int=-1):
        _r = voidFrame(aux.cp2d(self.lat[fromx:tox:interv, fromy:toy:interv]), aux.cp2d(self.long[fromx:tox:interv, fromy:toy:interv]), self.time)
        for key in self.getall().keys():
            _r[key] = aux.cp2d(self[key][fromx:tox:interv, fromy:toy:interv])
        for flag in self._flag.keys():
            _r._flag[flag] = self._flag[flag]
        _r._flag['RES'] *= interv
        _r.label = self.label + f'CROP:{interv}__'
        return _r

    def lowres3(self, fromx:int=1, tox:int=-1, fromy:int=1, toy:int=-1):
        r = self.mean3x3()
        r = r.crop(3, fromx=fromx, tox=tox, fromy=fromy, toy=toy)
        return r

    def tail(self, all:int=0, w:int=0, e:int=0, s:int=0, n:int=0):
        shp = self.lat.shape
        if all:
            fx, fy = all, all
            tx, ty = shp[1]-all, shp[0]-all
        else:
            fx, fy = w, s
            tx, ty = e, n
        r = voidFrame(aux.cp2d(self.lat[fy:ty,fx:tx]), aux.cp2d(self.long[fy:ty,fx:tx]), self.time)
        for key in self.getall().keys():
            r._data[key] = aux.cp2d(self._data[key][fy:ty,fx:tx])
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        return r

    def pseudo_lowres3(self):
        _r = self.mean3x3()
        _r = _r.tail(all=1)
        _r._flag['RES'] = 3
        return _r

    def pseudo_lowres(self, res:int=3):
        if not res % 2:
            raise RuntimeError('\'res\' should be a single number!')
        _r = self.meannxn(res)
        _r = _r.tail(all=res//2)
        _r._flag['RES'] = res
        return _r

    @property
    def res(self) -> int:
        return self._flag['RES']

    @property
    def latrange(self) -> Tuple[float]:
        return (self.lat[:,0].min(), self.lat[:,0].max())

    @property
    def longrange(self) -> Tuple[float]:
        return (self.long[0,:].min(), self.long[0,:].max())

    @property
    def anchor(self) -> Tuple[float]:
        return self.lat[:,0].min(), self.long[0,:].min()

    @property
    def lat1d(self) -> np.ndarray:
        return self.lat[:,0]

    @property
    def long1d(self) -> np.ndarray:
        return self.long[0,:]

    def cut(self, interv:int, fromx:int, fromy:int):
        fx, fy = int(fromx), int(fromy)
        tx = int(fromx + interv)
        ty = int(fromy + interv)
        r = voidFrame(aux.cp2d(self.lat[fy:ty,fx:tx]), aux.cp2d(self.long[fy:ty,fx:tx]), self.time)
        for key in self.getall().keys():
            r._data[key] = aux.cp2d(self._data[key][fy:ty,fx:tx])
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        r.setflag('CUT', True)
        r.setflag('LEN', interv)
        r.label = self.label + f'CUT:{interv}@({fromx},{fromy})__'
        return r

    def cutto(self, fromx:int, fromy:int, tox:int, toy:int):
        fx, fy, tx, ty = int(fromx), int(fromy), int(tox), int(toy)
        r = voidFrame(aux.cp2d(self.lat[fy:ty,fx:tx]), aux.cp2d(self.long[fy:ty,fx:tx]), self.time)
        for key in self.getall().keys():
            r._data[key] = aux.cp2d(self._data[key][fy:ty,fx:tx])
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        r.setflag('CUT', True)
        r.setflag('LENX', tx-fx)
        r.setflag('LENY', ty-fy)
        r.label = self.label + f'CUT:X[{fx}:{tx}]Y[{fy}:{ty}]__'
        return r
    
    def cutup(self, interv:int) -> list: 
        coorlist = []
        for i in range(self.lat.shape[0]//interv):
            for j in range(self.long.shape[1]//interv):
                coorlist.append((i*interv, j*interv))
        r = []
        for coor in coorlist:
            r.append(self.cut(interv, coor[1], coor[0]))
        return r

    def cut3nup(self) -> list:
        ilist = []
        while 3**(len(ilist)+1) < np.min(self.lat.shape) and 3**(len(ilist)+1) < np.min(self.long.shape):
            ilist.append(3**(len(ilist)+1))
        r = []
        for interv in ilist:
            r.append(self.cutup(interv))
        return r

    @property
    def timestr(self) -> str:
        return f'{str(self.time)[:4]}{str(self.time)[5:7]}{str(self.time)[8:10]}{str(self.time)[11:13]}{str(self.time)[14:16]}{str(self.time)[17:19]}'

    @property
    def timeobj(self) -> ascl.dt:
        return ascl.dt(self.timestr)

    def __str__(self) -> str:
        return self.label

    def fileout(self, path:str, overw:bool=False):
        if os.path.exists(path):
            if overw:
                shutil.rmtree(path)
                os.mkdir(path)
        else:
            os.mkdir(path)
        kwargs = {'header': False, 'index': False}
        tk.tocsv(self.lat, path+f'\\LAT.csv', **kwargs)
        tk.tocsv(self.long, path+f'\\LONG.csv', **kwargs)
        tk.tocsv([[self.time]], path+f'\\TIME.csv', **kwargs)
        for key in self._data.keys():
            if len(self[key].shape) == 2:
                tk.tocsv(self[key], path+f'\\DATA_{key}.csv', **kwargs)
        tk.tocsv([[key, self._flag[key]] for key in self._flag.keys()], path+f'\\FLAG.csv', **kwargs)

class voidFrame(frame):
    def __init__(self, lat:np.ndarray, long:np.ndarray, time):
        self.lat = aux.cp2d(lat)
        self.long = aux.cp2d(long)
        self.time = time
        self._data = {}    
        self._flag = {}
        self.label = '__'
        for flag in FRAME_DEFAULT_FLAGS.keys():
            self._flag[flag] = FRAME_DEFAULT_FLAGS[flag]
        self._chara = {}   

class nullFrame(frame):
    def __init__(self):
        self.lat = None
        self.long = None
        self.time = None
        self._data = {}    
        self._flag = {}
        self.label = 'NULL'
        for flag in FRAME_DEFAULT_FLAGS.keys():
            self._flag[flag] = FRAME_DEFAULT_FLAGS[flag]
        self._chara = {}

def findanchor(li:Sequence[frame], lat:float, lon:float) -> frame:
    for l in li:
        if l.anchor == (lat, lon):
            return l
    return nullFrame()

def correspond(hrdf:frame, lrdf:frame, len:int, lx:int, ly:int) -> Tuple[frame]:
    thinGrid = hrdf.cut(len*lrdf.res, lx*lrdf.res, ly*lrdf.res)
    thickGrid= lrdf.cut(len*hrdf.res, lx*hrdf.res, ly*hrdf.res)
    return thinGrid, thickGrid

def to_ts_wpframe(lf:Sequence[frame]) -> apts.wpframe:
    _s1 = apts.wpframe(lat=lf[0].lat, long=lf[0].long)
    for r in lf:
        _s1[r.timestr] = r
    return _s1

def issmallgrid(grid:frame, threshold:Union[int, float]) -> bool:
    return grid.res < threshold

def create_wpframe(path:str, *keys:Tuple[str], removewater:bool=False) -> apts.wpframe:
    _rs = []
    paths = os.listdir(path)
    for fname in paths:
        wo = wrfout(f'{path}\\{fname}')
        _rs.append(wo.extract(*keys).removewater() if removewater else wo.extract(*keys))
    _s1 = to_ts_wpframe(_rs)
    return _s1

def pseudo_correspond(odf:frame, lrdf:frame, lx:int, ly:int) -> Tuple[frame]:
    thinGrid = odf.cut(lrdf.res, lx*lrdf.res, ly*lrdf.res)
    thickGrid= lrdf.cut(1, lx, ly)
    return thinGrid, thickGrid

class filein(frame):

    def __init__(self, path:str):
        paths = os.listdir(path)
        self.lat = aux.cp2d(app.csv(path+r'\LAT.csv', header=None)())
        self.long = aux.cp2d(app.csv(path+r'\LONG.csv', header=None)())
        self.time = app.csv(path+r'\TIME.csv', header=None)[0,0]
        self._data = {}    
        self._flag = {}
        self.label = '__'
        for p in paths:
            if p[:5] == 'DATA_':
                self._data[p[5:-4]] = aux.cp2d(app.csv(f'{path}\\{p}', header=None)())
        self.to_flag(self._flag, aux.cp2d(app.csv(path+r'\FLAG.csv', header=None)()))

    @classmethod
    def to_flag(self, _flag:dict, flaglist: np.ndarray):
        for f in flaglist:
            if f[1] == 'True':
                _flag[f[0]] = True
            elif f[1] == 'False':
                _flag[f[0]] = False
            else:
                try:
                    _flag[f[0]] = int(f[1])
                except:
                    _flag[f[0]] = float(f[1])