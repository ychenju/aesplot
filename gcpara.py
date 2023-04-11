# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from . import ascl
from typing import Union
from . import gcparadata as pdata
from . import gc

R = 8.3144598e-3

MEGAN_T_STANDARD = 303.
WM2_TO_UMOLM2S = 4.766

def get_glai_params(time:ascl.dt, lat:float, long:float, bi:bool):
    m = time()[4:6]
    v = f'V{int((lat+60)//15):1d}'
    h = f'H{int((long+180)//15):0>2d}'
    try:
        if bi:
            return pdata.GLAI_EOH_SELECTED_PARAMS1[h][v][m]
        else:
            return pdata.GLAI_ISOP_SELECTED_PARAMS1[h][v][m]
    except:
        return 0

def get_glai_fix(area:float, time:ascl.dt, lat:float, long:float, bi:bool):
    return 1 + get_glai_params(time, lat, long, bi) * np.log(area)**2

def glai_fix(glai:Union[float, np.ndarray], area:Union[float, np.ndarray], time:ascl.dt,\
              lat:Union[float, np.ndarray], long:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        '''
        if not isinstance(glai, np.ndarray):
            return get_glai_fix(area, time, lat, long, gc.megan.get_const(species, 'BI')) * glai
        elif isinstance(glai, np.ndarray):
            _gt = np.zeros(glai.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = get_glai_fix(area, time, lat[i,j], long[i,j], gc.megan.get_const(species, 'BI')) * glai[i,j]
            return np.array(_gt)
        
def glai_fix_to_ref(glai:Union[float, np.ndarray], area:Union[float, np.ndarray], time:ascl.dt,\
              lat:Union[float, np.ndarray], long:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        = glai_fix(area^-1), the area here is the current grid area, not the target area
        '''
        return glai_fix(glai=glai, area=1./area, time=time, lat=lat, long=long, species=species)