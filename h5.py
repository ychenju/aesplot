# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py

class h5:
    
    def __init__(self, path:str, mode:str='r', **kwargs):
        '''
        '''
        self.path = path
        self.open(mode=mode, **kwargs)

    def open(self, mode:str='r'):
        '''
        '''
        self.h5 = h5py.File(self.path, mode=mode)
        self.operation = self.h5

    def close(self):
        '''
        '''
        del self.h5

    def __getitem__(self, key:str):
        '''
        '''
        if not key in self.h5.keys():
            self.operation.create_group(key)
        return h5_group(self.h5, self, key)

    def add(self, key:str, data, **kwargs):
        '''
        '''
        self.operation.create_dataset(key, data=data, **kwargs)

    def __call__(self, key:str):
        '''
        '''
        return self.operation[key][:]

    def keys(self):
        return self.operation.keys()


class h5_group(h5):

    def __init__(self, ancestor:h5py.File, parent:h5, key:str):
        '''
        '''
        self.h5 = ancestor
        self.operation = parent.operation[key]