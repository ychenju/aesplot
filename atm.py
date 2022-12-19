# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import ascl
from . import trigo as tr
from typing import Union

MONTH_NAMES = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

BEAUFORT_SCALE = (  0.2,    1.5,    3.3,    4.5,    7.9,    10.7,   13.8,   17.1,   20.7,   24.4,
                    28.4,   32.6,   36.9,   41.4,   46.1,   50.9,   56.,    61.2)

def mps_to_beaufort(windspeed:float) -> int:
    '''
    Convert windspeed in m/s to Beaufort wind scale (extended)
    '''
    if np.isnan(windspeed):
        return np.nan
    for i, x in enumerate(BEAUFORT_SCALE):
        if windspeed <= x:
            return i
    return 18

def sea(lat:float, long:float, date:Union[str, ascl.dt]) -> float:
    '''
    Calculate the solar elevation angle (in degree)
    '''
    return tr.arcsind(tr.sind(lat)*tr.sind(declination(date)) + tr.cosd(lat)*tr.cosd(declination(date))*tr.cosd(timeangle(date, long)))

def declination(date:Union[str, ascl.dt]) -> float:
    '''
    Calculate the solar declination (in degree)
    '''
    if isinstance(date, str):
        return tr.arcsind(tr.sind(23.45)*np.sin(2*np.pi/365.24*(284+ascl.gc.toyd(*ascl.dt(date).date)[1])))
    else:
        return tr.arcsind(tr.sind(23.45)*np.sin(2*np.pi/365.24*(284+ascl.gc.toyd(*date.date)[1])))

def timeangle(date:Union[str, ascl.dt], long:float) -> float:
    '''
    Calculate the time angle
    '''
    if isinstance(date, str):
        st = ascl.tm.hours(*ascl.dt(date).utc) + long/15.
    else:
        st = ascl.tm.hours(*date.utc) + long/15.
    return 15*(st-12)

def tdt(lat:float, date:Union[str, ascl.dt]) -> float:
    '''
    Calculate the total daytime (in seconds)
    '''
    if tr.tand(-lat)*tr.tand(declination(date)) > 1:
        return 0
    elif tr.tand(-lat)*tr.tand(declination(date)) < -1:
        return 86400
    else:
        return np.arccos(tr.tand(-lat)*tr.tand(declination(date)))*86400./np.pi

def ssrd_to_tsolar(lat:float, long:float, date:Union[str, ascl.dt], ssrd:float) -> float:
    '''
    Convert SSRD data (of a day) to tsolar value (of a moment)
    '''
    if not np.isnan(_r := np.pi*ssrd*tr.sind(max(sea(lat, long, date),0))/\
        (np.pi*tdt(lat,date)*tr.sind(lat)*tr.sind(declination(date))+86400*tr.cosd(lat)*tr.cosd(declination(date))*np.sin(np.pi/86400.*tdt(lat,date)))):
        return _r
    else:
        return 0