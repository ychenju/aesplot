# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from .data import GC_MEGAN_SPECIES_CONST
from typing import Tuple, Union

R = 8.3144598e-3

MEGAN_T_STANDARD = 303.

class megan:

    @staticmethod
    def gamma_t(t:Union[float, np.ndarray], pt_15:Union[float, np.ndarray], pt_1:Union[float, np.ndarray], species:str=0,
                ldf:float=GC_MEGAN_SPECIES_CONST['ISOP']['ldf'], 
                beta:float=GC_MEGAN_SPECIES_CONST['ISOP']['beta'], 
                ct1:float=GC_MEGAN_SPECIES_CONST['ISOP']['ct1'], 
                ceo:float=GC_MEGAN_SPECIES_CONST['ISOP']['ceo'], 
                ) -> Union[float, np.ndarray]:
        if isinstance(species, str):
            _r = megan.get_const(species, 'beta', 'ldf', 'ct1', 'ceo')
        else:
            _r = [beta, ldf, ct1, ceo]
        if not isinstance(t, np.ndarray) and not isinstance(pt_15, np.ndarray):
            return (1.-_r[1])*megan.get_gamma_t_li(t, _r[0]) + _r[1]*megan.get_gamma_t_ld(t, pt_15, pt_1, _r[2], _r[3])
        elif isinstance(t, np.ndarray) and isinstance(pt_15, np.ndarray):
            _gt = []
            for i in range(t.shape[0]):
                _gt.append([])
                for j in range(t.shape[1]):
                    _gt[-1].append((1.-_r[1])*megan.get_gamma_t_li(t[i][j], _r[0]) + _r[1]*megan.get_gamma_t_ld(t[i][j], pt_15[i][j], pt_1[i][j], _r[2], _r[3]))
            return np.array(_gt)

    @staticmethod
    def get_gamma_t_li(t:float, beta:float) -> float:
        gamma_t_li = np.exp(beta*(t - MEGAN_T_STANDARD))
        return gamma_t_li

    @staticmethod
    def get_gamma_t_ld(t:float, pt_15:float, pt_1:float, ct1:float, ceo:float) -> float:
        e_opt = ceo * np.exp(0.08*(pt_15 - 2.97e2))
        t_opt = 3.13e2 + (6.0e-1 * (pt_15 - 2.97e2))
        CT2 = 200.0
        x = (1./t_opt - 1./t) / R
        c_t = e_opt * CT2 * np.exp(ct1 * x) / (CT2 - ct1 * (1.-np.exp(CT2 * x)))
        gamma_t_ld = max(c_t, 0.)
        return gamma_t_ld

    @staticmethod
    def get_const(species:str, *const:Tuple[str]):
        if len(const) == 1:
            return GC_MEGAN_SPECIES_CONST[species][const[0]]
        else:
            return [GC_MEGAN_SPECIES_CONST[species][c] for c in const]