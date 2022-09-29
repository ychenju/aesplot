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