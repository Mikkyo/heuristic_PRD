#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from models.Resource import Resource


class Node:
    """Class to represents number of core and memory for a task or container"""

    # --- Attributes
    # Private
    _id = None  # identifier of a node
    _max_resource = None
    _containers = None

    # --- Constructor
    def __init__(self, id_node, max_resource):
        self._id = id_node
        self._max_resource = max_resource
        self._containers = []

    # --- Methods
    # Method to get used resources
    def get_used_resources(self):
        vcores = 0
        memory = 0
        for i in range(0, len(self._containers)):
            vcores += self._containers[i].capacity.vcores
            memory += self._containers[i].capacity.memory
        return Resource(vcores, memory)

    # Method to get available resources
    def get_available_resources(self):
        resources_used = self.get_used_resources()
        return Resource(self._max_resource.vcores - resources_used.vcores, self._max_resource.memory - resources_used.memory)

    # Method to add a container
    def add_container(self, container):
        self._containers.append(container)

    # Method to remove a container
    def remove_container(self, container):
        # A container is preempter
        count = self._containers.count(container)
        if (count > 0):
            self._containers.remove(container)

    # --- Getters/Setters
    #
