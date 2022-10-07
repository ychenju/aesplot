# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import fig as apf
from . import stat as aps
from typing import Tuple

def linreg_show(reg:aps.linreg) -> Tuple[apf.scatter, apf.func]:
    return (apf.scatter(x=reg.x, y=reg.y).format(c='k'), apf.func(xrange=[np.min(reg.x), np.max(reg.x)], f=reg.f).format(c='r'))