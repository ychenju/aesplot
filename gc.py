# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from symbol import or_test
import numpy as np
from .data import GC_MEGAN_SPECIES_CONST, GC_MEGAN_PFT_EF, GC_MEGAN_EM_FRAC
from . import ascl
from .atm import sea, ssrd_to_tsolar
from . import trigo as atri
from typing import Sequence, Tuple, Union

R = 8.3144598e-3

MEGAN_T_STANDARD = 303.
WM2_TO_UMOLM2S = 4.766

class megan:

    ENABLE = {
        'norm_fac'  : True,
        'aef'       : False,
        'gamma_a'   : True,
        'gamma_sm'  : True,
        'gamma_lai' : True,
        'gamma_t_li': True,
        'gamma_t_ld': True,
        'gamma_p'   : True,
        'gamma_CO2' : True,
    }

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def emis(**kwargs):
        '''
        '''
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
    def norm_fac() -> float:
        '''
        '''
        return megan.get_norm_fac()

    @staticmethod
    def get_norm_fac() -> float:
        '''
        Calculate the normalization factor of MEGAN standard state
        '''
        PAC_DAILY = 400.0
        PHI       = 0.6
        BBB       = 1.0 + 0.0005 *( PAC_DAILY - 400.0 )
        AAA       = ( 2.46 * BBB * PHI ) - ( 0.9 * PHI**2 )
        GAMMA_P_STANDARD = 0.866 * AAA
        GAMMA_T_LI_STANDARD = 1.0
        GAMMA_SM_STANDARD = 1.0
        CMLAI = 5.0
        GAMMA_LAI_STANDARD = 0.49 * CMLAI / np.sqrt( 1.0 + 0.2 * CMLAI**2 )
        GAMMA_AGE_STANDARD = 0.1*0.6 + 0.8*1.0 + 0.1*0.9
        PT_15 = 297.0
        T     = 303.0
        R     = 8.3144598e-3
        CEO = 2.0
        CT1 = 95.0
        E_OPT = CEO * np.exp( 0.08 * ( PT_15  - 2.97e2 ) )
        T_OPT = 3.13e2 + ( 6.0e-1 * ( PT_15 - 2.97e2 ) )
        CT2   = 200.0
        X     = ( 1.0/T_OPT - 1.0/T ) / R
        GAMMA_T_LD_STANDARD = E_OPT * CT2 * np.exp( CT1 * X ) /  ( CT2 - CT1 * ( 1.0 - np.exp( CT2 * X ) ) )
        LDF = 1.0
        GAMMA_STANDARD = GAMMA_AGE_STANDARD * GAMMA_SM_STANDARD * GAMMA_LAI_STANDARD * ((1.0 - LDF) * GAMMA_T_LI_STANDARD + (LDF * GAMMA_P_STANDARD * GAMMA_T_LD_STANDARD))
        return 1. / GAMMA_STANDARD

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def aef_args(**kwargs) -> dict:
        '''
        '''
        pass

    @staticmethod
    def aef():
        '''
        '''
        pass

    @staticmethod
    def get_aef():
        """
        sfx:str = Inst.SUFFIX

        HCO_EvalFld( HcoState, 'MEGAN_AEF_ISOP'+sfx, Inst.AEF_ISOP )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_MBOX'+sfx, Inst.AEF_MBOX )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_BPIN'+sfx, Inst.AEF_BPIN )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_CARE'+sfx, Inst.AEF_CARE )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_LIMO'+sfx, Inst.AEF_LIMO )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_OCIM'+sfx, Inst.AEF_OCIM )
        HCO_EvalFld( HcoState, 'MEGAN_AEF_SABI'+sfx, Inst.AEF_SABI )
        HCO_EvalFld( HcoState, 'MEGAN_ORVC'+sfx, Inst.GEIA_ORVC )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BARE'+sfx, PFT_BARE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_NDLF_EVGN_TMPT_TREE'+sfx, PFT_NDLF_EVGN_TMPT_TREE ) 
        HCO_EvalFld( HcoState, 'CLM4_PFT_NDLF_EVGN_BORL_TREE'+sfx, PFT_NDLF_EVGN_BORL_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_NDLF_DECD_BORL_TREE'+sfx, PFT_NDLF_DECD_BORL_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_EVGN_TROP_TREE'+sfx, PFT_BDLF_EVGN_TROP_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_EVGN_TMPT_TREE'+sfx, PFT_BDLF_EVGN_TMPT_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_DECD_TROP_TREE'+sfx, PFT_BDLF_DECD_TROP_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_DECD_TMPT_TREE'+sfx, PFT_BDLF_DECD_TMPT_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_DECD_BORL_TREE'+sfx, PFT_BDLF_DECD_BORL_TREE )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_EVGN_SHRB'+sfx, PFT_BDLF_EVGN_SHRB )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_DECD_TMPT_SHRB'+sfx, PFT_BDLF_DECD_TMPT_SHRB )
        HCO_EvalFld( HcoState, 'CLM4_PFT_BDLF_DECD_BORL_SHRB'+sfx, PFT_BDLF_DECD_BORL_SHRB )
        HCO_EvalFld( HcoState, 'CLM4_PFT_C3_ARCT_GRSS'+sfx, PFT_C3_ARCT_GRSS )
        HCO_EvalFld( HcoState, 'CLM4_PFT_C3_NARC_GRSS'+sfx, PFT_C3_NARC_GRSS )
        HCO_EvalFld( HcoState, 'CLM4_PFT_C4_GRSS'+sfx, PFT_C4_GRSS )
        HCO_EvalFld( HcoState, 'CLM4_PFT_CROP'+sfx, PFT_CROP )

        Inst.ARRAY_16[:,:, 1] = PFT_BARE
        Inst.ARRAY_16[:,:, 2] = PFT_NDLF_EVGN_TMPT_TREE
        Inst.ARRAY_16[:,:, 3] = PFT_NDLF_EVGN_BORL_TREE
        Inst.ARRAY_16[:,:, 4] = PFT_NDLF_DECD_BORL_TREE
        Inst.ARRAY_16[:,:, 5] = PFT_BDLF_EVGN_TROP_TREE
        Inst.ARRAY_16[:,:, 6] = PFT_BDLF_EVGN_TMPT_TREE
        Inst.ARRAY_16[:,:, 7] = PFT_BDLF_DECD_TROP_TREE
        Inst.ARRAY_16[:,:, 8] = PFT_BDLF_DECD_TMPT_TREE
        Inst.ARRAY_16[:,:, 9] = PFT_BDLF_DECD_BORL_TREE
        Inst.ARRAY_16[:,:,10] = PFT_BDLF_EVGN_SHRB
        Inst.ARRAY_16[:,:,11] = PFT_BDLF_DECD_TMPT_SHRB
        Inst.ARRAY_16[:,:,12] = PFT_BDLF_DECD_BORL_SHRB
        Inst.ARRAY_16[:,:,13] = PFT_C3_ARCT_GRSS
        Inst.ARRAY_16[:,:,14] = PFT_C3_NARC_GRSS
        Inst.ARRAY_16[:,:,15] = PFT_C4_GRSS
        Inst.ARRAY_16[:,:,16] = PFT_CROP


        for p in range(1,1+15):
            Inst.AEF_APIN[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('APIN', p)
            Inst.AEF_MYRC[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('MYRC', p)
            Inst.AEF_OMON[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('OMON', p)
            Inst.AEF_FARN[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('FARN', p)
            Inst.AEF_BCAR[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('BCAR', p)
            Inst.AEF_OSQT[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('OSQT', p)
            Inst.AEF_MOH[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('MOH', p)
            Inst.AEF_ACET[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('ACET', p)
            Inst.AEF_EOH[:,:] += Inst.ARRAY_16[:,:,ARR_IND]* megan.pft_ef('BIDR', p)* megan.em_frac('EOH', p)
            Inst.AEF_CH2O[:,:] += Inst.ARRAY_16[:,:,ARR_IND]* megan.pft_ef('BIDR', p)* megan.em_frac('CH2O', p)
            Inst.AEF_ALD2[:,:] += Inst.ARRAY_16[:,:,ARR_IND]* megan.pft_ef('BIDR', p)* megan.em_frac('ALD2', p)
            Inst.AEF_FAXX[:,:] += Inst.ARRAY_16[:,:,ARR_IND]* megan.pft_ef('BIDR', p)* megan.em_frac('FAXX', p)
            Inst.AEF_AAXX[:,:] += Inst.ARRAY_16[:,:,ARR_IND]* megan.pft_ef('BIDR', p)* megan.em_frac('AAXX', p)
            Inst.AEF_C2H4[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('STRS', p) * 0.58
            Inst.AEF_TOLU[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('STRS', p) * 0.03
            Inst.AEF_HCNX[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('STRS', p) * 0.015
            Inst.AEF_PRPE[:,:] += Inst.ARRAY_16[:,:,ARR_IND] * megan.pft_ef('OTHR', p) * 0.722

        FACTOR = 1.0e-9 / 3600.0

        for j in range(1, HcoState.NY):
            for i in range(1, 1+HcoState.Nx):

                Inst.AEF_APIN[i,j] *= FACTOR * 120.0 / 136.234
                Inst.AEF_MYRC[i,j] *= FACTOR * 120.0 / 136.234
                Inst.AEF_OMON[i,j] *= FACTOR * 120.0 / 136.234

                #    ! Sesquiterpenes
                SPECIES2CARBON = 15. * 12.01 / ( 15. * 12.01 + 24. * 1.01 )
                Inst.AEF_FARN[i,j] *= FACTOR * SPECIES2CARBON
                Inst.AEF_BCAR[i,j] *= FACTOR * SPECIES2CARBON
                Inst.AEF_OSQT[i,j] *= FACTOR * SPECIES2CARBON

                Inst.AEF_ACET[i,j] *= FACTOR *  36.0 /  58.079
                Inst.AEF_EOH[i,j]  *= FACTOR *  24.0 /  46.068
                Inst.AEF_ALD2[i,j] *= FACTOR *  24.0 /  44.053
                Inst.AEF_C2H4[i,j] *= FACTOR *  24.0 /  28.053
                Inst.AEF_TOLU[i,j] *= FACTOR *  84.0 /  92.138
                Inst.AEF_PRPE[i,j] *= FACTOR *  36.0 /  42.080

                #    ! Methanol, formaldehyde, formic acid, acetic acid, HCN are
                #    ! carried in kg, not kg C
                #    ! Convert AEF arrays to [kg/m2/s]
                Inst.AEF_MOH[i,j]  *= FACTOR
                Inst.AEF_CH2O[i,j] *= FACTOR
                Inst.AEF_FAXX[i,j] *= FACTOR
                Inst.AEF_AAXX[i,j] *= FACTOR
                Inst.AEF_HCNX[i,j] *= FACTOR

        return Inst

    # ENDDO
    # ENDDO

    # ! Return w/ success
    # RC = HCO_SUCCESS
    """

    @staticmethod
    def pft_ef(category:str, *efx:Tuple[int]) -> Union[float, Sequence[float]]:
        '''
        '''
        if len(efx) == 1:
            return GC_MEGAN_PFT_EF[category][efx[0]-1]
        else:
            return [GC_MEGAN_PFT_EF[category][c-1] for c in efx]

    @staticmethod
    def em_frac(category:str, *efx:Tuple[int]) -> Union[float, Sequence[float]]:
        '''
        '''
        if len(efx) == 1:
            return GC_MEGAN_EM_FRAC[category][efx[0]-1]
        else:
            return [GC_MEGAN_EM_FRAC[category][c-1] for c in efx]


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_a_args(**kwargs) -> dict:
        '''
        '''
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
        '''
        '''
        _r = megan.get_const(species, 'anew', 'agro', 'amat', 'aold')
        if not isinstance(cmlai, np.ndarray):
            return megan.get_gamma_a(cmlai, pmlai, dbtwn, tt, *_r)
        elif isinstance(cmlai, np.ndarray):
            _gt = np.zeros(cmlai.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = megan.get_gamma_a(cmlai[i,j], pmlai[i,j], dbtwn[i,j], tt[i,j],  *_r)
            return np.array(_gt)

    @staticmethod
    def get_gamma_a(cmlai:float, pmlai:float, dbtwn:float, tt:float, an:float, ag:float, am:float, ao:float) -> float:
        '''
        '''
        if np.isnan(cmlai) or np.isnan(pmlai) or np.isnan(dbtwn) or np.isnan(tt):
            return np.nan            
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
        '''
        '''
        _r = {}
        for kw in kwargs.keys():
            if kw == 'gwetroot':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_sm(gwetroot:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        '''
        if not isinstance(gwetroot, np.ndarray):
            return megan.get_gamma_sm(gwetroot, species)
        elif isinstance(gwetroot, np.ndarray):
            _gt = np.zeros(gwetroot.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = megan.get_gamma_sm(gwetroot[i,j], species)
            return np.array(_gt)

    @staticmethod
    def get_gamma_sm(gwetroot:float, species:str) -> float:  
        '''
        '''      
        if np.isnan(gwetroot):
            return np.nan 
        _gamma_sm = 1.
        gwetroot = min(max(gwetroot,0.),1.)
        if species == 'ALD2' or species == 'EOH':
            _gamma_sm = max(20.*gwetroot-17., 1.)
        return _gamma_sm

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_lai_args(**kwargs) -> dict:
        '''
        '''
        _r = {}
        for kw in kwargs.keys():
            if kw == 'cmlai':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_lai(cmlai:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        '''
        if not isinstance(cmlai, np.ndarray):
            return megan.get_gamma_lai(cmlai, megan.get_const(species, 'BI'))
        elif isinstance(cmlai, np.ndarray):
            _gt = np.zeros(cmlai.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = megan.get_gamma_lai(cmlai[i,j], megan.get_const(species, 'BI'))
            return np.array(_gt)

    @staticmethod
    def get_gamma_lai(cmlai:float, bidirexch:bool) -> float:
        '''
        '''
        if np.isnan(cmlai):
            return np.nan 
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
        '''
        '''
        _r = {}
        for kw in kwargs.keys():
            if kw == 't':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_t_ld_args(**kwargs) -> dict:
        '''
        '''
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
        '''
        '''
        _r = megan.get_const(species, 'beta', 'ldf')
        if not isinstance(t, np.ndarray):
            return (1.-_r[1])*megan.get_gamma_t_li(t, _r[0])
        elif isinstance(t, np.ndarray):
            _gt = np.zeros(t.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = (1.-_r[1])*megan.get_gamma_t_li(t[i,j], _r[0])
            return np.array(_gt)

    @staticmethod
    def gamma_t_ld(t:Union[float, np.ndarray], pt_15:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        '''
        _r = megan.get_const(species, 'ldf', 'ct1', 'ceo')
        if not isinstance(t, np.ndarray) and not isinstance(pt_15, np.ndarray):
            return _r[0]*megan.get_gamma_t_ld(t, pt_15, _r[1], _r[2])
        elif isinstance(t, np.ndarray) and isinstance(pt_15, np.ndarray):
            _gt = np.zeros(t.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = _r[0]*megan.get_gamma_t_ld(t[i,j], pt_15[i,j], _r[1], _r[2])
            return np.array(_gt)

    @staticmethod
    def get_gamma_t_li(t:float, beta:float) -> float:
        '''
        '''
        if np.isnan(t):
            return np.nan
        _gamma_t_li = np.exp(beta*(t - MEGAN_T_STANDARD))
        return _gamma_t_li

    @staticmethod
    def get_gamma_t_ld(t:float, pt_15:float, ct1:float, ceo:float) -> float:
        '''
        '''
        if np.isnan(t) or np.isnan(pt_15):
            return np.nan
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
        '''
        '''
        _r = {}
        for kw in kwargs.keys():
            if kw == 'q_dir_2':
                _r[kw] == kwargs[kw]
            elif kw == 'q_diff_2':
                _r[kw] == kwargs[kw]
            elif kw == 'pardr_avg_sim':
                _r[kw] == kwargs[kw]
            elif kw == 'pardf_avg_sim':
                _r[kw] == kwargs[kw]
            elif kw == 'timeobj':
                _r[kw] == kwargs[kw]
            elif kw == 'lat':
                _r[kw] == kwargs[kw]
            elif kw == 'long':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_p(pardr:Union[float, np.ndarray], pardf:Union[float, np.ndarray], pardr_avg_sim:Union[float, np.ndarray], pardf_avg_sim:Union[float, np.ndarray],
                timeobj:Union[ascl.dt, np.ndarray], lat:Union[float, np.ndarray], long:Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        '''
        The original 'gamma_p()' adding to a preprocessing module of 'gamma_p' calculation \n
        PARDR = 0.8 * pardb \n
        PARDF = 0.8 * pardif \n
        q_dir_2 = PARDR * WM2_TO_UMOLM2S \n
        q_diff_2 = PARDF * WM2_TO_UMOLM2S \n
        pardr_avg_sim = PARDR_LASTXDAYS \n
        pardf_avg_sim = PARDF_LASTXDAYS \n
        '''
        return megan.gamma_p_sub(pardr*WM2_TO_UMOLM2S, pardf*WM2_TO_UMOLM2S, pardr_avg_sim, pardf_avg_sim, timeobj, lat, long)

    @staticmethod
    def gamma_p_sub(q_dir_2:Union[float, np.ndarray], q_diff_2:Union[float, np.ndarray], pardr_avg_sim:Union[float, np.ndarray], pardf_avg_sim:Union[float, np.ndarray],
                timeobj:Union[ascl.dt, np.ndarray], lat:Union[float, np.ndarray], long:Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        '''
        The original 'gamma_p()'
        '''
        if not isinstance(q_dir_2, np.ndarray):
            return megan.get_gamma_p(q_dir_2, q_diff_2, pardr_avg_sim, pardf_avg_sim, timeobj, lat, long)
        elif isinstance(q_dir_2, np.ndarray):
            _gt = np.zeros(q_dir_2.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = megan.get_gamma_p(q_dir_2[i,j], q_diff_2[i,j], pardr_avg_sim[i,j], pardf_avg_sim[i,j], timeobj, lat[i,j], long[i,j])
            return np.array(_gt)

    @staticmethod
    def get_gamma_p(q_dir_2:float, q_diff_2:float, pardr_avg_sim:float, pardf_avg_sim:float, timeobj:ascl.dt, lat:float, long:float) -> float:
        '''
        '''
        if np.isnan(q_dir_2) or np.isnan(q_diff_2) or np.isnan(pardr_avg_sim) or np.isnan(pardf_avg_sim) or np.isnan(lat) or np.isnan(long):
            return np.nan
        ptoa   = 0.0
        mm_pardr_daily = pardr_avg_sim  * WM2_TO_UMOLM2S
        mm_pardf_daily = pardf_avg_sim  * WM2_TO_UMOLM2S
        pac_daily    = mm_pardr_daily + mm_pardf_daily
        pac_instant  = q_dir_2       +  q_diff_2
        doy = ascl.gc.toyd(*timeobj.date)[1]
        beta = sea(lat, long, timeobj)
        sinbeta = atri.sind(beta)
        if sinbeta <= 0.:
            gamma_p_pceea = 0.
        elif sinbeta > 0.:
            ptoa    = 3000.0 + 99. * np.cos( 2. * np.pi * ( doy - 10.0 ) / 365.0 )
            phi     = pac_instant / ( sinbeta * ptoa )
            _b     = 1.0 + 0.0005 *( pac_daily - 400.0 )
            _a     = ( 2.46 * _b * phi ) - ( 0.9 * phi**2 )
            gamma_p_pceea = sinbeta * _a
        if ( beta < 1.0 and gamma_p_pceea > 0.1 ):
            gamma_p_pceea  = 0.0
        gamma_p_pceea = max( gamma_p_pceea , 0.0)
        return gamma_p_pceea

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def gamma_CO2_args(**kwargs) -> dict:
        '''
        '''
        _r = {}
        for kw in kwargs.keys():
            if kw == 'CO2a':
                _r[kw] == kwargs[kw]
            elif kw == 'species':
                _r[kw] == kwargs[kw]
        return _r

    @staticmethod
    def gamma_CO2(CO2a:Union[float, np.ndarray], species:str='ISOP') -> Union[float, np.ndarray]:
        '''
        '''
        if not isinstance(CO2a, np.ndarray):
            return megan.get_gamma_CO2(species, CO2a)
        elif isinstance(CO2a, np.ndarray):
            _gt = np.zeros(CO2a.shape)
            for i in range(_gt.shape[0]):
                for j in range(_gt.shape[1]):
                    _gt[i,j] = megan.get_gamma_CO2(species, CO2a[i,j])
            return np.array(_gt)

    @staticmethod
    def get_gamma_CO2(species:float, *args, **kwargs) -> float:
        '''
        '''
        return megan.get_gamma_CO2_ISOP(*args, **kwargs) if species == 'ISOP' else 1

    @staticmethod
    def get_gamma_CO2_ISOP(CO2a:float, CO2_inhibition_scheme:str='lpossell') -> float:
        '''
        '''
        if np.isnan(CO2a):
            return np.nan
        if CO2_inhibition_scheme.upper() == 'LPOSSELL':
            LPOSSELL    = True
            LWILKINSON  = False
        elif CO2_inhibition_scheme.upper() == 'LWINKINSON':
            LWILKINSON  = True
            LPOSSELL    = False
        else:
            LPOSSELL    = False
            LWILKINSON  = False
        if LPOSSELL:
            _gamma_CO2 = 8.9406 / (1.0 + 8.9406 * 0.0024 * CO2a)
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
            _gamma_CO2 = (ISMAXi - ISMAXi * CO2i**HEXPi / (CSTARi**HEXPi + CO2i**HEXPi))*(ISMAXa - ISMAXa*(0.7*CO2a)**HEXPa / (CSTARa**HEXPa + (0.7 * CO2a)**HEXPa))
        else:
            _gamma_CO2 = 1.
        return _gamma_CO2

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    SPECIES_LIST = (
        'ISOP',
        'MBOX',
        'MYRC',
        'SABI',
        'APIN',
        'LIMO',
        'CARE',
        'BPIN',
        'OCIM',
        'OMON',
        'MOH' ,
        'ACET',
        'EOH' ,
        'CH2O',
        'ALD2',
        'FAXX',
        'AAXX',
        'C2H4',
        'TOLU',
        'HCNX',
        'PRPE',
        'FARN',
        'BCAR',
        'OSQT',
    )

    @staticmethod
    def get_const(species:str, *const:Tuple[str]) -> Union[float, bool, Sequence[Union[float, bool]]]:
        '''
        '''
        if len(const) == 1:
            return GC_MEGAN_SPECIES_CONST[species][const[0]]
        else:
            return [GC_MEGAN_SPECIES_CONST[species][c] for c in const]

class coupler:

    @staticmethod
    def getpar(tsolar:float, pres:float, zen:float) -> Tuple[float]:
        '''
        Inputs
        tsolar  ! modeled or observed total radiation (W/m2) \n
        pres    ! atmospheric pressure (mb) \n
        zen     ! solar zenith angle (radians) \n

        Outputs (pardb, pardif) \n
        pardb   ! direct beam PAR (umol/m2-s) now (W/m^2) \n
        pardif  ! diffuse PAR (umol/m2-s) now (W/m^2) \n
        '''
        if zen >= 1.51844 or tsolar <= 0:
            return 0, 0
        ot = pres / 1013.25 / np.cos(zen)
        rdvis = 600. * np.exp(-0.185*ot) * np.cos(zen)
        rfvis = 0.42 * (600 - rdvis) * np.cos(zen)
        wa = 1320 * 0.077 * (2. * ot)**0.3
        rdir = (720. * np.exp(-0.06 * ot) - wa) * np.cos(zen)
        rfir = 0.65 * (720. - wa - rdir) * np.cos(zen)
        rvt = rdvis + rfvis
        rirt = rdir + rfir
        fvis = rvt/(rirt + rvt)
        ratio = tsolar /(rirt + rvt)
        if ratio >= 0.89:
            fvb = rdvis/rvt * 0.941124
        elif ratio <= 0.21:
            fvb = rdvis/rvt * 9.55E-3
        else:
            fvb = rdvis/rvt * (1.-((0.9 - ratio)/0.7)**0.666667)
        fvd = 1. - fvb
        pardb = tsolar * fvis * fvb
        pardif = tsolar * fvis * fvd
        return pardb, pardif

    @staticmethod
    def getparfromssrd(ssrd:float, pres:float, lat:float, long:float, date:Union[str, ascl.dt]) -> Tuple[float]:
        '''
        Get PAR from SSRD instead of tsolar. LAT, LONG &amp; timeobj are required
        '''
        _sea = sea(lat, long, date)
        szar = atri.d2r(90.-_sea)
        return coupler.getpar(ssrd_to_tsolar(lat, long, date, ssrd), pres, szar)

    @staticmethod
    def getpardr(tsolar:float, pres:float, zen:float) -> float:
        '''
        Inputs
        tsolar  ! modeled or observed total radiation (W/m2) \n
        pres    ! atmospheric pressure (mb) \n
        zen     ! solar zenith angle (radians) \n

        Outputs (pardb, pardif) \n
        pardb   ! direct beam PAR (umol/m2-s) now (W/m^2) \n
        pardif  ! diffuse PAR (umol/m2-s) now (W/m^2) \n
        '''
        if zen >= 1.51844 or tsolar <= 0:
            return 0, 0
        ot = pres / 1013.25 / np.cos(zen)
        rdvis = 600. * np.exp(-0.185*ot) * np.cos(zen)
        rfvis = 0.42 * (600 - rdvis) * np.cos(zen)
        wa = 1320 * 0.077 * (2. * ot)**0.3
        rdir = (720. * np.exp(-0.06 * ot) - wa) * np.cos(zen)
        rfir = 0.65 * (720. - wa - rdir) * np.cos(zen)
        rvt = rdvis + rfvis
        rirt = rdir + rfir
        fvis = rvt/(rirt + rvt)
        ratio = tsolar /(rirt + rvt)
        if ratio >= 0.89:
            fvb = rdvis/rvt * 0.941124
        elif ratio <= 0.21:
            fvb = rdvis/rvt * 9.55E-3
        else:
            fvb = rdvis/rvt * (1.-((0.9 - ratio)/0.7)**0.666667)
        fvd = 1. - fvb
        pardb = tsolar * fvis * fvb
        pardif = tsolar * fvis * fvd
        return pardb * 0.8

    @staticmethod
    def getpardf(tsolar:float, pres:float, zen:float) -> float:
        '''
        Inputs
        tsolar  ! modeled or observed total radiation (W/m2) \n
        pres    ! atmospheric pressure (mb) \n
        zen     ! solar zenith angle (radians) \n

        Outputs (pardb, pardif) \n
        pardb   ! direct beam PAR (umol/m2-s) now (W/m^2) \n
        pardif  ! diffuse PAR (umol/m2-s) now (W/m^2) \n
        '''
        if zen >= 1.51844 or tsolar <= 0:
            return 0, 0
        ot = pres / 1013.25 / np.cos(zen)
        rdvis = 600. * np.exp(-0.185*ot) * np.cos(zen)
        rfvis = 0.42 * (600 - rdvis) * np.cos(zen)
        wa = 1320 * 0.077 * (2. * ot)**0.3
        rdir = (720. * np.exp(-0.06 * ot) - wa) * np.cos(zen)
        rfir = 0.65 * (720. - wa - rdir) * np.cos(zen)
        rvt = rdvis + rfvis
        rirt = rdir + rfir
        fvis = rvt/(rirt + rvt)
        ratio = tsolar /(rirt + rvt)
        if ratio >= 0.89:
            fvb = rdvis/rvt * 0.941124
        elif ratio <= 0.21:
            fvb = rdvis/rvt * 9.55E-3
        else:
            fvb = rdvis/rvt * (1.-((0.9 - ratio)/0.7)**0.666667)
        fvd = 1. - fvb
        pardb = tsolar * fvis * fvb
        pardif = tsolar * fvis * fvd
        return pardif * 0.8

    @staticmethod
    def getpardr_fromssrd(ssrd:float, pres:float, lat:float, long:float, date:Union[str, ascl.dt]) -> float:
        '''
        Get PAR from SSRD instead of tsolar. LAT, LONG &amp; timeobj are required
        '''
        _sea = sea(lat, long, date)
        szar = atri.d2r(90.-_sea)
        return coupler.getpardr(ssrd_to_tsolar(lat, long, date, ssrd), pres, szar)    

    @staticmethod
    def getpardf_fromssrd(ssrd:float, pres:float, lat:float, long:float, date:Union[str, ascl.dt]) -> float:
        '''
        Get PAR from SSRD instead of tsolar. LAT, LONG &amp; timeobj are required
        '''
        _sea = sea(lat, long, date)
        szar = atri.d2r(90.-_sea)
        return coupler.getpardf(ssrd_to_tsolar(lat, long, date, ssrd), pres, szar)