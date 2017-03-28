#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from models.ResourceManager import ResourceManager
from models.Node import Node


class Simulator:
    """Class to represents number of core and memory for a task or container"""

    # --- Attributes
    # Private
    _nodes = None  # Number of nodes
    _resource_manager = None  # Resource Manager Object
    _application_request = None # All Application requests
    _applications = None # Array of application
    _simulation_date = None # Date of Simulation

    # --- Constructor
    def __init__(self, number_node, resource_per_node, application_requests):
        self._nodes = []
        for i in range(0, number_node):
            self._nodes[i] = Node(i, resource_per_node)

        self._resource_manager = ResourceManager(self._nodes, resource_per_node)
        self._application_request = application_requests
        self._applications = []
        self._simulation_date = None

    # --- Getters/Setters
    #

    # --- Methods
    # Debugging Method
    def tmp_pct(self, task):
        app = None
        for i in range(0, len(self._applications)):
            if self._applications[i].dag.tasks.indexOf(task) > -1:
                app = self._applications[i]
                break
        if app is None:
            return
        container = task.container
        containers = self._resource_manager.containers_per_app[app.id]
        index = containers.indexOf(container)
        if index > -1:
            containers.splice(index, 1)
            container.preempt(self._simulation_date)

    # Steps Method
    def steps(self,number_iteration):
        for i in range(0, number_iteration):
            self.step()

    # Step Method
    def step(self):
        # 1 - Increment Simulation Date
        if self._simulation_date is None:
            self._simulation_date = 0
        else:
            self._simulation_date += 1

        # 2 - Check Task Termination
        for i in range(0, len(self._applications)):
            self._applications[i].updateTasks(self._simulation_date)

        # 3 - Add applications requested by users
        for i in range(0, len(self._application_request)):
            curr_request = self._application_request[i]
            if curr_request.request_date == self._simulation_date:
                # Try to start an app
                self._resource_manager.add_application(curr_request.application)
                self._applications.append(curr_request.application)

        # 4 - Preempt resources routine (Fair-Share)
        self._resource_manager.preempt_containers(self._simulation_date)

        # 5 - Updating applications states & Making reservations
        for i in range(0, len(self._applications)):
            self._applications[i].update(self._simulation_date)

        # 6 - Attempt to fulfill an app's reservation
        self._resource_manager.fulfil_reservation(self._simulation_date)
