#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area

class Container:
    """Class to represent a container"""

    # --- Attributes
    # Private
    _capacity = None  # Resource Object
    _node = None  # Node Object
    _app = None # App Object

    _base_priority = None # natural priority
    _priority = None # real priority

    _tasks = None
    _last_used = None

    # --- Constructor
    def __init__(self, capacity, node, app, base_priority):
        self._capacity = capacity
        self._node = node
        self._app = app
        self._base_priority = base_priority
        self._priority = base_priority
        self._tasks = []
        self._last_used = 0


    # --- Getters/Setters
    # Vcores
    @property
    def vcores(self):
        return self._v_cores

    @vcores.setter
    def vcores(self, value):
        self._vcores = value

    @vcores.deleter
    def vcores(self):
        self._vcores = None



