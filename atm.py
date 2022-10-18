# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import ascl
from . import trigo as tr
from typing import Union

BEAUFORT_SCALE = (  0.2,    1.5,    3.3,    4.5,    7.9,    10.7,   13.8,   17.1,   20.7,   24.4,
                    28.4,   32.6,   36.9,   41.4,   46.1,   50.9,   56.,    61.2)

def mps_to_beaufort(windspeed:float) -> int:
    if np.isnan(windspeed):
        return np.nan
    for i, x in enumerate(BEAUFORT_SCALE):
        if windspeed <= x:
            return i
    return 18

# solar elevation angle
# sin h = sin φ sin δ + cos φ cos δ cos t
# h: SEA
# φ: latitude
# δ: declination
# t: time angle
def sea(lat:float, long:float, date:Union[str, ascl.dt]) -> float:
    return tr.arcsind(tr.sind(lat)*tr.sind(declination(date)) + tr.cosd(lat)*tr.cosd(declination(date))*tr.cosd(timeangle(date, long)))

def declination(date:Union[str, ascl.dt]) -> float:
    if isinstance(date, str):
        return tr.arcsind(tr.sind(23.45)*np.sin(2*np.pi/365.24*(284+ascl.gc.toyd(*ascl.dt(date).date)[1])))
    else:
        return tr.arcsind(tr.sind(23.45)*np.sin(2*np.pi/365.24*(284+ascl.gc.toyd(*date.date)[1])))

def timeangle(date:Union[str, ascl.dt], long:float) -> float:
    if isinstance(date, str):
        st = ascl.tm.hours(*ascl.dt(date).utc) + long/15.
    else:
        st = ascl.tm.hours(*date.utc) + long/15.
    return 15*(st-12)