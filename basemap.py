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

    # 初始化，指定投影，分辨率和地图边界
    def init(self):
        try:
            self._base = Basemap(projection=self['proj'], llcrnrlon = self['long'][0], llcrnrlat = self['lat'][0], 
                    urcrnrlon = self['long'][1], urcrnrlat = self['lat'][1], resolution=self['res'])
        except:
            raise RuntimeError('More attributes needed!')
        return self._base

    # 绘制海岸线（当且仅当边界内有海岸线的时候）
    def drawcoastlines(self):
        if len(self._base.coastsegs) and len(self._base.coastsegs[0]):
            self._base.drawcoastlines(color=self._attr['clcolor'], linewidth=self._attr['cllw'])
        return self._base

    # 使用彩色背景（预设）
    def colorbg(self, style=None):
        if style == 'bluemarble':
            self._base.bluemarble(scale=self._attr['clbgs'])
        if style == 'shadedrelief':
            self._base.shadedrelief(scale=self._attr['clbgs'])
        if style == 'etopo':
            self._base.etopo(scale=self._attr['clbgs'])
        return self._base

    # 画经纬度线的操作
    def lldraw(self):
        if self['grid'] == 'grid':
            self._base.drawparallels(np.arange(self['latref'], self['latref2'], self['latinv']), labels=[1,0,0,0],
                                        color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
            self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self['longinv']), labels=[0,0,0,1],
                                        color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
        elif self['grid'] == 'lls':
            self._base.drawparallels(np.arange(self['latref'], self['latref2'], self._lls['inv']), labels=[1,0,0,0],
                                         color=self._lls['c'], linewidth=self._lls['lw'], fontsize=self._lls['fs'])
            self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self._lls['inv']), labels=[0,0,0,1],
                                         color=self._lls['c'], linewidth=self._lls['lw'], fontsize=self._lls['fs'])
        elif self['grid'] == 'latslongs':
            self._latssub = {'inv': 0, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10}
            self._longssub = {'inv': 0, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10}
            for kw in self._lats.keys():
                self._latssub[kw] = self._lats[kw]
                if self._latssub['inv']:
                    self._base.drawparallels(np.arange(self['latref'], self['latref2'], self._latssub['inv']), labels=[1,0,0,0],
                                         color=self._latssub['c'], linewidth=self._latssub['lw'], linestyle=self._latssub['ls'], fontsize=self._latssub['fs'])
            for kw in self._longs.keys():
                self._longssub[kw] = self._longs[kw]
                if self._latssub['inv']:
                    self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self._longssub['inv']), labels=[0,0,0,1],
                                         color=self._longssub['c'], linewidth=self._longssub['lw'], linestyle=self._longssub['ls'], fontsize=self._longssub['fs'])

    


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # 以下是返回self的函数
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # 画经纬度线（完整版设置）
    def grid(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self['grid'] = 'grid'
        # if int(self._attr['latinv']):
            # self._base.drawparallels(np.arange(self['latref'], self['latref2'], self['latinv']), labels=[1,0,0,0],
            #                             color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
        # if int(self._attr['longinv']):
            # self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self['longinv']), labels=[0,0,0,1],
            #                             color=self['gridc'], linewidth=self['gridlw'], linestyle=self['gridls'], fontsize=self['gfontsize'])
        return self

    # 画经纬度线（快捷版设置）
    def lls(self, inv, **kwargs):
        self._lls = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10,}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'lls'
        # self._base.drawparallels(np.arange(self['latref'], self['latref2'], self._lls['inv']), labels=[1,0,0,0],
        #                                 color=self._lls['c'], linewidth=self._lls['lw'], linestyle=self._lls['ls'], fontsize=self._lls['fs'])
        # self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self._lls['inv']), labels=[0,0,0,1],
        #                                 color=self._lls['c'], linewidth=self._lls['lw'], linestyle=self._lls['ls'], fontsize=self._lls['fs'])
        return self
    
    # 画经度线（快速设置）
    def longs(self, inv, **kwargs):
        self._longs = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10,}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'latslongs'
        # self._base.drawmeridians(np.arange(self['longref'], self['longref2'], self._lls['inv']), labels=[0,0,0,1],
        #                                 color=self._lls['c'], linewidth=self._lls['lw'], linestyle=self._lls['ls'], fontsize=self._lls['fs'])
        return self

    # 画纬度线（快速设置）
    def lats(self, inv, **kwargs):
        self._lats = {'inv': inv, 'c': 'k', 'lw': 1, 'ls': '-', 'fs': 10,}
        for kw in kwargs.keys():
            self._lls[kw] = kwargs[kw]
        self['grid'] = 'latslongs'
        # self._base.drawparallels(np.arange(self['latref'], self['latref2'], self._lls['inv']), labels=[1,0,0,0],
        #                                 color=self._lls['c'], linewidth=self._lls['lw'], linestyle=self._lls['ls'], fontsize=self._lls['fs'])
        return self

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class imageB(image):
    
    def __init__(self, basemap: basemap):
        self._attr = {}
        for kw in IMG_DEFAULT_ATTRS.keys():
            self._attr[kw] = IMG_DEFAULT_ATTRS[kw]
        for kw in basemap._attr.keys():
            self._attr[kw] = basemap[kw]
        self.preset()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

BASIC_DEFAULT_ATTRS = {
    'proj'      :   'cyl',          # changed from 'cea'
    'long'      :   [-180.,180.],
    'lat'       :   [-90.,90.],
    'res'       :   'c',

    # 画经纬度时的参数
    'grid'      :   'default',
    'gridc'     :   'k',       # color of parallels and meridians
    'gridlw'    :   0.5,            # linewidth of parallels and meridians
    'gfontsize' :   12,
    'gridls'    :   '-',

    # 画经纬度线时的参考点
    'latinv': 0,
    'longinv': 0,
    'latref': -90,
    'latref2': 90,
    'longref': -180,
    'longref2': 179,
}
# 空白地图
class blank(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self._base = self.init()
        self.lldraw()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

COAST_DEFAULT_ATTRS = {
    'clcolor'   :   'k',            # coastline $color
    'cllw'      :   1.,             # coastline $linewidth
}
# 带海岸线的地图
class coast(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **COAST_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self.init()
        self._base = self.drawcoastlines()
        self.lldraw()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

CLBG_DEFAULT_ATTRS = {
    'clbgs'     :   0.5,            # colored backgrounds $scale
}
# 用内置的bluemarble或shadedrelief或etopo作为底图的地图，默认不画海岸线
class bluemarble(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self.init()
        self['clbg'] = 'bluemarble'
        self._base = self.colorbg('bluemarble')
        self.lldraw()
        if show:
            plt.show()
        return self._base

class shadedrelief(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self.init()
        self['clbg'] = 'shadedrelief'
        self._base = self.colorbg('shadedrelief')
        self.lldraw()
        if show:
            plt.show()
        return self._base

class etopo(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self.init()
        self['clbg'] = 'etopo'
        self._base = self.colorbg('etopo')
        self.lldraw()
        if show:
            plt.show()
        return self._base

class colorbg(basemap):

    def __init__(self, **kwargs):
        self._init_with(BASIC_DEFAULT_ATTRS, **CLBG_DEFAULT_ATTRS, **kwargs)

    def out(self, show=False):
        self.init()
        if 'clbg' in self._attr.keys():
            self._base = self.colorbg(self['clbg'])
        self.lldraw()
        if show:
            plt.show()
        return self._base

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 