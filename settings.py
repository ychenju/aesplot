# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from .img import *
import matplotlib as mpl

def sans_serif(font:str) -> None:
    '''
    '''
    mpl.rcParams['font.sans-serif']=[font]