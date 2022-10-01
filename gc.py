# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

R = 8.3144598e-3

class megan:

    T_STANDARD = 303.

    @staticmethod
    def get_gamma_t_li(t, beta):
        gamma_t_li = np.exp(beta*(t - megan.T_STANDARD))
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

    CEO_ISOP = 2.0
    CT1_ISOP = 95.0