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

    def s(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{self.end_time - self.start_time} s')

    def ms(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{(self.end_time - self.start_time)*1000.} ms')

    def min(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{(self.end_time - self.start_time)/60.} min')

    def mins(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')

    def h(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{(self.end_time - self.start_time)/3600.} h')

    def hms(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.perf_counter()
        print(f'{label}:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')

class processtime(Time):
    def __init__(self) -> None:
        '''
        '''
        self.start_time = time.process_time()

    def reset(self) -> None:
        '''
        '''
        self.start_time = time.process_time()

    def s(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{self.end_time - self.start_time} s')

    def ms(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{(self.end_time - self.start_time)*1000.} ms')

    def min(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{(self.end_time - self.start_time)/60.} min')

    def mins(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')

    def h(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{(self.end_time - self.start_time)/3600.} h')

    def hms(self, label='Time') -> None:
        '''
        '''
        self.end_time = time.process_time()
        print(f'{label}:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')

def fileout(path:str, mode:str, *content:Tuple[str]) -> None:
    '''
    '''
    with open(path, mode) as theF:
        for c in content:
            theF.write(f'{c},\t')
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

def listdir(path: str, full=False) -> Sequence[str]:
    '''
    '''
    paths = os.listdir(path)
    if full:
        return [f'{path}\\{p}' for p in paths]
    else:
        return [f'{p}' for p in paths]

def dirref(pattern:re.Pattern, path:str, full=True, in_os='windows') -> Sequence[str]:
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