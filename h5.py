# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py

class h5:
    
    def __init__(self, path:str, mode:str='r', **kwargs):
        '''
        Create an HDF5 file pointer and open the file
        '''
        self.path = path
        self.open(mode=mode, **kwargs)

    def open(self, mode:str='r'):
        '''
        Open an HDF5 file, the mode can be:
        - 'r': Read only
        - 'r+': Read & write (The target should exist)
        - 'w': Create and write, truncate if exists
        - 'x': Create and write, fail if exists
        - 'a': Read & write if exists, truncate overwise
        '''
        self.h5 = h5py.File(self.path, mode=mode)
        self.operation = self.h5

    def close(self):
        '''
        Close the file opened
        '''
        del self.h5

    def __getitem__(self, key:str):
        '''
        Return a group (h5_group object), create if not exist
        '''
        if not key in self.h5.keys():
            self.operation.create_group(key)
        return h5_group(self.h5, self, key)

    def add(self, key:str, data, **kwargs):
        '''
        Add a dataset to the current operating layer
        '''
        self.operation.create_dataset(key, data=data, **kwargs)

    def addlzf(self, key:str, data, **kwargs):
        '''
        Add a dataset to the current operating layer, with lzf compression
        '''
        self.operation.create_dataset(key, data=data, compression='lzf', **kwargs)

    def addgz(self, key:str, data, opts:int=6, **kwargs):
        '''
        Add a dataset to the current operating layer, with gzip compression
        '''
        self.operation.create_dataset(key, data=data, compression='gzip', compression_opts=opts, **kwargs)

    def __call__(self, key:str):
        '''
        Read a dataset to numpy at the current operating layer
        '''
        return self.operation[key][:]

    def keys(self):
        return self.operation.keys()


class h5_group(h5):

    def __init__(self, ancestor:h5py.File, parent:h5, key:str):
        '''
        Create a new group (or operating layer)
        '''
        self.h5 = ancestor
        self.operation = parent.operation[key]