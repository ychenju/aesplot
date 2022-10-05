# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from . import auxf as aux
from . import basemap as apb
from . import figure as apf
from . import filter as apfilter
from . import main as ap
from . import prep as app
from . import stat
from . import toolkit as tk
from . import ascl
from . import ts as apts

class wrfout:

    ncfile = None

    def __init__(self, path):
        self.ncfile = xr.open_dataset(path)
    
    def extract(self, *keys):
        return frame(self.ncfile, *keys)   

    def __getitem__(self, key):
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

    def __init__(self, source, *keys):
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
    
    def load(self, source, *keys):    
        for key in keys:
            self._data[key] = aux.cp2d(np.array(source.ncfile[key]).squeeze())

    def params(self):   
        _l = [x for x in self._data]
        print(_l)
        return _l
    
    def get(self, key): 
        return self._data[key]
    
    def __getitem__(self, key):
        return self._data[key]
    
    def getall(self):  
        return self._data

    def set(self, key, value):  
        self._data[key] = value
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
        return self._data[key]
    
    def delete(self, key):  
        del self._data[key]
    
    def __delitem__(self, key):
        del self._data[key]

    def getflag(self, key):
        return self._flag[key]

    def setflag(self, key, value):
        self._flag[key] = value
        return self._flag[key]

    def getchara(self, key):
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

    def planefit(self, key):
        if self._flag['REMOVEWATER']:
            _T1, _Tr = stat.planefit(self._data['XLONG_RW'], self._data['XLAT_RW'], self._data[key])
        else:
            _T1, _Tr = stat.planefit(self.long, self.lat, self._data[key])
        self._data['PF_'+key+'_1'] = _T1
        self._data['PF_'+key+'_r'] = _Tr
        return _T1, _Tr

    def sigma(self, key, fit=True):
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

    def sigma_alt(self, key, threshold=10):
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

    def getsigma(self, key):
        return self._chara[key+'_SIGMA']

    def quickshow(self, key):
        _img = ap.image()
        _img.addbasemap(apb.coast(**app.boundaries(self.lat, self.long)).lls(10))
        _img.add(apf.contourf(**app.xyz([self.long, self.lat, self[key]])).format(cmap='jet'))
        _img.labels(title=key)
        _img.colorbar()
        _img.show()

    def show(self, key, **kwargs):
        _image_attrs = {'title': key}
        _basemap_attrs = app.boundaries(self.lat, self.long)
        _lls_attrs = {'inv': 10}
        _figure_attrs = app.xyz([self.long, self.lat, self[key]])
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

    def maxof(self, key):
        return np.array(self[key].reshape(-1)).max()

    def minof(self, key):
        return np.array(self[key].reshape(-1)).min()

    def get3x3(self, key, x, y):
        return np.array([self[key][x+i,y+j] for i in (-1,0,1) for j in (-1,0,1)])

    def mean3x3(self):
        r = voidFrame(self.lat, self.long, self.time)
        for key in self.getall().keys():
            d = []
            for i in range(self[key].shape[0]):
                d.append([])
                for j in range(self[key].shape[1]):
                    d[-1].append(self[key][i,j])

            for i, x in enumerate(d[1:-1]):
                for j, _ in enumerate(x[1:-1]):
                    if np.mean(list(map(apfilter.isnan, self.get3x3(key,i,j)))) < 0.5:
                        d[i+1][j+1] = np.nanmean(self.get3x3(key,i,j))
                    else:
                        d[i+1][j+1] = np.nan
            r[key] = np.array(d)
        for flag in self._flag.keys():
            r._flag[flag] = self._flag[flag]
        r.label = self.label + 'MEAN3__'
        return r

    def crop(self, interv=3, fromx=1, tox=-1, fromy=1, toy=-1):
        _r = voidFrame(aux.cp2d(self.lat[fromx:tox:interv, fromy:toy:interv]), aux.cp2d(self.long[fromx:tox:interv, fromy:toy:interv]), self.time)
        for key in self.getall().keys():
            _r[key] = aux.cp2d(self[key][fromx:tox:interv, fromy:toy:interv])
        for flag in self._flag.keys():
            _r._flag[flag] = self._flag[flag]
        _r._flag['RES'] *= interv
        _r.label = self.label + f'CROP:{interv}__'
        return _r

    def lowres3(self, fromx=1, tox=-1, fromy=1, toy=-1):
        r = self.mean3x3()
        r = r.crop(3, fromx=fromx, tox=tox, fromy=fromy, toy=toy)
        return r

    @property
    def res(self):
        return self._flag['RES']

    @property
    def latrange(self):
        return (self.lat[:,0].min(), self.lat[:,0].max())

    @property
    def longrange(self):
        return (self.long[0,:].min(), self.long[0,:].max())

    @property
    def anchor(self):
        return self.lat[:,0].min(), self.long[0,:].min()

    @property
    def lat1d(self):
        return self.lat[:,0]

    @property
    def long1d(self):
        return self.long[0,:]

    def cut(self, interv: int, fromx, fromy):
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
    
    def cutup(self, interv: int): 
        coorlist = []
        for i in range(self.lat.shape[0]//interv):
            for j in range(self.long.shape[1]//interv):
                coorlist.append((i*interv, j*interv))
        r = []
        for coor in coorlist:
            r.append(self.cut(interv, coor[1], coor[0]))
        return r

    def cut3nup(self):
        ilist = []
        while 3**(len(ilist)+1) < np.min(self.lat.shape) and 3**(len(ilist)+1) < np.min(self.long.shape):
            ilist.append(3**(len(ilist)+1))
        r = []
        for interv in ilist:
            r.append(self.cutup(interv))
        return r

    @property
    def timestr(self):
        return f'{str(self.time)[:4]}{str(self.time)[5:7]}{str(self.time)[8:10]}{str(self.time)[11:13]}{str(self.time)[14:16]}{str(self.time)[17:19]}'

    @property
    def timeobj(self):
        return ascl.dt(self.timestr)

class voidFrame(frame):
    def __init__(self, lat, long, time):
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

def findanchor(li: list, lat, lon):
    for l in li:
        if l.anchor == (lat, lon):
            return l
    return nullFrame()

def correspond(hrdf, lrdf, len, lx, ly):
    thinGrid = hrdf.cut(len*lrdf.res(), lx*lrdf.res(), ly*lrdf.res())
    thickGrid= lrdf.cut(len*hrdf.res(), lx*hrdf.res(), ly*hrdf.res())
    return thinGrid, thickGrid

def to_ts_wpframe(lf):
    _s1 = apts.wpframe(lat=lf[0].lat, long=lf[0].long)
    for r in lf:
        _s1[r.timestr] = r
    return _s1

def issmallgrid(grid: frame, threshold):
    return grid.res < threshold