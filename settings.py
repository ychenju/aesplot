# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from .main import *
import matplotlib as mpl

def sans_serif(font : str):
    mpl.rcParams['font.sans-serif']=[font]