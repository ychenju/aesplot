# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def d2r(deg:float) -> float:
    '''
    Degree to radian
    '''
    return deg/180.*np.pi

def r2d(rad:float) -> float:
    '''
    Radian to degree
    '''
    return rad/np.pi*180.

def sind(deg:float) -> float:
    '''
    sin for value in degree
    '''
    return np.sin(d2r(deg))

def cosd(deg:float) -> float:
    '''
    cos for value in degree
    '''
    return np.cos(d2r(deg))

def tand(deg:float) -> float:
    '''
    tan for value in degree
    '''
    return np.tan(d2r(deg))

def arcsind(val:float) -> float:
    '''
    arcsin returning value in degree
    '''
    return r2d(np.arcsin(val))

def arccosd(val:float) -> float:
    '''
    arccos returning value in degree
    '''
    return r2d(np.arccos(val))

def arctand(val:float) -> float:
    '''
    arctan returning value in degree
    '''
    return r2d(np.arctan(val))

class tri:
    
    def __init__(self, **kwargs) -> None:
        '''
        '''
        if len(kwargs.keys()) != 3:
            raise RuntimeError('Invalid Triangle!')
        self.counta = 0
        for kw in kwargs.keys():
            if kw[0] == 'a':
                self.counta += 1
        if self.counta == 3:
            raise RuntimeError('Invalid Triangle!')
        self._bool = {
            's1': False, 's2': False, 's3': False,
            'a12': False, 'a23': False, 'a13': False,
        }
        self._data = {
            's1': 0, 's2': 0, 's3': 0,
            'a12': 0, 'a23': 0, 'a13': 0,
        }
        for kw in kwargs.keys():
            self._bool[kw] = True
            self._data[kw] = kwargs[kw]
    
    @property
    def s1(self) -> float:
        return self._data['s1'] if self._bool['s1'] else self.gets1()

    @property
    def s2(self) -> float:
        return self._data['s2'] if self._bool['s2'] else self.gets2()

    @property
    def s3(self) -> float:
        return self._data['s3'] if self._bool['s3'] else self.gets3()

    @property
    def a12(self) -> float:
        a = self._data['a12'] if self._bool['a12'] else self.geta12()
        return 90 if np.isnan(a) else a

    @property
    def a23(self) -> float:
        a = self._data['a23'] if self._bool['a23'] else self.geta23()
        return 90 if np.isnan(a) else a

    @property
    def a13(self) -> float:
        a = self._data['a13'] if self._bool['a13'] else self.geta13()
        return 90 if np.isnan(a) else a

    def gets1(self) -> float:
        if self._bool['s1']:
            return self._data['s1']
        elif self.counta == 1:
            return np.sqrt(self.s2**2 + self.s3**2 - 2*self.s2*self.s3*cosd(self.a23))
        elif self.counta == 2:
            return self.s2 * sind(self.a23) / sind(self.a13)

    def gets2(self) -> float:
        if self._bool['s2']:
            return self._data['s2']
        elif self.counta == 1:
            return np.sqrt(self.s1**2 + self.s3**2 - 2*self.s1*self.s3*cosd(self.a13))
        elif self.counta == 2:
            return self.s3 * sind(self.a13) / sind(self.a12)

    def gets3(self) -> float:
        if self._bool['s3']:
            return self._data['s3']
        elif self.counta == 1:
            return np.sqrt(self.s1**2 + self.s2**2 - 2*self.s1*self.s2*cosd(self.a12))
        elif self.counta == 2:
            return self.s1 * sind(self.a12) / sind(self.a23)

    def geta12(self) -> float:
        if self._bool['a12']:
            return self._data['a12']
        elif self.counta == 0:
            return arccosd((self.s1**2 + self.s2**2 - self.s3**2)/(2*self.s1*self.s2))
        elif self.counta == 1:
            try:
                return arcsind(sind(self.a23)*self.s3/self.s1)
            except:
                return arcsind(sind(self.a13)*self.s3/self.s2)
        elif self.counta == 2:
            return 180 - self.a23 - self.a13

    def geta23(self) -> float:
        if self._bool['a23']:
            return self._data['a23']
        elif self.counta == 0:
            return arccosd((self.s2**2 + self.s3**2 - self.s1**2)/(2*self.s2*self.s3))
        elif self.counta == 1:
            try:
                return arcsind(sind(self.a13)*self.s1/self.s2)
            except:
                return arcsind(sind(self.a12)*self.s1/self.s3)
        elif self.counta == 2:
            return 180 - self.a13 - self.a12

    def geta13(self) -> float:
        if self._bool['a13']:
            return self._data['a13']
        elif self.counta == 0:
            return arccosd((self.s3**2 + self.s1**2 - self.s2**2)/(2*self.s3*self.s1))
        elif self.counta == 1:
            try: 
                return arcsind(sind(self.a12)*self.s2/self.s3)
            except:
                return arcsind(sind(self.a23)*self.s2/self.s1)
        elif self.counta == 2:
            return 180 - self.a12 - self.a23

    @property
    def area(self) -> float:
        '''
        Area of the triangle
        '''
        return np.sqrt(self.circ/2*(self.circ/2-self.s1)*(self.circ/2-self.s2)*(self.circ/2-self.s3))

    @property
    def circ(self) -> float:
        '''
        Circumference of the triangle
        '''
        return self.s1 + self.s2 + self.s3

    def __str__(self) -> str:
        return f's1:\t{self.s1}\n' + f's2:\t{self.s2}\n' + f's3:\t{self.s3}\n' + f'a12:\t{self.a12}\n' + f'a23:\t{self.a23}\n' + f'a13:\t{self.a13}\n'

def nmtokm(value:float) -> float:
    '''
    Convert n mile to kilometer
    '''
    return 10000./5400.*value

def kmtonm(value:float) -> float:
    '''
    Convert kilometer to n mile
    '''
    return 5400./10000.*value

def lattokm(value:float) -> float:
    '''
    Convert degree latitute to kilometer
    '''
    return 60.*nmtokm(value)

def kmtolat(value:float) -> float:
    '''
    Convert kilometer to degree latitute
    '''
    return kmtonm(value)/60.

def longtokm(long:float, lat:float) -> float:
    '''
    Convert degree longitute on certain latitute to kilometer
    '''
    return lattokm(long)*cosd(lat)

def kmtolong(km:float, lat:float) -> float:
    '''
    Convert kilometer to degree longitute on certain latitute
    '''
    return kmtolat(km)/cosd(lat)