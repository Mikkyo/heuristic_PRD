#!/usr/bin/python
# -*- coding: utf-8 -*-

#--- Import Area

class Resource:
    """Class to represents number of core and memory for a task or container"""

    #--- Attributes
    # Private
    _vcores = None #Number of cores
    _memory = None #Number of memory needed

    #--- Constructor
    def __init__(self, vcores, memory):
        """
        Constructor
        :param vcores: Integer
        :param memory: Integer
        """
        self._vcores = vcores
        self._memory = memory

    #--- Getters/Setters
    # Vcores
    @property
    def vcores(self):
        return self._vcores
    
    @vcores.setter
    def vcores(self, value):
        self._vcores = value
    
    @vcores.deleter
    def vcores(self):
        self._vcores = None

    # Memory
    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @memory.deleter
    def memory(self):
        self._memory = None

