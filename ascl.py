# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class gc:

    NORMAL_MONTHS_DAYS = np.array([
        0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ])

    @staticmethod
    def read(date: str):
        return int(date[:4]), int(date[4:6]), int(date[6:])

    @staticmethod
    def ytype(year: int):
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
    def ydays(year: int):
        if gc.ytype(year) == -1:
            return 355
        else:
            return 365 + gc.ytype(year)

    @staticmethod
    def mdays(year: int, month: int):
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
    def zerostart(year: int, month: int, day: int):
        return year, month-1, day-1

    @staticmethod
    def onestart(year: int, month: int, day: int):
        return year, month+1, day+1

    @staticmethod
    def toyd_normal(year: int, month: int, day: int):
        return year, gc.NORMAL_MONTHS_DAYS[:month].sum() + day

    @staticmethod
    def dfix(year: int, month: int, day: int):
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
    def toyd(year: int, month: int, day: int):
        return gc.toyd_normal(year, month, day)[0], gc.toyd_normal(year, month, day)[1] + gc.dfix(year, month, day)

    @staticmethod
    def ydtogc(year: int, day: int):
        month = 0
        daysub = day
        while daysub > 0:
            month += 1
            daysub -= gc.mdays(year, month)
        return year, month, gc.mdays(year, month) + daysub

    @staticmethod
    def leap(year1: int, month1: int, day1: int, year0: int, month0: int, day0: int):
        y1, d1 = gc.toyd(year1, month1, day1)
        y0, d0 = gc.toyd(year0, month0, day0)
        if y1 > y0:
            return d1 + gc.ydays(y0) - d0 + np.array([gc.ydays(y) for y in range(y0+1,y1)] if y0+1 < y1 else [0]).sum()
        elif y1 < y0:
            return d1 - gc.ydays(y1) - d0  - np.array([gc.ydays(y) for y in range(y1+1,y0)] if y1+1 < y0 else [0]).sum()
        else:
            return d1 - d0

    @staticmethod
    def after(year: int, month: int, day: int, period: int):
        y, d = gc.toyd(year, month, day)
        dy = 0
        d2 = d + period
        if period > 0:
            while d2 > gc.ydays(y):
                d2 -= gc.ydays(y)
                dy += 1
        else:
            while d2 <= 0:
                d2 += gc.ydays(y-1)
                dy -= 1
        return gc.ydtogc(y+dy, d2)

    @staticmethod
    def before(year: int, month: int, day: int, period: int):
        return gc.after(year, month, day, -period)

    @staticmethod
    def ud(year: int, month: int, day: int):
        return gc.leap(year, month, day, *gc.read('19700101'))
    
    @staticmethod
    def md(year: int, month: int, day: int):
        return gc.leap(year, month, day, *gc.read('20000101'))

    @staticmethod
    def ad(year: int, month: int, day: int):
        return gc.leap(year, month, day, *gc.read('00010101'))

    @staticmethod
    def mjd(year: int, month: int, day: int):
        return gc.leap(year, month, day, *gc.read('18581116'))

    @staticmethod
    def arcud(days: int):
        return gc.after(1970, 1, 1, days)

    @staticmethod
    def arcmd(days: int):
        return gc.after(2000, 1, 1, days)

    @staticmethod
    def arcad(days: int):
        return gc.after(1, 1, 1, days)

    @staticmethod
    def arcmjd(days: int):
        return gc.after(1858, 11, 16, days)

