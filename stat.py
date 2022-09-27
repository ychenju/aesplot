# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def arg_minp(eV: np.ndarray):
    return np.where(eV>0,eV,np.inf).argmin()

def pfit(X: np.ndarray, Y: np.ndarray, T: np.ndarray):
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

def rmse(T: np.ndarray):
    T_ = T.reshape(-1)
    return np.sqrt(np.nanmean(T_*T_))

def sigma(X, Y, T):
    _, Tr = pfit(X,Y,T)
    return rmse(Tr)