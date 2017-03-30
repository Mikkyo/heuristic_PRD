#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from enums.TaskStatus import TaskStatus
from models.Reservation import Reservation
from models.Resource import Resource

class Application:
    """Class to represent Tasks submitted by user"""

    # --- Attributes
    # Private
    _dag = None
    _containers = None
    _terminated = None
    _algorithm = None
    _resource_manager = None

    # Constants
    APP_ALGO_NAIVE = 1
    APP_ALGO_SMART = 2

    SEUIL_COMPAT = 0.2
    RES_MAX_WAIT_TIME = 99999999
    RES_MAX_UNUSED_TIME = 10

    # --- Constructor
    def __init__(self, dag, algo):
        """
        Constructor of Application
        :param dag: Take a TaskDag Object
        :param algo: Which algo to implement
        """
        self._dag = dag
        self._dag.init()

        self._containers = []
        self._terminated = False

        self._algorithm = algo | self.APP_ALGO_SMART

    # --- Methods
    def get_used_resources(self):
        """
        Method to get the used resources
        :return Resource type Object
        """
        vcores = 0
        memory = 0
        for i in range(0, len(self._containers)):
            vcores += self._containers[i].vcores
            memory += self._containers[i].memory
        return Resource(vcores, memory)

    def add_container(self, reservation, simulation_date):
        """
        Method to add a container
        :param reservation: Allocated resources
        :param simulation_date: Integer
        :return Add in a container
        """
        container = reservation.container
        tasks = reservation.tasks

        #Begin tasks
        for i in range(0, len(tasks)):
            container.add_task(tasks[i], simulation_date)

        self._containers.append(container)

    def remove_container(self, container):
        """
        Method to remove a container
        :param container: The container to remove (preempted)
        """
        #A container is preempted
        count = self._containers.count(container)
        if count > 0:
            self._containers.remove(container)

    def update_task(self, simulation_date):
        """
        Method to update a task
        :param simulation_date: Integer
        :return None if application is finished
        """
        if self._terminated :
            return

        self._dag.updateTasks(simulation_date)
        self._terminated = self._dag.are_all_tasks_finished()

    def update(self, simulation_date):
        """
        Method to update an application
        :param simulation_date: Integer
        :return None if application is finished
        """
        if self._terminated :
            return
        self._dag.update(simulation_date)

        #Making reservation
        ready_tasks = self._dag.get_ready_tasks()
        for i in range(0, len(ready_tasks)):
            ready_task = ready_tasks[i]
            reservation = Reservation(ready_task.resource, ready_task.criticality, ready_task)
            ready_task.status = TaskStatus.SCHEDULED
            self._resource_manager.reserve(self, reservation)

    # --- Getters/Setters