class time:

    @staticmethod
    def read(time: str):
        return int(time[:2]), int(time[2:4]), int(time[4:])

    @staticmethod
    def secs(h: int, m: int, s: int):
        return h*3600 + m*60 + s

    @staticmethod
    def tohms(ss):
        return ss//3600, ss%3600//60, ss%60

    @staticmethod
    def hours(h: int, m: int, s: int):
        return h + float(m)/60. + float(s)/3600.

    @staticmethod
    def days(h: int, m: int, s: int):
        return float(h)/24. + float(m)/1440. + float(s)/86400.

    @staticmethod
    def leap(h1: int, m1: int, s1: int, h0: int, m0: int, s0: int):
        return time.secs(h1, m1, s1) - time.secs(h0, m0, s0)

    @staticmethod
    def after(h: int, m: int, s: int, period: int):
        ss = time.secs(h, m, s)
        s2 = ss + period
        return time.tohms(s2)

    @staticmethod
    def before(h: int, m: int, s: int, period: int):
        ss = time.secs(h, m, s)
        s2 = ss - period
        return time.tohms(s2)

    @staticmethod
    def afterd(h: int, m: int, s: int, period: int):
        ss = time.secs(h, m, s)
        s2 = ss + period
        hr, mr, sr = time.tohms(s2)
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
    def befored(h: int, m: int, s: int, period: int):
        return time.afterd(h, m, s, -period)

class dt:

    def __init__(self, dtstr: str):
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
            elif len(dtstr) == 8:
                self.Y = int(dtstr[:4])
                self.M = int(dtstr[4:6])
                self.D = int(dtstr[6:8])
                self._date = True
                self._time = False
            elif len(dtstr) == 6:
                self.h = int(dtstr[:2])
                self.m = int(dtstr[2:4])
                self.s = int(dtstr[4:])
                self._date = False
                self._time = True
        except:
            raise RuntimeError('Wrong data format for \'dt\' object')

    def __call__(self, div=''):
        if self._date and self._time:
            return f'{int(self.Y):0>4d}{div}{int(self.M):0>2d}{div}{int(self.D):0>2d}{div}{div}{int(self.h):0>2d}{div}{int(self.m):0>2d}{div}{int(self.s):0>2d}'
        elif self._date:
            return f'{int(self.Y):0>4d}{div}{int(self.M):0>2d}{div}{int(self.D):0>2d}'
        elif self._time:
            return f'{int(self.h):0>2d}{div}{int(self.m):0>2d}{div}{int(self.s):0>2d}'

    @property
    def date(self):
        if not self._date:
            raise RuntimeError('Invalid operation detected')
        else:
            return self.Y, self.M, self.D
            
    @property
    def time(self):
        if not self._time:
            raise RuntimeError('Invalid operation detected')
        else:
            return self.h, self.m, self.s

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__add__(-other)
        if self._date and self._time:
            return gc.leap(self.Y, self.M, self.D, other.Y, other.M, other.D) + time.leap(self.h, self.m, self.s, other.h, other.m, other.s)/86400.
        elif self._date:
            return gc.leap(self.Y, self.M, self.D, other.Y, other.M, other.D)
        elif self._time:
            return time.leap(self.h, self.m, self.s, other.h, other.m, other.s)

    def __add__(self, period):
        if self._date and self._time:
            p_d = period // 1
            p_s = period % 1 * 86400.
            rY, rM, rD = gc.after(self.Y, self.M, self.D, p_d)
            rd, rh, rm, rs = time.afterd(self.h, self.m, self.s, p_s)
            return dt(f'{int(rY):0>4d}{int(rM):0>2d}{int(rD+rd):0>2d}{int(rh):0>2d}{int(rm):0>2d}{int(rs):0>2d}')
        elif self._date:
            p_d = period // 1
            rY, rM, rD = gc.after(self.Y, self.M, self.D, p_d)
            return dt(f'{int(rY):0>4d}{int(rM):0>2d}{int(rD):0>2d}')
        elif self._time:
            p_s = period % 1 * 86400.
            rh, rm, rs = time.after(self.h, self.m, self.s, p_s)
            return dt(f'{int(rh):0>2d}{int(rm):0>2d}{int(rs):0>2d}')

    @property
    def us(self):
        if self._date and self._time:
            return gc.ud(self.Y, self.M, self.D)*86400 + time.secs(self.h, self.m, self.s)
        elif self._date:
            return gc.ud(self.Y, self.M, self.D)*86400.
        elif self._time:
            return time.secs(self.h, self.m, self.s)

    @property
    def ud(self):
        if self._date and self._time:
            return gc.ud(self.Y, self.M, self.D) + time.days(self.h, self.m, self.s)
        elif self._date:
            return gc.ud(self.Y, self.M, self.D)
        elif self._time:
            return time.days(self.h, self.m, self.s)

    @property
    def ms(self):
        if self._date and self._time:
            return gc.md(self.Y, self.M, self.D)*86400. + time.secs(self.h, self.m, self.s)
        elif self._date:
            return gc.md(self.Y, self.M, self.D)*86400.
        elif self._time:
            return time.secs(self.h, self.m, self.s)

    @property
    def md(self):
        if self._date and self._time:
            return gc.md(self.Y, self.M, self.D) + time.days(self.h, self.m, self.s)
        elif self._date:
            return gc.md(self.Y, self.M, self.D)
        elif self._time:
            return time.days(self.h, self.m, self.s)

    @property
    def ms(self):
        if self._date and self._time:
            return gc.mjd(self.Y, self.M, self.D)*86400. + time.secs(self.h, self.m, self.s)
        elif self._date:
            return gc.mjd(self.Y, self.M, self.D)*86400.
        elif self._time:
            return time.secs(self.h, self.m, self.s)

    @property
    def md(self):
        if self._date and self._time:
            return gc.mjd(self.Y, self.M, self.D) + time.days(self.h, self.m, self.s)
        elif self._date:
            return gc.mjd(self.Y, self.M, self.D)
        elif self._time:
            return time.days(self.h, self.m, self.s)

    @property
    def ads(self):
        if self._date and self._time:
            return gc.ad(self.Y, self.M, self.D)*86400. + time.secs(self.h, self.m, self.s)
        elif self._date:
            return gc.ad(self.Y, self.M, self.D)*86400.
        elif self._time:
            return time.secs(self.h, self.m, self.s)

    @property
    def ad(self):
        if self._date and self._time:
            return gc.ad(self.Y, self.M, self.D) + time.days(self.h, self.m, self.s)
        elif self._date:
            return gc.ad(self.Y, self.M, self.D)
        elif self._time:
            return time.days(self.h, self.m, self.s)

