# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt

from .rst import *  # gdal必须在Basemap之前导入，否则报错

from .ascl import *
from .atm import *
from .basemap import *
from .cnnc import *
from .gc import *
from .grib import *
from .grid import *
from .fig import *
from .filter import *
from .img import *
from .nc import *
from .prep import *
from .stat import *
from .tc import *
from .toolkit import *
from .templates import *
from .trigo import *
from .ts import *
from .wrfp import *

# Use：import aesplot.all as ap
#   
#   allabbrs    0.3.0   
#   ascl        0.4.0   astronomy and calendars
#   atm         0.3.0   atmospheric science function module
#   auxf        0.2.0   auxiliary functions (FOR INTERNAL USAGE)
#   basemap     0.1.0   Basemap supports
#   cnnc        0.5.20  CN netCDF file climate data processing module
#   data        0.4.9   large data charts
#   fig         0.1.0   figure objects
#   filter      0.3.0   filter objects
#   gc          0.4.7   GeosChem functions
#   grib        0.5.46  GRIB file processing
#   grid        0.5.26  grid-like data processing
#   img         0.1.0   main part (imported with the package)
#   nc          0.6.3   netCDF4 file processing
#   prep        0.2.1   data preprocessing
#   rst         0.5.21  raster processing
#   settings    0.1.0   internal setting functions
#   stat        0.3.0   statistics function module
#   tc          0.2.0   tropical cyclone track processing module
#   templates   0.4.12  templates
#   toolkit     0.2.0   useful tool functions for programming (FOR EXTERNAL USAGE)
#   trigo       0.5.6   trigometry and geometrics module
#   ts          0.4.5   time series module
#   wrfp        0.3.0   WRFout processing module