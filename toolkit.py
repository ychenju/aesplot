# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

class Time:
    start_time = 0
    end_time = 0

class perfcounter(Time):
    def __init__(self):
        self.start_time = time.perf_counter()

    def reset(self):
        self.start_time = time.perf_counter()

    def s(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{self.end_time - self.start_time} s')

    def ms(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)*1000.} ms')

    def min(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)/60.} min')

    def mins(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)//60} m \t{(self.end_time - self.start_time)%60} s')

    def h(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)/3600.} h')

    def hms(self):
        self.end_time = time.perf_counter()
        print(f'Time:\t{(self.end_time - self.start_time)//3600} h \t{(self.end_time - self.start_time)%3600//60} m \t{(self.end_time - self.start_time)%60} s')

def fileout(path, mode, *content):
    with open(path, mode) as theF:
        for c in content:
            theF.write(f'{c},\t')
        theF.write('\n')

def fold(table, length):
    r = []
    for i in range(len(table)//length):
        r.append([])
        for j in range(length):
            r[-1].append(table[i*length+j])
    return np.array(r)
