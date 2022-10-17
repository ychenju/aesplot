# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import ascl
from typing import Sequence, Union, Callable

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

    def __init__(self, **kwargs) -> None:
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
    def dtime(self) -> list:
        return [ascl.dt(t) for t in self.time]

    def __getitem__(self, t:Union[str, ascl.dt]):
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

    def __setitem__(self, t:Union[str, ascl.dt], values) -> None:
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
        return self

    def ref(self, time:ascl.dt) -> float:
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
    def ntime(self) -> list:
        return [self.ref(t) for t in self.dtime]

    @property
    def len(self) -> int:
        return len(self.time)

    def index(self, t:Union[str, ascl.dt]) -> int:
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
    
    def period(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float]) -> list:
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

    def sub(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], **kwargs):
        _r = self.period(start, end)
        return series(time=_r[0], data=_r[1], **kwargs)

    def split(self, n:int) -> list:
        return [series(time=self.time[i::n], data=self.data[i::n]) for i in range(n)]

    def iterate(self, f:Callable=lambda x: x) -> list:
        _r = [f(d) for d in self.data]
        return _r

    def iter(self, f:Callable=lambda x: x) -> list:
        _r = [f(d) for d in self.data]
        return _r

    def operation(self, f:Callable=lambda x: x):
        _r = [f(d) for d in self.data]
        return series(time=self.time, data=_r)

    def opera(self, f:Callable=lambda x: x):
        _r = [f(d) for d in self.data]
        return series(time=self.time, data=_r)

    def sum(self, f:Callable=lambda x: x) -> float:
        _r = np.array([f(d) for d in self.data])
        return np.sum(_r)

    def mean(self, f:Callable=lambda x: x) -> float:
        _r = np.array([f(d) for d in self.data])
        return np.mean(_r)

    def nanmean(self, f:Callable=lambda x: x) -> float:
        _r = np.array([f(d) for d in self.data])
        return np.nanmean(_r)

    def subiterate(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> list:
        _s = self.sub(start, end)
        _r = np.array([f(d) for d in _s.data])
        return _r

    def suboperation(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x):
        _s = self.sub(start, end)
        _r = np.array([f(d) for d in _s.data])
        return series(time=_s.time, data=_r)

    def subsum(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        _r = np.array([f(d) for d in _s.data])
        return np.sum(_r)

    def submean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        _r = np.array([f(d) for d in _s.data])
        return np.mean(_r)

    def subnanmean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        _r = np.array([f(d) for d in _s.data])
        return np.nanmean(_r)

class val(series):

    def sum(self, f:Callable=lambda x: x) -> float:
        return np.sum(np.array(self.data))
    
    def mean(self, f:Callable=lambda x: x) -> float:
        return np.mean(np.array(self.data))

    def nanmean(self, f:Callable=lambda x: x) -> float:
        return np.nanmean(np.array(self.data))

    def subsum(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        return np.sum(np.array(_s.data))

    def submean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        return np.mean(np.array(_s.data))

    def subnanmean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> float:
        _s = self.sub(start, end)
        return np.nanmean(np.array(_s.data))

class array(series):

    def sum(self, f:Callable=lambda x: x) -> np.ndarray:
        return np.sum(np.array(self.data), axis=0)
    
    def mean(self, f:Callable=lambda x: x) -> np.ndarray:
        return np.mean(np.array(self.data), axis=0)

    def nanmean(self, f:Callable=lambda x: x) -> np.ndarray:
        return np.nanmean(np.array(self.data), axis=0)

    def subsum(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.sum(np.array(_s.data), axis=0)

    def submean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.mean(np.array(_s.data), axis=0)

    def subnanmean(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.nanmean(np.array(_s.data), axis=0)

class array1(array):
    pass

class array2(array):
    pass

class gis(series):

    def __init__(self, **kwargs) -> None:
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

    def subgis(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], **kwargs) -> series:
        _r = self.period(start, end)
        return gis(time=_r[0], data=_r[1], lat=self.lat, long=self.long, **kwargs)

    def meanfield(self, f:Callable=lambda x: x, pack:bool=False) -> Union[Sequence[np.ndarray], np.ndarray]:
        _r = np.nanmean(np.array(self.iterate(f)), axis=0)
        return [self.long, self.lat, _r] if pack else _r

class wpframe(gis):

    def meanfield(self, var:str, pack:bool=False) -> Union[Sequence[np.ndarray], np.ndarray]:
        _r = np.nanmean(np.array([d[var] for d in self.data]), axis=0)
        return [self.long, self.lat, _r] if pack else _r

    def subvar(self, var:str, **kwargs) -> array2:
        _r = [d[var] for d in self.data]
        return array2(time=self.time, data=_r, **kwargs)

    def subwpf(self, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], **kwargs) -> series:
        _r = self.period(start, end)
        return wpframe(time=_r[0], data=_r[1], lat=self.lat, long=self.long, **kwargs)

    def sum(self, var:str) -> np.ndarray:
        return np.sum(np.array([d[var] for d in self.data]), axis=0)

    def mean(self, var:str) -> np.ndarray:
        return np.mean(np.array([d[var] for d in self.data]), axis=0)

    def nanmean(self, var:str) -> np.ndarray:
        return np.nanmean(np.array([d[var] for d in self.data]), axis=0)

    def subsum(self, var:str, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.sum(np.array([d[var] for d in _s.data]), axis=0)

    def submean(self, var:str, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.mean(np.array([d[var] for d in _s.data]), axis=0)

    def subnanmean(self, var:str, start:Union[str, ascl.dt], end:Union[str, ascl.dt, int, float], f:Callable=lambda x: x) -> np.ndarray:
        _s = self.sub(start, end)
        return np.nanmean(np.array([d[var] for d in _s.data]), axis=0)