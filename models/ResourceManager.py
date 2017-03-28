#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from models.Resource import Resource
from models.Container import Container

class ResourceManager:
    """Class to represents number of core and memory for a task or container"""

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
    # Method to add applications
    def add_application(self, application):
        self._applications.append(application)
        application.id = self._next_application_id + 1
        application.resource_manager = self
        self._containers_per_app[application.id] = []
        self._reservations_per_app[application.id] = []

    # Method to make a reservation
    def reserve(self, application, reservation):
        self._reservations_per_app[application.id] = reservation

    # Method to sort containers
    def sort_containers(self):
        #TODO - Check this
        for i in range(0, len(self._containers_per_app)):
            self._containers_per_app[i].sort('sortByPriorityDesc')

    # Method to help preempting a container
    def preempt_containers(self, simulation_date):
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

    # Method to fulfil the reservation
    def fulfil_reservation(self, simulation_date):
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
    #
