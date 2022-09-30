# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import ascl
import pandas as pd

SERIES_DEFAULT_ATTRS = {
    'ref': ascl.dt.udf
}

UDF_ALIASES = ('u', 'U', 'unix', 'UNIX', ascl.dt.udf)
USF_ALIASES = ('us', 'US', 'Us', 'unixs', 'UNIXs','unix_s', 'UNIX_s', 'unix_sec', 'UNIX_sec', ascl.dt.usf)
MDF_ALIASES = ('m', 'M', 'mill', 'millenium', ascl.dt.mdf)
MSF_ALIASES = ('ms', 'MS', 'Ms', 'mills', 'milleniums','mill_s', 'millenium_s', 'mill_sec', 'millenium_sec', ascl.dt.msf)
MJDF_ALIASES = ('mjd', 'MJD', 'mj', 'MJ', ascl.dt.mjdf)
MJSF_ALIASES = ('mjds', 'MJDS', 'mjs', 'MJS', 'mjd_s', 'MJD_s', 'mj_s', 'MJ_s', 'mjd_sec', 'MJD_sec', 'mj_sec', 'MJ_sec', ascl.dt.mjsf)
ADF_ALIASES = ('a', 'A', 'ad', 'AD', ascl.dt.adf)
ADSF_ALIASES = ('as', 'AS', 'As', 'ads', 'ADs', 'ADS', 'ad_s', 'AD_s', 'ad_sec', 'AD_sec', ascl.dt.adsf)

class series:

    def __init__(self, **kwargs):
        self.time = []
        self.data = []
        self._attr = {}
        for kw in SERIES_DEFAULT_ATTRS.keys():
            self._attr[kw] = SERIES_DEFAULT_ATTRS[kw]
        for kw in kwargs.keys():
            if kw == 'time':
                for t in kwargs[kw]:
                    self.time.append(t)
            elif kw == 'data':
                for d in kwargs[kw]:
                    self.data.append(d)
            else:
                self._attr[kw] = kwargs[kw]

    @property
    def dtime(self):
        return [ascl.dt(t) for t in self.time]

    def __getitem__(self, t):
        if isinstance(t, ascl.dt):
            try:
                return self.data[self.time.index(t())]
            except:
                raise RuntimeError('Target time not found in the series')
        else:
            try:
                return self.data[self.time.index(t)]
            except:
                raise RuntimeError('Target time not found in the series')

    def __setitem__(self, t, values):
        if isinstance(t, ascl.dt):
            try:
                _index = self.time.index(t())
                self.data[_index] = values
            except:
                self.time.append(t())
                self.data.append(values)
                self.sort()
        else:
            try:
                _index = self.time.index(t)
                self.data[_index] = values
            except:
                self.time.append(t)
                self.data.append(values)
                self.sort()

    def sort(self):
        indices = np.argsort(self.ntime)
        _r = list(zip(*np.array(list(zip(self.time, self.data)))[indices]))
        for i in range(len(_r[0])):
            self.time[i] = _r[0][i]
            self.data[i] = _r[1][i]

    def ref(self, time):
        if self._attr['ref'] in UDF_ALIASES:
            return ascl.dt.udf(time)
        elif self._attr['ref'] in USF_ALIASES:
            return ascl.dt.usf(time)
        elif self._attr['ref'] in MDF_ALIASES:
            return ascl.dt.mdf(time)
        elif self._attr['ref'] in MSF_ALIASES:
            return ascl.dt.msf(time)
        elif self._attr['ref'] in MJDF_ALIASES:
            return ascl.dt.mjdf(time)
        elif self._attr['ref'] in MJSF_ALIASES:
            return ascl.dt.mjsf(time)
        elif self._attr['ref'] in ADF_ALIASES:
            return ascl.dt.adf(time)
        elif self._attr['ref'] in ADSF_ALIASES:
            return ascl.dt.adsf(time)

    @property
    def ntime(self):
        return [self.ref(t) for t in self.dtime]

    def index(self, t):
        if isinstance(t, ascl.dt):
            try:
                return self.time.index(t())
            except:
                return -1
        else:
            try:
                return self.time.index(t)
            except:
                return -1
    
    def period(self, start, end):

        if isinstance(start, str):
            start_ref = self.ref(ascl.dt(start))
        elif isinstance(start, ascl.dt):
            start_ref = self.ref(start)
        else:
            raise RuntimeError('\'start\' must be a str or ascl.dt')

        if isinstance(end, str):
            end_ref = self.ref(ascl.dt(end))
        elif isinstance(end, ascl.dt):
            end_ref = self.ref(end)
        elif isinstance(end, int) or isinstance(end, float):
            if isinstance(start, str):
                end_ref = self.ref(ascl.dt(start) + end)
            elif isinstance(start, ascl.dt):
                end_ref = self.ref(start + end)

        if start_ref > end_ref:
            start_ref, end_ref = end_ref, start_ref

        start_i = 0
        for i, nt in enumerate(self.ntime):
            if nt >= start_ref:
                start_i = i
                break
        for i, nt in enumerate(self.ntime):
            if nt > end_ref:
                end_i = i
                break
            end_i = i + 1
        return [self.time[start_i:end_i], self.data[start_i:end_i]]

    def sub(self, start, end, **kwargs):
        _r = self.period(start, end)
        return series(time=_r[0], data=_r[1], **kwargs)

    def iterate(self, f):
        _r = [f(d) for d in self.data]
        return _r

    def operation(self, f):
        _r = [f(d) for d in self.data]
        return series(time=self.time, data=_r)

class val(series):
    pass

class array(series):
    pass

class gis(series):

    def __init__(self, **kwargs):
        self.time = []
        self.data = []
        self._attr = {}
        for kw in SERIES_DEFAULT_ATTRS.keys():
            self._attr[kw] = SERIES_DEFAULT_ATTRS[kw]
        for kw in kwargs.keys():
            if kw == 'time':
                for t in kwargs[kw]:
                    self.time.append(t)
            elif kw == 'data':
                for d in kwargs[kw]:
                    self.data.append(d)
            elif kw == 'lat':
                self.lat = kwargs[kw]
            elif kw == 'long':
                self.long = kwargs[kw]
            else:
                self._attr[kw] = kwargs[kw]

    def subgis(self, start, end, **kwargs):
        _r = self.period(start, end)
        return gis(time=_r[0], data=_r[1], lat=self.lat, long=self.long, **kwargs)

    def temporalmean(self, f, pack=False):
        _r = np.nanmean(np.array(self.iterate(f)), axis=0)
        return [self.long, self.lat, _r] if pack else _r