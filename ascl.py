# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import time as system_time
from typing import Tuple, NewType, Union

GregC = NewType('GregC', Tuple[int, int, int])
YearD = NewType('YearD', Tuple[int, int])
TimeHMS = NewType('TimeHMS', Tuple[int, int, int])

class gc:

    NORMAL_MONTHS_DAYS = np.array([
        0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ])

    @staticmethod
    def read(date:str) -> GregC:
        return int(date[:4]), int(date[4:6]), int(date[6:])

    @staticmethod
    def ytype(year:int) -> int:
        if year % 400:
            if year % 100:
                if year % 4:
                    if year == 1582:
                        return -1
                    else:
                        return 0
                else:
                    return 1
            else:
                return 0
        else:
            return 1

    @staticmethod
    def ydays(year:int) -> int:
        if gc.ytype(year) == -1:
            return 355
        else:
            return 365 + gc.ytype(year)

    @staticmethod
    def mdays(year:int, month:int) -> int:
        if month != 2 and month != 10:
            return gc.NORMAL_MONTHS_DAYS[month]
        elif month == 2:
            if gc.ytype(year) == 1:
                return 29
            else:
                return 28
        elif month == 10:
            if year == 1582:
                return 21
            else:
                return 31

    @staticmethod
    def zerostart(year:int, month:int, day:int) -> GregC:
        return year, month-1, day-1

    @staticmethod
    def onestart(year:int, month:int, day:int) -> GregC:
        return year, month+1, day+1

    @staticmethod
    def toyd_normal(year:int, month:int, day:int) -> YearD:
        return year, gc.NORMAL_MONTHS_DAYS[:month].sum() + day

    @staticmethod
    def dfix(year:int, month:int, day:int) -> int:
        if gc.ytype(year):
            if month < 3:
                return 0
            else:
                if gc.ytype(year) == 1:
                    return 1
                if gc.ytype(year) == -1:
                    if month < 10:
                        return 0
                    elif month > 10:
                        return -10
                    else:
                        if day < 5:
                            return 0
                        else:
                            return -10
        else:
            return 0

    @staticmethod
    def toyd(year:int, month:int, day:int) -> YearD:
        return gc.toyd_normal(year, month, day)[0], gc.toyd_normal(year, month, day)[1] + gc.dfix(year, month, day)

    @staticmethod
    def ydtogc(year:int, day:int) -> GregC:
        month = 0
        daysub = day
        while daysub > 0:
            month += 1
            daysub -= gc.mdays(year, month)
        return year, month, gc.mdays(year, month) + daysub

    @staticmethod
    def leap(year1:int, month1:int, day1:int, year0:int, month0:int, day0:int) -> int:
        y1, d1 = gc.toyd(year1, month1, day1)
        y0, d0 = gc.toyd(year0, month0, day0)
        if y1 > y0:
            return d1 + gc.ydays(y0) - d0 + np.array([gc.ydays(y) for y in range(y0+1,y1)] if y0+1 < y1 else [0]).sum()
        elif y1 < y0:
            return d1 - gc.ydays(y1) - d0  - np.array([gc.ydays(y) for y in range(y1+1,y0)] if y1+1 < y0 else [0]).sum()
        else:
            return d1 - d0

    @staticmethod
    def after(year:int, month:int, day:int, period:int) -> GregC:
        y, d = gc.toyd(year, month, day)
        dy = 0
        d2 = d + period
        if period > 0:
            while d2 > gc.ydays(y+dy):
                d2 -= gc.ydays(y+dy)
                dy += 1
        else:
            while d2 <= 0:
                d2 += gc.ydays(y-1+dy)
                dy -= 1
        return gc.ydtogc(y+dy, d2)

    @staticmethod
    def before(year:int, month:int, day:int, period:int) -> GregC:
        return gc.after(year, month, day, -period)

    @staticmethod
    def ud(year:int, month:int, day:int) -> int:
        return gc.leap(year, month, day, *gc.read('19700101'))
    
    @staticmethod
    def md(year:int, month:int, day:int) -> int:
        return gc.leap(year, month, day, *gc.read('20000101'))

    @staticmethod
    def ad(year:int, month:int, day:int) -> int:
        return gc.leap(year, month, day, *gc.read('00010101'))

    @staticmethod
    def mjd(year:int, month:int, day:int) -> int:
        return gc.leap(year, month, day, *gc.read('18581116'))

    @staticmethod
    def arcud(days:int) -> GregC:
        return gc.after(1970, 1, 1, days)

    @staticmethod
    def arcmd(days:int) -> GregC:
        return gc.after(2000, 1, 1, days)

    @staticmethod
    def arcad(days:int) -> GregC:
        return gc.after(1, 1, 1, days)

    @staticmethod
    def arcmjd(days:int) -> GregC:
        return gc.after(1858, 11, 16, days)

