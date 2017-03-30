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
        """
        Constructor
        :param resource: Resource Object
        :param duration: Integer
        :param parent_tasks: Task Array
        :param child_tasks: Task Array
        """
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
    def is_root(self):
        """
        Method to check if a task is a root
        :return Bool
        """
        if len(self._parent_tasks) > 0:
            return True
        return False

    def is_leaf(self):
        """
        Method to check if a task is a leaf
        :return Bool
        """
        if len(self._child_tasks) > 0:
            return True
        return False

    def is_ready(self):
        """
        Method to check if a task is ready to be scheduled
        :return Bool
        """
        if self._status is TaskStatus.READY:
            return True
        return False

    def is_running(self):
        """
        Method to check if a task is running
        :return Bool
        """
        if self._status is TaskStatus.RUNNING:
            return True
        return False

    def is_finished(self):
        """
        Method to check if a task is finished
        :return Bool
        """
        if self._status is TaskStatus.FINISHED:
            return True
        return False

    def is_current_root(self):
        """
        Method to check if a task is the current root
        :return Bool
        """
        if (self._status < TaskStatus.FINISHED) & (self._status > TaskStatus.PENDING):
            return True
        return False

    def reset_start_dates(self):
        """
        Method to reset all start dates
        """
        self._min_start_date = 0
        self._max_start_date = 999999

    def set_min_start_date(self, date):
        """
        Method to set the minimum starting date
        :param date: Integer
        :return None if it's finished
        """
        if self.is_finished() : return
        self._min_start_date = max(self._min_start_date, date)
        for i in range(0, len(self._child_tasks)):
            self._child_tasks[i].set_min_start_date(self._min_start_date + self._duration)

    def set_max_start_date(self, date):
        """
        Method to set the maximum starting date
        :param date: Integer
        :return None if it's finished
        """
        if self.is_finished(): return
        self._max_start_date = min(self._max_start_date, date)
        for i in range(0, len(self._parent_tasks)):
            self._parent_tasks[i].set_max_start_date(self._max_start_date - self._duration)

    def start(self, container, simulation_date):
        """
        Method to set the begining of a task
        :param container: Container Object
        :param simulation_date: Integer
        """
        self._start_date = simulation_date
        self._container = container
        self._status = TaskStatus.RUNNING

    def preempt(self):
        """
        Method to preempt a task
        """
        if self.is_running() :
            self._start_date = -1
            self._progress = 0.0
            self._criticality = 0.0
            self._container = None
            self._status = TaskStatus.READY

    def finish(self, simulation_date):
        """
        Method to finish a task
        :param simulation_date: Integer
        """
        self._criticality = 0.0
        self._container.remove_task(self, simulation_date)
        self._container = None
        self._status = TaskStatus.FINISHED
        for i in range(0, len(self._child_tasks)):
            self._child_tasks[i].status = TaskStatus.READY

    def compute_criticality(self):
        """
        Method to compute criticality
        """
        if self.is_finished(): return
        # This calculation is based on Nicolas Gougeon heuristic
        criticality = self.CRIT_KD * min(self._duration/ self.CRIT_D_MAX, 1.0)
        criticality += self.CRIT_KR * max(1.0 - (self._max_start_date - self._min_start_date) / self.CRIT_R_MAX,0.0)

        self._criticality = criticality / (self.CRIT_KD + self.CRIT_KR) # To normalize the result

    def update(self, simulation_date):
        """
        Methode to update the task
        :param simulation_date: Integer
        """
        if self.is_running() :
            self._progress = (simulation_date - self._start_date) / self._duration
            self._container.update(simulation_date) #Update the container priority
            if (simulation_date - self._start_date) is self._duration:
                self.finish(simulation_date)

    # --- Getters/Setters




