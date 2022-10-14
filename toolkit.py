# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import pandas as pd
from typing import Tuple, Sequence

class Time:
    start_time = 0
    end_time = 0

class perfcounter(Time):
    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def reset(self) -> None:
        self.start_time = time.perf_counter()

    def s(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{self.end_time - self.start_time} s')

    def ms(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)*1000.} ms')

    def min(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)/60.} min')

    def mins(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')

    def h(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)/3600.} h')

    def hms(self) -> None:
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')

def fileout(path:str, mode:str, *content:Tuple[str]) -> None:
    with open(path, mode) as theF:
        for c in content:
            theF.write(f'{c},\t')
        theF.write('\n')

def fold(table:Sequence, length:int) -> np.ndarray:
    r = []
    for i in range(len(table)//length):
        r.append([])
        for j in range(length):
            r[-1].append(table[i*length+j])
    return np.array(r)

def npfold(table:np.ndarray, length:int) -> np.ndarray:
    try:
        if not isinstance(table, np.ndarray):
            table = np.array(table)
        return np.array(table).reshape(-1, length)
    except:
        raise RuntimeError('Cannot \'npfold\'. Please try \'fold\' instead')

def tocsv(table:np.ndarray, path:str, **kwargs) -> pd.DataFrame:
    _df = pd.DataFrame(table)
    _df.to_csv(path, **kwargs)
    return _df