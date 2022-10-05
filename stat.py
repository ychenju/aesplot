# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy.stats as spss
from . import auxf as aux

def arg_minp(eV: np.ndarray):
    return np.where(eV>0,eV,np.inf).argmin()

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

class corr:

    def __init__(self, *data, base='scipy', method='pearson'):
        if len(data) < 2:
            raise RuntimeError('No enough data!')
        if base == 'scipy':
            if len(data) != 2:
                raise RuntimeError('Only 2 lists of data are allowed in scipy mode')
            if aux.hasnan(data):
                raise RuntimeError('Data with NaN are not allowed in scipy mode')
            self._base = 's'
            if method.lower() in ('pearson', 'p'):
                self.result = spss.pearsonr(*data)
                self._method = 'p'
            elif method.lower() in ('spearman', 's'):
                self.result = spss.spearmanr(*data)
                self._method = 's'
            else:
                raise RuntimeError('Invalid method!')
        elif base == 'pandas':
            self._base = 'p'
            if method.lower() in ('pearson', 'p'):
                self.result = pd.DataFrame(np.array([*data]).T).corr()
                self._method = 'p'
            elif method.lower() in ('spearman', 's'):
                self.result = pd.DataFrame(np.array([*data]).T).corr(method='spearman')
                self._method = 's'

    def __call__(self):
        return self.result

    def __str__(self):
        return self.result.__str__()

    def r(self, x:int=1, y:int=0) -> float:
        if self._base == 's':
            if self._method == 'p':
                return self.result[0]
            elif self._method == 's':
                return self.result.correlation
        elif self._base == 'p':
            return self.result.iloc[y,x]

    def p(self) -> float:
        if self._base == 'p':
            raise RuntimeError('Cannot return p when the base is Pandas')
        elif self._base == 's':
            if self._method == 'p':
                return self.result[1]
            elif self._method == 's':
                return self.result.pvalue