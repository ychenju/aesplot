# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def longfix(lon: float):
    if lon < 0:
        return 360.+lon
    else:
        return lon

def samesign(x, y):
    return (np.sign(x)*np.sign(y)+1)/2.