class tm:

    @staticmethod
    def read(tm:str) -> TimeHMS:
        return int(tm[:2]), int(tm[2:4]), int(tm[4:])

    @staticmethod
    def secs(h:int,m:int, s:int) -> int:
        return h*3600 + m*60 + s

    @staticmethod
    def tohms(ss:int) -> TimeHMS:
        return ss//3600, ss%3600//60, ss%60

    @staticmethod
    def hours(h:int, m:int, s:int) -> float:
        return h + float(m)/60. + float(s)/3600.

    @staticmethod
    def days(h:int, m:int, s:int) -> float:
        return float(h)/24. + float(m)/1440. + float(s)/86400.

    @staticmethod
    def leap(h1:int, m1:int, s1:int, h0:int, m0:int, s0:int) -> int:
        return tm.secs(h1, m1, s1) - tm.secs(h0, m0, s0)

    @staticmethod
    def after(h:int, m:int, s:int, period:int) -> TimeHMS:
        ss = tm.secs(h, m, s)
        s2 = ss + period
        return tm.tohms(s2)

    @staticmethod
    def before(h:int, m:int, s:int, period:int) -> TimeHMS:
        ss = tm.secs(h, m, s)
        s2 = ss - period
        return tm.tohms(s2)

    @staticmethod
    def afterd(h:int, m:int, s:int, period:int) -> Tuple[int, TimeHMS]:
        ss = tm.secs(h, m, s)
        s2 = ss + period
        hr, mr, sr = tm.tohms(s2)
        d = 0
        if period > 0:
            while hr >= 24:
                hr -= 24
                d += 1
        else:
            while hr < 0:
                hr += 24
                d -= 1
        return d, hr, mr, sr

    @staticmethod
    def befored(h:int, m:int, s:int, period:int) -> Tuple[int, TimeHMS]:
        return tm.afterd(h, m, s, -period)

