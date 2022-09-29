# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from . import main as ap
from . import ascl as apac
from . import atm as apa
from . import basemap as apb
from . import figure as apf
from . import filter as apfilter
from . import prep as app
from . import stat as aps
from . import tc as aptc
from . import templates as aptps
from . import toolkit as aptk
from . import wrfp as wp


# 用法：from aesplot.allabbrs import *
#
#   atm         atmospheric science function module
#   auxf        auxiliary functions (FOR INTERNAL USAGE)
#   basemap     Basemap supports
#   figure      figure objects
#   main        main part (imported with the package)
#   prep        data preprocessing
#   settings    internal setting functions
#   stat        statistics function module
#   tc          tropical cyclone track processing module
#   templates   templates
#   toolkit     useful tool functions for programming (FOR EXTERNAL USAGE)
#   wrfp        WRFout processing module