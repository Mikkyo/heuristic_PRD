#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area

class Application:
    """Class to represent a container"""

    # --- Attributes
    # Private
    _dag = None
    _containers = None
    _terminated = None
    _algorithme = None
    _resource_manager = None

    # Constants
    APP_ALGO_NAIVE = 1
    APP_ALGO_SMART = 2

    SEUIL_COMPAT = 0.2
    RES_MAX_WAIT_TIME = 99999999
    RES_MAX_UNUSED_TIME = 10

    # --- Constructor
    def __init__(self, dag, algo):
        self._dag = dag
        self._dag.init()

        self._containers = []
        self._terminated = False

        self._algorithme = algo

    # --- Methods
    # Method to get the used resources
    def get_used_resources(self):
        resource = new Resource()
        for i in range(0, len(self._containers)):
            resource.add(self._containers[i].capacity)
        return resource

    # Method to add a container
    def add_container(self, reservation, simulation_date):
        container = reservation.container
        tasks = reservation.tasks

        #Begin tasks
        for i in range(0, len(tasks)):
            container.add_task(tasks[i], simulation_date)

        self._containers.append(container)

    # Method to remove a container
    def remove_container(self, container):
        #A container is preempted
        index = self._containers.index(container)
        if index > -1:
            self._containers.splice(index, 1)

    # Method to update a task
    def update_task(self, simulation_date):
        if self._terminated :
            return

        self._dag.updateTasks(simulation_date)
        self._terminated = self._dag.are_all_tasks_finished()

    # Method to update an application
    def update(self, simulation_date):
        if self._terminated :
            return
        self._dag.update(simulation_date)

        #Making reservation
        ready_tasks = self._dag.get_ready_tasks()
        for i in range(0, len(ready_tasks)):
            ready_task = ready_tasks[i]
            reservation = Reservation(ready_task.resource, ready_task.criticality, [read_task])
            ready_task.status = TASK_SCHEDULED
            self.rm.reserve(self, reservation)

    # --- Getters/Setters