class dt:

    def __init__(self, dtstr:str, tz:Union[int, float]=0) -> None:
        try:
            if len(dtstr) == 14:
                self.Y = int(dtstr[:4])
                self.M = int(dtstr[4:6])
                self.D = int(dtstr[6:8])
                self.h = int(dtstr[8:10])
                self.m = int(dtstr[10:12])
                self.s = int(dtstr[12:])
                self._date = True
                self._time = True
                self._tz = tz
            elif len(dtstr) == 12:
                self.Y = int(dtstr[:4])
                self.M = int(dtstr[4:6])
                self.D = int(dtstr[6:8])
                self.h = int(dtstr[8:10])
                self.m = int(dtstr[10:12])
                self.s = 0
                self._date = True
                self._time = True
                self._tz = tz
            elif len(dtstr) == 10:
                self.Y = int(dtstr[:4])
                self.M = int(dtstr[4:6])
                self.D = int(dtstr[6:8])
                self.h = int(dtstr[8:10])
                self.m = 0
                self.s = 0
                self._date = True
                self._time = True
                self._tz = tz
            elif len(dtstr) == 8:
                self.Y = int(dtstr[:4])
                self.M = int(dtstr[4:6])
                self.D = int(dtstr[6:8])
                self._date = True
                self._time = False
                self._tz = tz
            elif len(dtstr) == 6:
                self.h = int(dtstr[:2])
                self.m = int(dtstr[2:4])
                self.s = int(dtstr[4:])
                self._date = False
                self._time = True
                self._tz = tz
        except:
            raise RuntimeError('Wrong data format for \'dt\' object')

    def __call__(self, div:str='', utc=False) -> str:
        if utc:
            pass
        else:
            if self._date and self._time:
                return f'{int(self.Y):0>4d}{div}{int(self.M):0>2d}{div}{int(self.D):0>2d}{div}{div}{int(self.h):0>2d}{div}{int(self.m):0>2d}{div}{int(self.s):0>2d}'
            elif self._date:
                return f'{int(self.Y):0>4d}{div}{int(self.M):0>2d}{div}{int(self.D):0>2d}'
            elif self._time:
                return f'{int(self.h):0>2d}{div}{int(self.m):0>2d}{div}{int(self.s):0>2d}'

    def __str__(self) -> str:
        return self.__call__('-')

    @property
    def date(self) -> GregC:
        if not self._date:
            raise RuntimeError('Invalid operation detected')
        else:
            return self.Y, self.M, self.D
            
    @property
    def time(self) -> TimeHMS:
        if not self._time:
            raise RuntimeError('Invalid operation detected')
        else:
            return self.h, self.m, self.s

    @property
    def utc(self) -> TimeHMS:
        if not self._time:
            raise RuntimeError('Invalid operation detected')
        else:
            return self.h-self._tz, self.m, self.s

    @property
    def UTC(self):
        if not self._date or not self._time:
            raise RuntimeError('Invalid operation detected')
        if self.h-self._tz < 0:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D-1):0>2d}{int(self.h-self._tz+24):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')
        elif self.h-self._tz >= 24:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D+1):0>2d}{int(self.h-self._tz-24):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')
        else:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D):0>2d}{int(self.h-self._tz):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')

    @property
    def tz(self) -> str:
        if self._tz > 0:
            return f'UTC +{self._tz}'
        elif self._tz < 0:
            return f'UTC -{-self._tz}'
        else:
            return 'UTC'

    def TZ(self, newtz:Union[int, float]):
        diff = self._tz - newtz
        if self.h-diff < 0:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D-1):0>2d}{int(self.h-diff+24):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')
        elif self.h-diff >= 24:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D+1):0>2d}{int(self.h-diff-24):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')
        else:
            return dt(f'{int(self.Y):0>4d}{int(self.M):0>2d}{int(self.D):0>2d}{int(self.h-diff):0>2d}{int(self.m):0>2d}{int(self.s):0>2d}')

    def __sub__(self, other:Union[int, float, object]) -> Union[int, float, object]:
        if isinstance(other, int) or isinstance(other, float):
            return self.__add__(-other)
        else:
            if self._date and self._time:
                return gc.leap(*self.date, *other.date) + tm.leap(*self.utc, *other.utc)/86400.
            elif self._date:
                return gc.leap(*self.date, *other.date)
            elif self._time:
                return tm.leap(*self.utc, *other.utc)

    def __add__(self, period:float):
        if self._date and self._time:
            p_d = period // 1
            p_s = period % 1 * 86400.
            rY, rM, rD = gc.after(*self.date, p_d)
            rd, rh, rm, rs = tm.afterd(*self.time, p_s)
            return dt(f'{int(rY):0>4d}{int(rM):0>2d}{int(rD+rd):0>2d}{int(rh):0>2d}{int(rm):0>2d}{int(rs):0>2d}', tz=self._tz)
        elif self._date:
            p_d = period // 1
            rY, rM, rD = gc.after(*self.date, p_d)
            return dt(f'{int(rY):0>4d}{int(rM):0>2d}{int(rD):0>2d}', tz=self._tz)
        elif self._time:
            p_s = period % 1 * 86400.
            rh, rm, rs = tm.after(*self.time, p_s)
            return dt(f'{int(rh):0>2d}{int(rm):0>2d}{int(rs):0>2d}', tz=self._tz)

    @property
    def us(self) -> int:
        if self._date and self._time:
            return gc.ud(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.ud(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    @property
    def ud(self) -> float:
        if self._date and self._time:
            return gc.ud(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.ud(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    def usf(self) -> int:
        if self._date and self._time:
            return gc.ud(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.ud(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    def udf(self) -> float:
        if self._date and self._time:
            return gc.ud(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.ud(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    @property
    def ms(self) -> int:
        if self._date and self._time:
            return gc.md(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.md(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    @property
    def md(self) -> float:
        if self._date and self._time:
            return gc.md(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.md(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    def msf(self) -> int:
        if self._date and self._time:
            return gc.md(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.md(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    def mdf(self) -> float:
        if self._date and self._time:
            return gc.md(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.md(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    @property
    def mjs(self) -> int:
        if self._date and self._time:
            return gc.mjd(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.mjd(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    @property
    def mjd(self) -> float:
        if self._date and self._time:
            return gc.mjd(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.mjd(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    def mjsf(self) -> int:
        if self._date and self._time:
            return gc.mjd(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.mjd(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    def mjdf(self) -> float:
        if self._date and self._time:
            return gc.mjd(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.mjd(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    @property
    def ads(self) -> int:
        if self._date and self._time:
            return gc.ad(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.ad(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    @property
    def ad(self) -> float:
        if self._date and self._time:
            return gc.ad(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.ad(*self.date)
        elif self._time:
            return tm.days(*self.utc)

    def adsf(self) -> int:
        if self._date and self._time:
            return gc.ad(*self.date)*86400. + tm.secs(*self.utc)
        elif self._date:
            return gc.ad(*self.date)*86400.
        elif self._time:
            return tm.secs(*self.utc)

    def adf(self) -> float:
        if self._date and self._time:
            return gc.ad(*self.date) + tm.days(*self.utc)
        elif self._date:
            return gc.ad(*self.date)
        elif self._time:
            return tm.days(*self.utc)

class ud(dt):

    def __init__(self, days:Union[int,float], tz:Union[int, float]=0) -> None:
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcud(days)
            self._date = True
            self._time = False
            self._tz = tz
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcud(d_d)
            self.h, self.m, self.s = tm.tohms(d_s)
            self._date = True
            self._time = True
            self._tz = tz

class uds(dt):

    def __init__(self, ss:float, tz:Union[int, float]=0) -> None:
        obj = dt('19700101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True
        self._tz = tz

class md(dt):

    def __init__(self, days:Union[int,float], tz:Union[int, float]=0) -> None:
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcmd(days)
            self._date = True
            self._time = False
            self._tz = tz
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcmd(d_d)
            self.h, self.m, self.s = tm.tohms(d_s)
            self._date = True
            self._time = True
            self._tz = tz

class mds(dt):

    def __init__(self, ss:float, tz:Union[int, float]=0) -> None:
        obj = dt('20000101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True
        self._tz = tz

class mjd(dt):

    def __init__(self, days:Union[int,float], tz:Union[int, float]=0) -> None:
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcmjd(days)
            self._date = True
            self._time = False
            self._tz = tz
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcmjd(d_d)
            self.h, self.m, self.s = tm.tohms(d_s)
            self._date = True
            self._time = True
            self._tz = tz

class mjds(dt):

    def __init__(self, ss:float, tz:Union[int, float]=0) -> None:
        obj = dt('18581116000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True
        self._tz = tz

class ad(dt):

    def __init__(self, days:Union[int,float], tz:Union[int, float]=0) -> None:
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcad(days)
            self._date = True
            self._time = False
            self._tz = tz
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcad(d_d)
            self.h, self.m, self.s = tm.tohms(d_s)
            self._date = True
            self._time = True
            self._tz = tz

class ads(dt):

    def __init__(self, ss:float, tz:Union[int, float]=0) -> None:
        obj = dt('00010101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True
        self._tz = tz

class dts(dt):

    def __init__(self, **kwargs:dict) -> None:
        self._tz = 0
        self._date = False
        self._time = False
        self.h = 0
        self.m = 0
        self.s = 0
        for kw in kwargs.keys():
            if kw == 'Y':
                self.Y = kwargs[kw]
                self._date = True
            elif kw == 'M':
                self.M = kwargs[kw]
                self._date = True
            elif kw == 'D':
                self.D = kwargs[kw]
                self._date = True
            elif kw == 'h':
                self.h = kwargs[kw]
                self._time = True
            elif kw == 'm':
                self.m = kwargs[kw]
                self._time = True
            elif kw == 's':
                self.s = kwargs[kw]
                self._time = True
            elif kw.lower() == 'tz':
                self._tz = kwargs[kw]

class now(dt):

    def __init__(self, tz:Union[int, float]=0) -> None:
        obj = dt(system_time.strftime('%Y%m%d%H%M%S', system_time.localtime(system_time.time())))
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True
        self._tz = tz