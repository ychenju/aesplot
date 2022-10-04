# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr
from . import figure as apf
from . import stat as aps

def linreg_show(reg: aps.linreg):
    return (apf.scatter(x=reg.x, y=reg.y).format(c='k'), apf.func(xrange=[np.min(reg.x), np.max(reg.x)], f=reg.f).format(c='r'))