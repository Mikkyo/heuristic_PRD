#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area

class Reservation:
    """Class to store all reservations"""

    # --- Attributes
    # Private
    _resource = None  # Resource Object
    _priority = None  # Priority Reservation
    _tasks = None # Array of Tasks
    _container = None # Reservation is made in a container

    # --- Constructor
    def __init__(self, resource, priority, tasks):
        """
        Constructor
        :param resource: Resource Object
        :param priority: Double
        :param tasks: Task[]
        """
        self._resource = resource
        self._priority = priority
        self._tasks = tasks
        self.container = None

    # --- Getters/Setters


