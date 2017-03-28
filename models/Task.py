#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from enums.TaskStatus import TaskStatus

class Task:
    """Class to represent a container"""

    # --- Attributes
    # Private
    _resource = None # The resource's task
    _duration = None # The task duration

    _parent_tasks = None # The parent task
    _child_tasks = None # The child task

    _min_start_date = None # The minimum start date
    _max_start_date = None # The maximum start date

    _start_date = None # The start date
    _progress = None # Progess of task
    _criticality = None # Criticality of task

    _container = None # The container task
    _status = None # Task Status

    # Constants
    # Criticity Score Constants
    CRIT_KD = 0.2 # weight for the duration crit
    CRIT_D_MAX = 6 # Max duration before duration crit stops
    CRIT_KR = 0.8 # weight for the delay crit
    CRIT_R_MAX = 40 # Max delay before delay crit stops

    # --- Constructor
    def __init__(self, resource, duration, parent_tasks, child_tasks):
        self._resource = resource
        self._duration = duration

        self._parent_tasks = parent_tasks
        self._child_tasks = child_tasks

        self._min_start_date = -1
        self._max_start_date = 0.0
        self._criticality = 0.0

        self._container = None
        self._status = TaskStatus.UNKNOWN

    # --- Methods
    # Method to check if a task is a root
    def is_root(self):
        if len(self._parent_tasks) > 0:
            return True
        return False

    # Method to check if a task is a leaf
    def is_leaf(self):
        if len(self._child_tasks) > 0:
            return True
        return False

    # Method to check if a task is ready to be scheduled
    def is_ready(self):
        if self._status is TaskStatus.READY:
            return True
        return False

    # Method to check if a task is running
    def is_running(self):
        if self._status is TaskStatus.RUNNING:
            return True
        return False

    # Method to check if a task is finished
    def is_finished(self):
        if self._status is TaskStatus.FINISHED:
            return True
        return False

    # Method to check if a task is the current root
    def is_current_root(self):
        if (self._status < TaskStatus.FINISHED) & (self._status > TaskStatus.PENDING):
            return True
        return False

    # Method to reset all start dates
    def reset_start_dates(self):
        self._min_start_date = 0
        self._max_start_date = 999999

    # Method to set the minimum starting date
    def set_min_start_date(self, date):
        if self.is_finished() : return
        self._min_start_date = max(self._min_start_date, date)
        for i in range(0, len(self._child_tasks)):
            self._child_tasks[i].set_min_start_date(self._min_start_date + self._duration)

    # Method to set the maximum starting date
    def set_max_start_date(self, date):
        if self.is_finished(): return
        self._max_start_date = min(self._max_start_date, date)
        for i in range(0, len(self._parent_tasks)):
            self._parent_tasks[i].set_max_start_date(self._max_start_date - self._duration)

    # Method to set the begining of a task
    def start(self, container, simulation_date):
        self._start_date = simulation_date
        self._container = container
        self._status = TaskStatus.RUNNING

    # Method to preempt a task
    def preempt(self):
        if self.is_running() :
            self._start_date = -1
            self._progress = 0.0
            self._criticality = 0.0
            self._container = None
            self._status = TaskStatus.READY

    # Method to finish a task
    def finish(self, simulation_date):
        self._criticality = 0.0
        self._container.remove_task(self, simulation_date)
        self._container = None
        self._status = TaskStatus.FINISHED
        for i in range(0, len(self._child_tasks)):
            self._child_tasks[i].status = TaskStatus.READY

    # Method to compute criticality
    def compute_criticality(self):
        if self.is_finished(): return
        # This calculation is based on Nicolas Gougeon heuristic
        criticality = self.CRIT_KD * min(self._duration/ self.CRIT_D_MAX, 1.0)
        criticality += self.CRIT_KR * max(1.0 - (self._max_start_date - self._min_start_date) / self.CRIT_R_MAX,0.0)

        self._criticality = criticality / (self.CRIT_KD + self.CRIT_KR) # To normalize the result

    # Methode to update the task
    def update(self, simulation_date):
        if self.is_running() :
            self._progress = (simulation_date - self._start_date) / self._duration
            self._container.update(simulation_date) #Update the container priority
            if (simulation_date - self._start_date) is self._duration:
                self.finish(simulation_date)

    # --- Getters/Setters




