# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import time
import numpy as np
import pandas as pd
from typing import Tuple, Sequence
from . import ascl

class Time:
    start_time = 0
    end_time = 0

class perfcounter(Time):
    def __init__(self) -> None:
        '''
        '''
        self.start_time = time.perf_counter()

    def reset(self) -> None:
        '''
        '''
        self.start_time = time.perf_counter()

    def s(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{self.end_time - self.start_time} s')
        return self.end_time - self.start_time

    def ms(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)*1000.} ms')
        return (self.end_time - self.start_time)*1000.

    def min(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)/60.} min')
        return (self.end_time - self.start_time)/60.

    def mins(self, label='Time', verbose=True) -> Tuple:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')
        return (self.end_time - self.start_time)//60, (self.end_time - self.start_time)%60

    def h(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)/3600.} h')
        return (self.end_time - self.start_time)/3600.

    def hms(self, label='Time', verbose=True) -> Tuple:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')
        return (self.end_time - self.start_time)//3600, (self.end_time - self.start_time)%3600//60, (self.end_time - self.start_time)%60

class processtime(Time):
    def __init__(self) -> None:
        '''
        '''
        self.start_time = time.process_time()

    def reset(self) -> None:
        '''
        '''
        self.start_time = time.process_time()

    def s(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{self.end_time - self.start_time} s')
        return self.end_time - self.start_time

    def ms(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)*1000.} ms')
        return (self.end_time - self.start_time)*1000.

    def min(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)/60.} min')
        return (self.end_time - self.start_time)/60.

    def mins(self, label='Time', verbose=True) -> Tuple:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')
        return (self.end_time - self.start_time)//60, (self.end_time - self.start_time)%60

    def h(self, label='Time', verbose=True) -> float:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)/3600.} h')
        return (self.end_time - self.start_time)/3600.

    def hms(self, label='Time', verbose=True) -> Tuple:
        '''
        '''
        self.end_time = time.perf_counter()
        if verbose:
            print(f'{label}:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')
        return (self.end_time - self.start_time)//3600, (self.end_time - self.start_time)%3600//60, (self.end_time - self.start_time)%60

def fileout(path:str, mode:str, *content:Tuple[str], tab=False) -> None:
    '''
    '''
    with open(path, mode) as theF:
        for c in content:
            if tab:
                theF.write(f'{c},\t')
            else:
                theF.write(f'{c},')
        theF.write('\n')

def fold(table:Sequence, length:int) -> np.ndarray:
    '''
    '''
    r = []
    for i in range(len(table)//length):
        r.append([])
        for j in range(length):
            r[-1].append(table[i*length+j])
    return np.array(r)

def npfold(table:np.ndarray, length:int) -> np.ndarray:
    '''
    '''
    try:
        if not isinstance(table, np.ndarray):
            table = np.array(table)
        return np.array(table).reshape(-1, length)
    except:
        raise RuntimeError('Cannot \'npfold\'. Please try \'fold\' instead')

def tocsv(table:np.ndarray, path:str, **kwargs) -> pd.DataFrame:
    '''
    '''
    _df = pd.DataFrame(table)
    _df.to_csv(path, **kwargs)
    return _df

def listdir(path: str, full=False, sort=True) -> Sequence[str]:
    '''
    '''
    paths = os.listdir(path)
    if sort:
        if full:
            r = [f'{path}\\{p}' for p in paths]
        else:
            r = [f'{p}' for p in paths]
        r = sorted(r, key=lambda k: [ord(i) for i in k], reverse=False)
        return r
    else:
        if full:
            return [f'{path}\\{p}' for p in paths]
        else:
            return [f'{p}' for p in paths]

def dirref(pattern:re.Pattern, path:str, full=True, in_os='windows', sort=True) -> Sequence[str]:
    '''
    DIRectory Regular Expression Find
    '''
    paths = os.listdir(path)
    if in_os.lower() == 'windows':
        rp = []
        for p in paths:
            if re.search(pattern, p, re.I):
                rp.append(p)
    elif in_os.lower() == 'linux':
        rp = []
        for p in paths:
            if re.search(pattern, p):
                rp.append(p)
    if sort:
        if not full:
            rp = sorted(rp, key=lambda k: [ord(i) for i in k], reverse=False)
            return rp
        else:
            rp2 = [f'{path}\\{p}' for p in rp]
            rp2 = sorted(rp2, key=lambda k: [ord(i) for i in k], reverse=False)
            return rp2
    else:
        if not full:
            return rp
        else:
            rp2 = [f'{path}\\{p}' for p in rp]
            return rp2

def ref(pattern:re.Pattern, strs:str, reI:bool=True) -> Sequence[str]:
    '''
    Regular Expression Filter
    '''
    rp = []
    for p in strs:
        if reI:
            if re.search(pattern, p, re.I):
                rp.append(p)
        else:
            if re.search(pattern, p):
                rp.append(p)
    return rp

def log(path:str, *content:Tuple[str]) -> None:
    '''
    '''
    with open(path, 'a') as theF:
        theF.write(f'{ascl.now()("-")},\t')
        for c in content:
            theF.write(f'{c},\t')
        theF.write('\n')