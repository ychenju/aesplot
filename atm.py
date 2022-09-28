# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

BEAUFORT_SCALE = (  0.2,    1.5,    3.3,    4.5,    7.9,    10.7,   13.8,   17.1,   20.7,   24.4,
                    28.4,   32.6,   36.9,   41.4,   46.1,   50.9,   56.,    61.2)

def mps_to_beaufort(windspeed):
    if np.isnan(windspeed):
        return np.nan
    for i, x in enumerate(BEAUFORT_SCALE):
        if windspeed <= x:
            return i
    return 18