class ud(dt):

    def __init__(self, days):
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcud(days)
            self._date = True
            self._time = False
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcud(d_d)
            self.h, self.m, self.s = time.tohms(d_s)
            self._date = True
            self._time = True

class uds(dt):

    def __init__(self, ss: float):
        obj = dt('19700101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True

class md(dt):

    def __init__(self, days):
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcmd(days)
            self._date = True
            self._time = False
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcmd(d_d)
            self.h, self.m, self.s = time.tohms(d_s)
            self._date = True
            self._time = True

class mds(dt):

    def __init__(self, ss: float):
        obj = dt('20000101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True

class mjd(dt):

    def __init__(self, days):
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcmjd(days)
            self._date = True
            self._time = False
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcmjd(d_d)
            self.h, self.m, self.s = time.tohms(d_s)
            self._date = True
            self._time = True

class mjds(dt):

    def __init__(self, ss: float):
        obj = dt('18581116000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True

class ad(dt):

    def __init__(self, days):
        if isinstance(days, int):
            self.Y, self.M, self.D = gc.arcad(days)
            self._date = True
            self._time = False
        else:
            d_d = days // 1
            d_s = days % 1 * 86400
            self.Y, self.M, self.D = gc.arcad(d_d)
            self.h, self.m, self.s = time.tohms(d_s)
            self._date = True
            self._time = True

class ads(dt):

    def __init__(self, ss: float):
        obj = dt('00010101000000') + ss/86400.
        self.Y = obj.Y
        self.M = obj.M
        self.D = obj.D
        self.h = obj.h
        self.m = obj.m
        self.s = obj.s
        self._date = True
        self._time = True

class dts(dt):

    def __init__(self, **kwargs):
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
