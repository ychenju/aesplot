# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from .main import *
from .ascl import *
from .atm import *
from .basemap import *
from .figure import *
from .filter import *
from .prep import *
from .stat import *
from .tc import *
from .toolkit import *
from .templates import *
from .wrfp import *

# 用法：import aesplot.all as ap
#   
#   allabbrs    0.3.0   
#   ascl        0.4.0   astronomy and calendars
#   atm         0.3.0   atmospheric science function module
#   auxf        0.2.0   auxiliary functions (FOR INTERNAL USAGE)
#   basemap     0.1.0   Basemap supports
#   figure      0.1.0   figure objects
#   filter      0.3.0   filter objects
#   gc          0.4.7   GeosChem functions
#   main        0.1.0   main part (imported with the package)
#   prep        0.2.1   data preprocessing
#   settings    0.1.0   internal setting functions
#   stat        0.3.0   statistics function module
#   tc          0.2.0   tropical cyclone track processing module
#   templates           templates
#   toolkit     0.2.0   useful tool functions for programming (FOR EXTERNAL USAGE)
#   ts          0.4.5   time series module
#   wrfp        0.3.0   WRFout processing module