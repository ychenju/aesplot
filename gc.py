# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from .data import GC_MEGAN_SPECIES_CONST
from typing import Tuple, Union

R = 8.3144598e-3

MEGAN_T_STANDARD = 303.

class megan:
    ENABLE = {
        'norm_fac'  : False,
        'aef'       : False,
        'gamma_a'   : False,
        'gamma_sm'  : False,
        'gamma_lai' : False,
        'gamma_t_li': True,
        'gamma_t_ld': True,
        'gamma_p'   : False,
        'gamma_CO2' : False,
    }

    @staticmethod
    def emis(**kwargs):
        _r = 1.
        _sub = 1.
        _r *= megan.norm_fac() if megan.ENABLE['norm_fac'] else 1.
        _r *= megan.aef() if megan.ENABLE['aef'] else 1.
        _r *= megan.gamma_a() if megan.ENABLE['gamma_a'] else 1.
        _r *= megan.gamma_sm() if megan.ENABLE['gamma_sm'] else 1.
        _r *= megan.gamma_lai(*megan.gamma_lai_args(**kwargs)) if megan.ENABLE['gamma_lai'] else 1.
        _r *= megan.gamma_CO2() if megan.ENABLE['gamma_CO2'] else 1.
        _sub *= megan.gamma_t_ld(*megan.gamma_t_ld_args(**kwargs)) if megan.ENABLE['gamma_t_ld'] else 1.
        _sub *= megan.gamma_p() if megan.ENABLE['gamma_p'] else 1.
        _sub += megan.gamma_t_li(*megan.gamma_t_li_args(**kwargs)) if megan.ENABLE['gamma_t_li'] else 0.
        _r *= _sub
        return _r

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def norm_fac_args(**kwargs):
        pass

    @staticmethod
    def norm_fac():
        pass

    @staticmethod
    def get_norm_fac():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def aef_args(**kwargs):
        pass

    @staticmethod
    def aef():
        pass

    @staticmethod
    def get_aef():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_a_args(**kwargs):
        pass

    @staticmethod
    def gamma_a():
        pass

    @staticmethod
    def get_gamma_a():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_sm_args(**kwargs):
        _r = {}
        for kw in kwargs.keys():
            if kw == 'gwetroot':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_sm():
        pass

    @staticmethod
    def get_gamma_sm(gwetroot, species):
        _gamma_sm = 1.
        gwetroot = min(max(gwetroot,0.),1.)
        if species == 'ALD2' or species == 'EOH':
            _gamma_sm = max(20.*gwetroot-17., 1.)
        return _gamma_sm

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_lai_args(**kwargs):
        _r = {}
        for kw in kwargs.keys():
            if kw == 'cmlai':
                _r[kw] == kwargs[kw]
            elif kw == 'bidirexch':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_lai():
        pass

    @staticmethod
    def get_gamma_lai(cmlai:float, bidirexch:bool):
        if  bidirexch:
            if  cmlai <= 6.:
                if  cmlai <= 2.:
                    _gamma_lai = 0.5 * cmlai
                else:
                    _gamma_lai = 1. - 0.0625 * ( cmlai - 2. )
            else:
                _gamma_lai = 0.75
        else:
            _gamma_lai = 0.49 * cmlai / np.sqrt(1. + 0.2*cmlai**2)
        return _gamma_lai

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_t_li_args(**kwargs):
        _r = {}
        for kw in kwargs.keys():
            if kw == 't':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_t_ld_args(**kwargs):
        _r = {}
        for kw in kwargs.keys():
            if kw == 't':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
            elif kw == 'pt_15':
                _r[kw] == kwargs[kw]
            elif kw == 'pt_1':
                _r[kw] == kwargs[kw]
        return _r

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
                    _gt[-1]:list.append((1.-_r[1])*megan.get_gamma_t_li(t[i][j], _r[0]) + _r[1]*megan.get_gamma_t_ld(t[i][j], pt_15[i][j], pt_1[i][j], _r[2], _r[3]))
            return np.array(_gt)

    @staticmethod
    def gamma_t_li(t:Union[float, np.ndarray], species:str=0,
                ldf:float=GC_MEGAN_SPECIES_CONST['ISOP']['ldf'], 
                beta:float=GC_MEGAN_SPECIES_CONST['ISOP']['beta'],
                ) -> Union[float, np.ndarray]:
        if isinstance(species, str):
            _r = megan.get_const(species, 'beta', 'ldf')
        else:
            _r = [beta, ldf]
        if not isinstance(t, np.ndarray):
            return (1.-_r[1])*megan.get_gamma_t_li(t, _r[0])
        elif isinstance(t, np.ndarray):
            _gt = []
            for i in range(t.shape[0]):
                _gt.append([])
                for j in range(t.shape[1]):
                    _gt[-1].append((1.-_r[1])*megan.get_gamma_t_li(t[i][j], _r[0]))
            return np.array(_gt)

    @staticmethod
    def gamma_t_ld(t:Union[float, np.ndarray], pt_15:Union[float, np.ndarray], pt_1:Union[float, np.ndarray], species:str=0,
                ldf:float=GC_MEGAN_SPECIES_CONST['ISOP']['ldf'], 
                ct1:float=GC_MEGAN_SPECIES_CONST['ISOP']['ct1'], 
                ceo:float=GC_MEGAN_SPECIES_CONST['ISOP']['ceo'], 
                ) -> Union[float, np.ndarray]:
        if isinstance(species, str):
            _r = megan.get_const(species, 'ldf', 'ct1', 'ceo')
        else:
            _r = [ldf, ct1, ceo]
        if not isinstance(t, np.ndarray) and not isinstance(pt_15, np.ndarray):
            return _r[0]*megan.get_gamma_t_ld(t, pt_15, pt_1, _r[1], _r[2])
        elif isinstance(t, np.ndarray) and isinstance(pt_15, np.ndarray):
            _gt = []
            for i in range(t.shape[0]):
                _gt.append([])
                for j in range(t.shape[1]):
                    _gt[-1].append(_r[0]*megan.get_gamma_t_ld(t[i][j], pt_15[i][j], pt_1[i][j], _r[1], _r[2]))
            return np.array(_gt)

    @staticmethod
    def get_gamma_t_li(t:float, beta:float) -> float:
        _gamma_t_li = np.exp(beta*(t - MEGAN_T_STANDARD))
        return _gamma_t_li

    @staticmethod
    def get_gamma_t_ld(t:float, pt_15:float, pt_1:float, ct1:float, ceo:float) -> float:
        e_opt = ceo * np.exp(0.08*(pt_15 - 2.97e2))
        t_opt = 3.13e2 + (6.0e-1 * (pt_15 - 2.97e2))
        CT2 = 200.0
        x = (1./t_opt - 1./t) / R
        c_t = e_opt * CT2 * np.exp(ct1 * x) / (CT2 - ct1 * (1.-np.exp(CT2 * x)))
        _gamma_t_ld = max(c_t, 0.)
        return _gamma_t_ld

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_p_args():
        pass

    @staticmethod
    def gamma_p():
        pass

    @staticmethod
    def get_gamma_p():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_CO2_args():
        pass

    @staticmethod
    def gamma_CO2():
        pass

    @staticmethod
    def get_gamma_CO2(species, **kwargs):
        return megan.get_gamma_CO2_ISOP(**kwargs) if species == 'ISOP' else 1

    @staticmethod
    def get_gamma_CO2_ISOP():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def get_const(species:str, *const:Tuple[str]):
        if len(const) == 1:
            return GC_MEGAN_SPECIES_CONST[species][const[0]]
        else:
            return [GC_MEGAN_SPECIES_CONST[species][c] for c in const]