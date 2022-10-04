# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as spss

def arg_minp(eV: np.ndarray):
    return np.where(eV>0,eV,np.inf).argmin()

# plane fitting
def planefit(X: np.ndarray, Y: np.ndarray, T: np.ndarray):
    X_ = X.reshape(-1)
    Y_ = Y.reshape(-1)
    T_ = T.reshape(-1)

    M_ = np.array([[np.nanmean(X_*X_)-np.nanmean(X_)**2, np.nanmean(X_*Y_)-np.nanmean(X_)*np.nanmean(Y_), np.nanmean(X_*T_)-np.nanmean(X_)*np.nanmean(T_)],
                   [np.nanmean(X_*Y_)-np.nanmean(X_)*np.nanmean(Y_), np.nanmean(Y_*Y_)-np.nanmean(Y_)**2, np.nanmean(Y_*T_)-np.nanmean(Y_)*np.nanmean(T_)],
                   [np.nanmean(X_*T_)-np.nanmean(X_)*np.nanmean(T_), np.nanmean(Y_*T_)-np.nanmean(Y_)*np.nanmean(T_), np.nanmean(T_*T_)-np.nanmean(T_)**2]])

    eValue, eVector = np.linalg.eig(M_)

    fVec = eVector.T[arg_minp(eValue)]
    A0 = -fVec[0]/fVec[2]
    B0 = -fVec[1]/fVec[2]
    T0 = -A0*np.nanmean(X_) - B0*np.nanmean(Y_) + np.nanmean(T_)

    T1 = T0 + A0*X + B0*Y
    Tr = T - T1       

    return T1, Tr

def rms(T: np.ndarray):
    T_ = T.reshape(-1)
    return np.sqrt(np.nanmean(T_*T_))

def sigma(X: np.ndarray, Y: np.ndarray, T: np.ndarray):
    _, Tr = planefit(X,Y,T)
    return rms(Tr)

def sigmawithoutfit(T: np.ndarray):
    Tr = T - np.nanmean(T)
    return rms(Tr)

def iserrsigma(sigma: float, table: np.ndarray):
    if sigma > np.array(table.reshape(-1)).max() - np.array(table.reshape(-1)).min():
        return True
    else:
        return False

# -*- update: v0.4.12 -*-

class linreg:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._linregress = spss.linregress(x, y)

    def __call__(self):
            return self._linregress
    
    @property
    def slope(self):
        return self._linregress.slope

    @property
    def k(self):
        return self._linregress.slope

    @property
    def intercept(self):
        return self._linregress.intercept

    @property
    def b(self):
        return self._linregress.intercept

    @property
    def rvalue(self):
        return self._linregress.rvalue

    @property
    def r(self):
        return self._linregress.rvalue

    @property
    def R2(self):
        return self._linregress.rvalue**2

    @property
    def pvalue(self):
        return self._linregress.pvalue

    @property
    def p(self):
        return self._linregress.pvalue

    @property
    def stderr(self):
        return self._linregress.stderr

    @property
    def intercept_stderr(self):
        return self._linregress.intercept_stderr

    def f(self, x):
        return self.k * x + self.b

