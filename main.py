# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from . import settings

IMG_DEFAULT_ATTRS = {
    'font': 'default',
    'preset': False,
    'saveas': 'default',
    'serif': 'sans-serif',
}

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   

class image:

    def __init__(self, **kwargs):
        self._attr = {}
        for kw in IMG_DEFAULT_ATTRS.keys():
            self._attr[kw] = IMG_DEFAULT_ATTRS[kw]
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self.preset()

    def __getitem__(self, key:str):
        return self._attr[key]

    def __setitem__(self, key:str, value):
        self._attr[key] = value
        return self._attr[key]

    def reset(self, **kwargs):
        self._attr = {}
        for kw in IMG_DEFAULT_ATTRS.keys():
            self._attr[kw] = IMG_DEFAULT_ATTRS[kw]
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self.preset()
        return self

    def clear(self):
        plt.clf()
        return self

    def restart(self, **kwargs):
        plt.clf()
        self._attr = {}
        for kw in IMG_DEFAULT_ATTRS.keys():
            self._attr[kw] = IMG_DEFAULT_ATTRS[kw]
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self.preset()
        return self

    def preset(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        if self['font'] != 'default':
            if self['serif'] == 'sans-serif':
                settings.sans_serif(self['font'])
        _figattr = {}
        if 'figsize' in self._attr.keys():
            _figattr['figsize'] = self['figsize']
        if 'dpi' in self._attr.keys():
            _figattr['dpi'] = self['dpi']
        if 'facecolor' in self._attr.keys():
            _figattr['facecolor'] = self['facecolor']
        if 'edgecolor' in self._attr.keys():
            _figattr['edgecolor'] = self['edgecolor']
        if len(_figattr.keys()):
            plt.figure(**_figattr)
        else:
            plt.figure()
        self['preset'] == True
        return self

    def set(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        return self

    def add(self, *figs:tuple):
        for fig in figs:
            try:
                fig()
            except:
                print(f'Failed to add the object \'{fig}\'')
        return self

    def addbasemap(self, *bmps:tuple):
        for bmp in bmps:
            try:
                bmp()
            except:
                print(f'Failed to add the Basemap object \'{bmp}\'')
        return self

    def addbaseNmask(self, bmp, mask):
        self.addbasemap(bmp)
        self.add(mask)
        return self

    def formatting(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        self.setaxes()
        self.labels()
        setf.grid(self)
        return self

    def setaxes(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        setf.xlim(self)
        setf.ylim(self)
        setf.xticks(self)
        setf.yticks(self)
        return self

    def labels(self, **kwargs):
        for kw in kwargs.keys():
            self._attr[kw] = kwargs[kw]
        setf.xlabel(self)
        setf.ylabel(self)
        setf.title(self)
        return self

    def save(self, path:str='\r\n'):
        if path != '\r\n':
            self['saveas'] = path
        try:
            plt.savefig(self['saveas'])
        except:
            raise RuntimeError('Output path (\'saveas\' attr) required.')
        return self

    def colorbar(self, **kwargs):
        plt.colorbar(**kwargs)
        return self

    def show(self):
        plt.show()
        return self

class setf:

    @staticmethod
    def xlim(img:image):
        if 'xlim' in img._attr.keys():
            plt.xlim(*img['xlim'])

    @staticmethod
    def ylim(img:image):
        if 'ylim' in img._attr.keys():
            plt.ylim(*img['ylim'])

    @staticmethod
    def xticks(img:image):
        if 'xticks' in img._attr.keys():
            plt.xticks(img['xticks'])

    @staticmethod
    def yticks(img:image):
        if 'yticks' in img._attr.keys():
            plt.yticks(img['yticks'])

    @staticmethod
    def xlabel(img:image):
        if 'xlabel' in img._attr.keys():
            plt.xlabel(img['xlabel'])

    @staticmethod
    def ylabel(img:image):
        if 'ylabel' in img._attr.keys():
            plt.ylabel(img['ylabel'])

    @staticmethod
    def title(img:image):
        if 'title' in img._attr.keys():
            plt.title(img['title'])

    @staticmethod
    def grid(img:image):
        if 'grc' in img._attr.keys() or 'grls' in img._attr.keys() or 'grlw' in img._attr.keys():
            _grattr = {}
            if 'grc' in img._attr.keys():
                _grattr['c'] = img['grc']
            if 'grls' in img._attr.keys():
                _grattr['ls'] = img['grls']
            if 'grlw' in img._attr.keys():
                _grattr['lw'] = img['grlw']
            plt.grid(**_grattr)