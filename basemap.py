# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from .main import image
from .main import IMG_DEFAULT_ATTRS
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class basemap:

    _base = Basemap()
    def _init_with(self, dic: dict, **kwargs):
        self._attr = {}
        self._formats = {}
        for kw in dic.keys():
            self._attr[kw] = dic[kw]
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]

    def __getitem__(self, key):
        return self._attr[key]

    def __setitem__(self, key, value):
        self._attr[key] = value
        return self

    def set(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        return self

    def init(self):
        try:
            self._base = Basemap(projection=self['proj'], llcrnrlon = self['long'][0], llcrnrlat = self['lat'][0], 
                    urcrnrlon = self['long'][1], urcrnrlat = self['lat'][1], resolution=self['res'])
        except:
            raise RuntimeError('More attributes needed!')
        return self._base

    def drawcoastlines(self):
        if 'coastline_func' in self._attr.keys():
            if 'c' in self._coastlines.keys():
                self['clcolor'] = self._coastlines['c']
            if 'color' in self._coastlines.keys():
                self['clcolor'] = self._coastlines['color']
            if 'lw' in self._coastlines.keys():
                self['cllw'] = self._coastlines['lw']
            if 'linewidth' in self._coastlines.keys():
                self['cllw'] = self._coastlines['linewidth']
        if len(self._base.coastsegs) and len(self._base.coastsegs[0]):
            self._base.drawcoastlines(color=self._attr['clcolor'], linewidth=self._attr['cllw'])
        return self._base

    def colorbg(self, style=None):
        if style == 'bluemarble':
            self._base.bluemarble(scale=self._attr['clbgs'])
        if style == 'shadedrelief':
            self._base.shadedrelief(scale=self._attr['clbgs'])
        if style == 'etopo':
            self._base.etopo(scale=self._attr['clbgs'])
        return self._base

    def lldraw(self):
        if self['grid'] == 'grid':
            self._base.drawparallels(np.arange(self['latref'], self['latref2'], self['latinv']), labels=[1,0,0,0],
                                        color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
            self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self['longinv']), labels=[0,0,0,1],
                                        color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
        elif self['grid'] == 'lls':
            self._base.drawparallels(np.arange(self._lls['latref'], self._lls['latref2'], self._lls['inv']), labels=[1,0,0,0],
                                         color=self._lls['c'], linewidth=self._lls['lw'], fontsize=self._lls['fs'])
            self._base.drawmeridians(np.arange(self._lls['longref'], self._lls['longref2'], self._lls['inv']), labels=[0,0,0,1],
                                         color=self._lls['c'], linewidth=self._lls['lw'], fontsize=self._lls['fs'])
        elif self['grid'] == 'latslongs':
            self._latssub = {'inv': 0, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10}
            self._longssub = {'inv': 0, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10}
            for kw in self._lats.keys():
                self._latssub[kw] = self._lats[kw]
                if self._latssub['inv']:
                    self._base.drawparallels(np.arange(self._latssub['latref'], self._latssub['latref2'], self._latssub['inv']), labels=[1,0,0,0],
                                         color=self._latssub['c'], linewidth=self._latssub['lw'], linestyle=self._latssub['ls'], fontsize=self._latssub['fs'])
            for kw in self._longs.keys():
                self._longssub[kw] = self._longs[kw]
                if self._latssub['inv']:
                    self._base.drawmeridians(np.arange(self._longssub['longref'], self._longssub['longref2'], self._longssub['inv']), labels=[0,0,0,1],
                                         color=self._longssub['c'], linewidth=self._longssub['lw'], linestyle=self._longssub['ls'], fontsize=self._longssub['fs'])

    def ifcoast(self):
        if 'coastline_func' in self._attr.keys():
            self.drawcoastlines()
            return True
        else:
            return False

    def extraproc(self):
        self.ifcoast()
        self.lldraw()

    def grid(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self['grid'] = 'grid'
        return self

    def lls(self, inv, **kwargs):
        self._lls = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10, 'latref': -90, 'latref2': 90, 'longref': -180, 'longref2': 180}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'lls'
        return self
    
    def longs(self, inv, **kwargs):
        self._longs = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10, 'latref': -90, 'latref2': 90, 'longref': -180, 'longref2': 180}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'latslongs'
        return self

    def lats(self, inv, **kwargs):
        self._lats = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10, 'latref': -90, 'latref2': 90, 'longref': -180, 'longref2': 180}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'latslongs'
        return self

    def coastlines(self, **kwargs):
        self._coastlines = {}
        for kw in COAST_DEFAULT_ATTRS.keys():
            self._attr[kw] = COAST_DEFAULT_ATTRS[kw]
        for kw in kwargs:
            self._coastlines[kw] = kwargs[kw]
        self['coastline_func'] = True
        return self

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

BASIC_DEFAULT_ATTRS = {
    'proj'      :   'cyl',
    'long'      :   [-180.,180.],
    'lat'       :   [-90.,90.],
    'res'       :   'c',

    'grid'      :   'default',
    'gridc'     :   'k',
    'gridlw'    :   0.5,
    'gfontsize' :   12,
    'gridls'    :   '-',

    'latinv': 0,
    'longinv': 0,
    'latref': -90,
    'latref2': 90,
    'longref': -180,
    'longref2': 179,
}

class blank(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self._base = self.init()
        self.extraproc()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

COAST_DEFAULT_ATTRS = {
    'clcolor'   :   'k',
    'cllw'      :   1.,
}

class coast(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **COAST_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self.init()
        self._base = self.drawcoastlines()
        self.extraproc()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

CLBG_DEFAULT_ATTRS = {
    'clbgs'     :   0.5,
}

class bluemarble(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self.init()
        self['clbg'] = 'bluemarble'
        self._base = self.colorbg('bluemarble')
        self.extraproc()
        if show:
            plt.show()
        return self._base

class shadedrelief(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self.init()
        self['clbg'] = 'shadedrelief'
        self._base = self.colorbg('shadedrelief')
        self.extraproc()
        if show:
            plt.show()
        return self._base

class etopo(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self.init()
        self['clbg'] = 'etopo'
        self._base = self.colorbg('etopo')
        self.extraproc()
        if show:
            plt.show()
        return self._base

class colorbg(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def __call__(self, show=False):
        self.init()
        if 'clbg' in self._attr.keys():
            self._base = self.colorbg(self['clbg'])
        self.extraproc()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 