#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area

class Container:
    """Class to represent a container"""

    # --- Attributes
    # Private
    _capacity = None  # Resource Object
    _node = None  # Node Object
    _application = None # App Object

    _base_priority = None # natural priority
    _priority = None # real priority

    _tasks = None
    _last_used = None

    # --- Constructor
    def __init__(self, resource, node, app, base_priority):
        """
        Constructor
        :param resource: Resource Object
        :param node: Node Object
        :param app: Application Object
        :param base_priority: Integer
        """
        self._capacity = resource
        self._node = node
        self._application = app
        self._base_priority = base_priority
        self._priority = base_priority
        self._tasks = []
        self._last_used = 0

    # --- Methods
    def add_task(self, task, simulation_date):
        """
        Method to add task to a container
        :param task: Task Object
        :param simulation_date: Integer
        """
        self._tasks.append(task)
        task.start()
        self.update(simulation_date)

    def remove_task(self, task, simulation_date):
        """
        Method to remove a task
        :param task: Task Object
        :param simulation_date: Integer
        """
        count = self._tasks.count(task)
        if count > 0 :
            self._tasks.remove(simulation_date)
            self.update(simulation_date)

    def preempt(self, simulation_date):
        """
        Method to preempt a container
        :param simulation_date: Integer
        :return:
        """
        for i in range(0, len(self._tasks)):
            self._tasks[i].preempt()
            self.remove_task(self._tasks[i], simulation_date)
        self._application.remove_container(self)
        self._node.remove_container(self)

    def update(self, simulation_date):
        """
        Method to update the container
        :param simulation_date: Integer
        """
        # P37 of the Nicolas Gougeon PRD, written in a different way
        A = 0.0
        for i in range(0, len(self._tasks)):
            A = max(A, pow(min(self._tasks[i].progress, 1.0), 1/4))
        self._priority = A * self._base_priority

        if len(self._tasks) > 0:
            self._last_used = simulation_date


    # --- Getters/Setters
    #



