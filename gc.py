# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from .data import GC_MEGAN_SPECIES_CONST
from typing import Sequence, Tuple, Union

R = 8.3144598e-3
MEGAN_T_STANDARD = 303.

class megan:
    ENABLE = {
        'norm_fac'  : False,
        'aef'       : False,
        'gamma_a'   : True,
        'gamma_sm'  : True,
        'gamma_lai' : True,
        'gamma_t_li': True,
        'gamma_t_ld': True,
        'gamma_p'   : False,
        'gamma_CO2' : True,
    }

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def emis(**kwargs):
        _r = 1.
        _sub = 1.
        _r *= megan.norm_fac() if megan.ENABLE['norm_fac'] else 1.
        _r *= megan.aef() if megan.ENABLE['aef'] else 1.
        _r *= megan.gamma_a(**megan.gamma_a_args(**kwargs)) if megan.ENABLE['gamma_a'] else 1.
        _r *= megan.gamma_sm(**megan.gamma_sm_args(**kwargs)) if megan.ENABLE['gamma_sm'] else 1.
        _r *= megan.gamma_lai(**megan.gamma_lai_args(**kwargs)) if megan.ENABLE['gamma_lai'] else 1.
        _r *= megan.gamma_CO2(**megan.gamma_CO2_args(**kwargs)) if megan.ENABLE['gamma_CO2'] else 1.
        _sub *= megan.gamma_t_ld(**megan.gamma_t_ld_args(**kwargs)) if megan.ENABLE['gamma_t_ld'] else 1.
        _sub *= megan.gamma_p() if megan.ENABLE['gamma_p'] else 1.
        _sub += megan.gamma_t_li(**megan.gamma_t_li_args(**kwargs)) if megan.ENABLE['gamma_t_li'] else 0.
        _r *= _sub
        return _r

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def norm_fac_args(**kwargs) -> dict:
        pass

    @staticmethod
    def norm_fac():
        pass

    @staticmethod
    def get_norm_fac():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def aef_args(**kwargs) -> dict:
        pass

    @staticmethod
    def aef():
        pass

    @staticmethod
    def get_aef():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_a_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 'cmlai':
                _r[kw] == kwargs[kw]
            elif kw == 'pmlai':
                _r[kw] == kwargs[kw]
            elif kw == 'dbtwn':
                _r[kw] == kwargs[kw]
            elif kw == 'tt':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_a(cmlai:Union[float, np.ndarray], pmlai:Union[float, np.ndarray], dbtwn:Union[float, np.ndarray], tt:Union[float, np.ndarray],
                 species:str='ISOP') -> Union[float, np.ndarray]:
        _r = megan.get_const(species, 'anew', 'agro', 'amat', 'aold')
        if not isinstance(cmlai, np.ndarray):
            return (1.-_r[1])*megan.get_gamma_a(cmlai, pmlai, dbtwn, tt, *_r)
        elif isinstance(cmlai, np.ndarray):
            _gt = []
            for i in range(cmlai.shape[0]):
                _gt.append([])
                for j in range(cmlai.shape[1]):
                    list.append(_gt[-1], (1.-_r[1])*megan.get_gamma_a(cmlai[i][j], pmlai[i][j], dbtwn[i][j], tt[i][j],  *_r))
            return np.array(_gt)

    @staticmethod
    def get_gamma_a(cmlai, pmlai, dbtwn, tt, an, ag, am, ao):
        if tt <= 303.0 :
            ti = 5.0 + 0.7*(300.0 - tt)
        elif tt >  303.0:
            ti = 2.9
        tm = 2.3 * ti
        if cmlai == pmlai:
            fnew = 0.
            fgro = 0.
            fmat = 0.
            fold = 0.
        elif cmlai > pmlai:
            if dbtwn > ti:
                fnew = ti/dbtwn*(1.-pmlai/cmlai)
            else:
                fnew = 1.0 - pmlai/cmlai
            if dbtwn > tm:
                fmat = pmlai/cmlai + ((dbtwn - tm )/dbtwn)*( 1.-pmlai/cmlai)
            else:
                fmat = pmlai/cmlai
            fgro = 1. - fnew - fmat
            fold = 0.
        else:
            fnew = 0.
            fgro = 0.
            fold = (pmlai - cmlai)/pmlai
            fmat = 1. - fold
            _gamma_age = fnew * an + fgro * ag + fmat * am + fold * ao
            _gamma_age = max(_gamma_age, 0.)
            return _gamma_age


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_sm_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 'gwetroot':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_sm(gwetroot:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        if not isinstance(gwetroot, np.ndarray):
            return megan.get_gamma_sm(gwetroot, species)
        elif isinstance(gwetroot, np.ndarray):
            _gt = []
            for i in range(gwetroot.shape[0]):
                _gt.append([])
                for j in range(gwetroot.shape[1]):
                    list.append(_gt[-1], megan.get_gamma_sm(gwetroot[i][j], species))
            return np.array(_gt)

    @staticmethod
    def get_gamma_sm(gwetroot:float, species:str) -> float:
        _gamma_sm = 1.
        gwetroot = min(max(gwetroot,0.),1.)
        if species == 'ALD2' or species == 'EOH':
            _gamma_sm = max(20.*gwetroot-17., 1.)
        return _gamma_sm

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_lai_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 'cmlai':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_lai(cmlai:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        if not isinstance(cmlai, np.ndarray):
            return megan.get_gamma_lai(cmlai, megan.get_const(species, 'BI'))
        elif isinstance(cmlai, np.ndarray):
            _gt = []
            for i in range(cmlai.shape[0]):
                _gt.append([])
                for j in range(cmlai.shape[1]):
                    list.append(_gt[-1], megan.get_gamma_lai(cmlai[i][j], megan.get_const(species, 'BI')))
            return np.array(_gt)

    @staticmethod
    def get_gamma_lai(cmlai:float, bidirexch:bool) -> float:
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
    def gamma_t_li_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 't':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_t_ld_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 't':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
            elif kw == 'pt_15':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_t_li(t:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        _r = megan.get_const(species, 'beta', 'ldf')
        if not isinstance(t, np.ndarray):
            return (1.-_r[1])*megan.get_gamma_t_li(t, _r[0])
        elif isinstance(t, np.ndarray):
            _gt = []
            for i in range(t.shape[0]):
                _gt.append([])
                for j in range(t.shape[1]):
                    list.append(_gt[-1], (1.-_r[1])*megan.get_gamma_t_li(t[i][j], _r[0]))
            return np.array(_gt)

    @staticmethod
    def gamma_t_ld(t:Union[float, np.ndarray], pt_15:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        _r = megan.get_const(species, 'ldf', 'ct1', 'ceo')
        if not isinstance(t, np.ndarray) and not isinstance(pt_15, np.ndarray):
            return _r[0]*megan.get_gamma_t_ld(t, pt_15, _r[1], _r[2])
        elif isinstance(t, np.ndarray) and isinstance(pt_15, np.ndarray):
            _gt = []
            for i in range(t.shape[0]):
                _gt.append([])
                for j in range(t.shape[1]):
                    list.append(_gt[-1], _r[0]*megan.get_gamma_t_ld(t[i][j], pt_15[i][j], _r[1], _r[2]))
            return np.array(_gt)

    @staticmethod
    def get_gamma_t_li(t:float, beta:float) -> float:
        _gamma_t_li = np.exp(beta*(t - MEGAN_T_STANDARD))
        return _gamma_t_li

    @staticmethod
    def get_gamma_t_ld(t:float, pt_15:float, ct1:float, ceo:float) -> float:
        e_opt = ceo * np.exp(0.08*(pt_15 - 2.97e2))
        t_opt = 3.13e2 + (6.0e-1 * (pt_15 - 2.97e2))
        CT2 = 200.0
        x = (1./t_opt - 1./t) / R
        c_t = e_opt * CT2 * np.exp(ct1 * x) / (CT2 - ct1 * (1.-np.exp(CT2 * x)))
        _gamma_t_ld = max(c_t, 0.)
        return _gamma_t_ld

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_p_args(**kwargs) -> dict:
        pass

    @staticmethod
    def gamma_p():
        pass

    @staticmethod
    def get_gamma_p():
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_CO2_args(**kwargs) -> dict:
        _r = {}
        for kw in kwargs.keys():
            if kw == 'CO2a':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_CO2(CO2a:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        if not isinstance(CO2a, np.ndarray):
            return megan.get_gamma_CO2(species, CO2a)
        elif isinstance(CO2a, np.ndarray):
            _gt = []
            for i in range(CO2a.shape[0]):
                _gt.append([])
                for j in range(CO2a.shape[1]):
                    list.append(_gt[-1], megan.get_gamma_CO2(species, CO2a[i][j]))
            return np.array(_gt)

    @staticmethod
    def get_gamma_CO2(species:float, *args, **kwargs) -> float:
        return megan.get_gamma_CO2_ISOP(*args, **kwargs) if species == 'ISOP' else 1

    @staticmethod
    def get_gamma_CO2_ISOP(CO2a:float) -> float:
        LPOSSELL    = True   # ! Default option
        LWILKINSON  = False   # ! Set .TRUE. only if LPOSSELL = .FALSE.
        if LPOSSELL:
            _gamma_CO2 = 8.9406 / ( 1.0 + 8.9406 * 0.0024 * CO2a )
        elif LWILKINSON:
            if CO2a <= 600.0:
                ISMAXi = 1.036  - (1.036 - 1.072) /    (600.0 - 400.0) * (600.0 - CO2a)
                HEXPi  = 2.0125 - (2.0125 - 1.7000) /  (600.0 - 400.0) * (600.0 - CO2a)
                CSTARi = 1150.0 - (1150.0 - 1218.0) /  (600.0 - 400.0) * (600.0 - CO2a)
            elif CO2a > 600.0 and CO2a < 800.0:
                ISMAXi = 1.046  - (1.046 - 1.036) /   (800.0 - 600.0) * (800.0 - CO2a)
                HEXPi  = 1.5380 - (1.5380 - 2.0125) /  (800.0 - 600.0) * (800.0 - CO2a)
                CSTARi = 2025.0 - (2025.0 - 1150.0) /  (800.0 - 600.0) * (800.0 - CO2a)
            else:
                ISMAXi = 1.014 - (1.014 - 1.046) /  (1200.0 - 800.0) * (1200.0 - CO2a)
                HEXPi  = 2.8610 - (2.8610 - 1.5380) /  (1200.0 - 800.0) * (1200.0 - CO2a)
                CSTARi = 1525.0 - (1525.0 - 2025.0) /  (1200.0 - 800.0) * (1200.0 - CO2a)
            ISMAXa    = 1.344
            HEXPa     = 1.4614
            CSTARa    = 585.0
            CO2i      = 0.7 * CO2a
            _gamma_CO2 = ( ISMAXi -  ISMAXi * CO2i**HEXPi /  ( CSTARi**HEXPi + CO2i**HEXPi ) )  * ( ISMAXa - ISMAXa * ( 0.7 * CO2a )**HEXPa / ( CSTARa**HEXPa + ( 0.7 * CO2a )**HEXPa ) )
        else:
            _gamma_CO2 = 1.
        return _gamma_CO2

    @staticmethod
    def get_const(species:str, *const:Tuple[str]) -> Union[float, bool, Sequence[Union[float, bool]]]:
        if len(const) == 1:
            return GC_MEGAN_SPECIES_CONST[species][const[0]]
        else:
            return [GC_MEGAN_SPECIES_CONST[species][c] for c in const]