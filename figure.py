# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class figure:
    
    def __init__(self, **kwargs):
        self._attr = {}
        self._formats = {}
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]

    def _init_with(self, dic, **kwargs):
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
        return self._attr[key]

    def set(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        return self

    def format(self, **kwargs):
        for kw in kwargs.keys():
            self._formats[kw] = kwargs[kw]
        self['format'] = True            
        return self

    def __call__(self):
        pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

HEAT_DEFAULT_ATTRS = {
    
}

class heat(figure):
    def __init__(self, **kwargs):
        self._init_with(HEAT_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'X' in self._attr.keys():
            plt.imshow(self['X'], **self._formats)
        else:
            raise RuntimeError('No data')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

SCATTER_DEFAULT_ATTRS = {

}

class scatter(figure):
    def __init__(self, **kwargs):
        self._init_with(SCATTER_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys():
            self['x'] = np.array(self['x']).reshape(-1)
            self['y'] = np.array(self['y']).reshape(-1)
            if self['x'].shape != self['y'].shape:
                raise RuntimeError('x and y should be in the same shape')
            else:
                for x, y in zip(self['x'],self['y']):
                    plt.plot(x, y, '.', **self._formats)
        elif 'xy' in self._attr.keys():
            for xy in self['xy']:
                plt.plot(*xy, '.', **self._formats)
        else:
            raise RuntimeError('No data')
            
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

FUNC_DEFAULT_ATTRS = {
    'xrange': [-10,10],
    'step': 1e-3,
}

class func(figure):
    def __init__(self, **kwargs):
        self._init_with(FUNC_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'f' in self._attr.keys():
            x = np.arange(*self['xrange'], self['step'])
            plt.plot(x, self['f'](x), **self._formats)
        else:
            raise RuntimeError('No data')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

FOLDLINE_DEFAULT_ATTRS = {

}

class foldline(figure):

    def __init__(self, **kwargs):
        self._init_with(FOLDLINE_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys():
            plt.plot(self['x'], self['y'], **self._formats)
        else:
            raise RuntimeError('No data')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

DOTLINE_DEFAULT_ATTRS = {

}

class dotline(figure):
    def __init__(self, **kwargs):
        self._dformats = {}
        self._lformats = {}
        self._init_with(DOTLINE_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys():
            self['x'] = np.array(self['x']).reshape(-1)
            self['y'] = np.array(self['y']).reshape(-1)
            if self['x'].shape != self['y'].shape:
                raise RuntimeError('x and y should be in the same shape')
            else:
                plt.plot(self['x'], self['y'], **self._lformats)
                for x, y in zip(self['x'],self['y']):
                    plt.plot(x, y, '.', **self._dformats)
        else:
            raise RuntimeError('No data')
    
    def dformat(self, **kwargs):
        for kw in kwargs.keys():
            self._dformats[kw] = kwargs[kw]
        self['format'] = True            
        return self

    def lformat(self, **kwargs):
        for kw in kwargs.keys():
            self._lformats[kw] = kwargs[kw]
        self['format'] = True            
        return self

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

CONTOURF_DEFAULT_ATTRS = {
    'clabel': False,
}

class contourf(figure):
    def __init__(self, **kwargs):
        self._init_with(CONTOURF_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys() and 'z' in self._attr.keys():
            try:
                plt.contourf(self['x'], self['y'], self['z'], **self._formats)
            except:
                self['x'] = np.array(self['x']).reshape(-1)
                self['y'] = np.array(self['y']).reshape(-1)
                self['z'] = np.array(self['z']).reshape(-1)
                plt.contourf(self['x'], self['y'], self['z'], **self._formats)
        else:
            raise RuntimeError('No data')

    def format_levelnumbers(self, x: int):
        self._formats['levels'] = np.arange(np.min(self['z']), np.max(self['z']) + (np.max(self['z'])-np.min(self['z']))/float(x), (np.max(self['z'])-np.min(self['z']))/float(x))
        return self

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

CONTOUR_DEFAULT_ATTRS = {
    'clabel': False,
}

class contour(figure):
    def __init__(self, **kwargs):
        self._init_with(CONTOUR_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys() and 'z' in self._attr.keys():
            try:
                if self['clabel']:
                    C = plt.contour(self['x'], self['y'], self['z'], **self._formats)
                    plt.clabel(C, **self['clabel_format'])
                else:
                    plt.contour(self['x'], self['y'], self['z'], **self._formats)
            except:
                self['x'] = np.array(self['x']).reshape(-1)
                self['y'] = np.array(self['y']).reshape(-1)
                self['z'] = np.array(self['z']).reshape(-1)
                if self['clabel']:
                    C = plt.contour(self['x'], self['y'], self['z'], **self._formats)
                    plt.clabel(C, **self['clabel_format'])
                else:
                    plt.contour(self['x'], self['y'], self['z'], **self._formats)
        else:
            raise RuntimeError('No data')

    def format_levelnumbers(self, x: int):
        self._formats['levels'] = np.arange(np.min(self['z']), np.max(self['z']) + (np.max(self['z'])-np.min(self['z']))/float(x), (np.max(self['z'])-np.min(self['z']))/float(x))
        return self

    def clabel(self, **kwargs):
        self['clabel'] = True
        self['clabel_format'] = kwargs
        return self
            
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

AXES_DEFAULT_ATTRS = {

}

class axes(figure):

    def __init__(self, **kwargs):
        self._init_with(AXES_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys():
            self['x'] = np.array(self['x']).reshape(-1)
            for x in self['x']:
                plt.axvline(x, **self._formats)
        if 'y' in self._attr.keys():
            self['y'] = np.array(self['y']).reshape(-1)
            for y in self['y']:
                plt.axhline(y, **self._formats)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

LLS_DEFAULT_ATTRS = {
    'lat': 0,
    'long': 0,
    'latref': -90,
    'latref2': 90,
    'longref': -180,
    'longref2': 180,
}

class lls(figure):

    def __init__(self, **kwargs):
        self._init_with(LLS_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'lls' in self._attr.keys():
            self['lat'], self['long'] = self['lls'], self['lls']
        if self['lat']:
            for x in np.arange(self['latref'], self['latref2'], self['lat']):
                plt.axhline(x, **self._formats)
        if self['long']:
            for y in np.arange(self['longref'], self['longref2'], self['long']):
                plt.axvline(y, **self._formats)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

TRACK_DEFAULT_ATTRS = {
    'zfargs': [],
}

TRACK_DEFAULT_LFORMATS = {
    'lw': .5,
    'c': 'w',
}

class track(dotline):

    def __init__(self, **kwargs):
        self._lformats = {}
        for kw in TRACK_DEFAULT_LFORMATS.keys():
            self._lformats[kw] = TRACK_DEFAULT_LFORMATS[kw]
        self._init_with(TRACK_DEFAULT_ATTRS, **kwargs)

    def __call__(self):
        if 'x' in self._attr.keys() and 'y' in self._attr.keys():
            self['x'] = np.array(self['x']).reshape(-1)
            self['y'] = np.array(self['y']).reshape(-1)
            self['z'] = np.array(self['z']).reshape(-1)
            if self['x'].shape != self['y'].shape or self['x'].shape != self['z'].shape or self['y'].shape != self['z'].shape:
                raise RuntimeError('x, y and z should be in the same shape')
            else:
                plt.plot(self['x'], self['y'], **self._lformats)
                if len(self['zfargs']):
                    for i in range(len(self['x'])):
                        plt.plot(self['x'][i], self['y'][i], **self['f'](self['z'][i], *self['zfargs'][i]))
                else:
                    for i in range(len(self['x'])):
                        plt.plot(self['x'][i], self['y'][i], **self['f'](self['z'][i]))
        else:
            raise RuntimeError('No data')

    @staticmethod
    def sshws(inten):
        if inten < 25:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([128,204,255])/256.}
        elif inten < 34:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([ 94,186,255])/256.}
        elif inten < 64:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([  0,255,244])/256.}
        elif inten < 82:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,255,204])/256.}
        elif inten < 96:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,231,117])/256.}
        elif inten < 112:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,193, 64])/256.}
        elif inten < 137:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,143, 32])/256.}
        else:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255, 96, 96])/256.}