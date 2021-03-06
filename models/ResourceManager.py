#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from models.Resource import Resource
from models.Container import Container

class ResourceManager:
    """Class to represent the ResourceManager"""

    # --- Attributes
    # Private
    _nodes = None  # Number of nodes
    _total_resources = None # Number of nodes
    _applications = None # It's jobs in a Fair-Share queue
    _next_application_id = None # Id of the next application
    _containers_per_app = None # Array of all containers in an application
    _reservations_per_app = None # Array of reservations per application

    # --- Constructor
    def __init__(self, nodes, resource_per_node):
        """
        Constructor
        :param nodes: Node Array
        :param resource_per_node: Resource Object
        """
        self._nodes = nodes
        temp_nodes_len = len(self._nodes)
        temp_vcores = resource_per_node.vcores
        temp_memory = resource_per_node.memory
        self._total_resources = Resource(temp_vcores * temp_nodes_len,  temp_memory * temp_nodes_len)
        self._applications = []
        self._next_application_id = 0
        self._containers_per_app = []
        self._reservations_per_app = []

    # --- Methods
    def add_application(self, application):
        """
        Method to add applications
        :param application: Application Object
        """
        self._applications.append(application)
        application.id = self._next_application_id + 1
        application.resource_manager = self
        self._containers_per_app[application.id] = []
        self._reservations_per_app[application.id] = []

    def reserve(self, application, reservation):
        """
        Method to make a reservation
        :param application: Application Object
        :param reservation: Resource Object
        """
        self._reservations_per_app[application.id] = reservation

    def sort_containers(self):
        """
        Method to sort containers
        """
        for i in range(0, len(self._containers_per_app)):
            self._containers_per_app[i].sort('sortByPriorityDesc')

    def preempt_containers(self, simulation_date):
        """
        Method to help preempting a container
        :param simulation_date: Integer
        """
        number_application = len(self._applications)
        reservations_per_app = Resource(self._total_resources.vcores / number_application, self._total_resources.memory/ number_application)

        # Sort the containers
        self.sort_containers()

        # Preempt overflowing containers
        for i in range(0, len(self._applications)):
            application = self._applications[i]
            containers = self._containers_per_app[i]

            while application.get_used_resources() >= reservations_per_app:
                containers.preempt(simulation_date) # We preempt the lowest priority resource

    def fulfil_reservation(self, simulation_date):
        """
        Method to fulfil the reservation
        :param simulation_date: Integer
        """
        for i in range(0, len(self._applications)):
            application = self._applications[i]
            reservations = self._reservations_per_app[application.id]
            len_reservation_queue = len(reservations)
            for j in range(0, len_reservation_queue):
                reservation = reservations[j]
                # Looking for an available node
                for k in range(0, len(self._nodes)):
                    if self._nodes[k].get_available_resources() > reservation.resource:
                        node = self._nodes[k]
                        container = Container(reservation.resource, node, application, reservation.priority)
                        self._containers_per_app[application.id] = container
                        node.add_container(container)

                        reservation.container = container
                        application.add_container(container, simulation_date)

                        reservations.splice(j, 1) # Reservation is fulfilled, we remove it
                        j -= 1
                        len_reservation_queue -= 1
                        break


    # --- Getters/Setters
    # containers_per_app
    @property
    def containers_per_app(self):
        return self._containers_per_app

    @containers_per_app.setter
    def containers_per_app(self, value):
        self._containers_per_app = value
