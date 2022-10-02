# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

R = 8.3144598e-3

MEGAN_T_STANDARD = 303.

MEGAN_SPECIES_CONST = {
    'ISOP': {'beta': 0.13, 'ldf': 1.0, 'ct1': 95.0, 'ceo': 2.00, 'anew': 0.05, 'agro': 0.6, 'amat': 1.0, 'aold': 0.90, 'BI': False},
    'MBOX': {'beta': 0.13, 'ldf': 1.0, 'ct1': 95.0, 'ceo': 2.00, 'anew': 0.05, 'agro': 0.6, 'amat': 1.0, 'aold': 0.90, 'BI': False},
    'MYRC': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'SABI': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'APIN': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'LIMO': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'CARE': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'BPIN': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'OCIM': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'OMON': {'beta': 0.10, 'ldf': 0.4, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'MOH' : {'beta': 0.08, 'ldf': 0.8, 'ct1': 60.0, 'ceo': 1.60, 'anew': 3.50, 'agro': 3.0, 'amat': 1.0, 'aold': 1.20, 'BI': False},
    'ACET': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'EOH' : {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'CH2O': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'ALD2': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'FAXX': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'AAXX': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'C2H4': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'TOLU': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'HCNX': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'PRPE': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'FARN': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
    'BCAR': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
    'OSQT': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
}

class megan:

    @staticmethod
    def gamma_t(t, pt_15, pt_1, species=0,
                ldf=MEGAN_SPECIES_CONST['ISOP']['ldf'], 
                beta=MEGAN_SPECIES_CONST['ISOP']['beta'], 
                ct1=MEGAN_SPECIES_CONST['ISOP']['ct1'], 
                ceo=MEGAN_SPECIES_CONST['ISOP']['ceo'], 
                ):
        if isinstance(species, str):
            _r = megan.get_const(species, 'beta', 'ldf', 'ct1', 'ceo')
        else:
            _r = [beta, ldf, ct1, ceo]
        return (1.-_r[1])*megan.get_gamma_t_li(t, _r[0]) + _r[1]*megan.get_gamma_t_ld(t, pt_15, pt_1, _r[2], _r[3])

    @staticmethod
    def get_gamma_t_li(t, beta):
        gamma_t_li = np.exp(beta*(t - MEGAN_T_STANDARD))
        return gamma_t_li

    @staticmethod
    def get_gamma_t_ld(t, pt_15, pt_1, ct1, ceo):
        e_opt = ceo * np.exp(0.08*(pt_15 - 2.97e2))
        t_opt = 3.13e2 + (6.0e-1 * (pt_15 - 2.97e2))
        CT2 = 200.0
        x = (1./t_opt - 1./t) / R
        c_t = e_opt * CT2 * np.exp(ct1 * x) / (CT2 - ct1 * (1.-np.exp(CT2 * x)))
        gamma_t_ld = max(c_t, 0.)
        return gamma_t_ld

    @staticmethod
    def get_const(species, *const):
        if len(const) == 1:
            return MEGAN_SPECIES_CONST[species][const[0]]
        else:
            return [MEGAN_SPECIES_CONST[species][c] for c in const]
