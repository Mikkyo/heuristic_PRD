#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from models.Resource import Resource


class Node:
    """Represent a node on the cluster and will be shared between different containers"""

    # --- Attributes
    # Private
    _id = None  # identifier of a node
    _max_resource = None
    _containers = None

    # --- Constructor
    def __init__(self, id_node, max_resource):
        """
        Constructor
        :param id_node: Integer
        :param max_resource: Resource Object
        """
        self._id = id_node
        self._max_resource = max_resource
        self._containers = []

    # --- Methods
    def get_used_resources(self):
        """
        Method to get used resources
        :return Resource Object
        """
        vcores = 0
        memory = 0
        for i in range(0, len(self._containers)):
            vcores += self._containers[i].capacity.vcores
            memory += self._containers[i].capacity.memory
        return Resource(vcores, memory)

    def get_available_resources(self):
        """
        Method to get available resources
        :return Resource Object
        """
        resources_used = self.get_used_resources()
        return Resource(self._max_resource.vcores - resources_used.vcores, self._max_resource.memory - resources_used.memory)

    def add_container(self, container):
        """
        Method to add a container
        :param container: Container Object
        """
        self._containers.append(container)

    def remove_container(self, container):
        """
        Method to remove a container
        :param container: Container Object
        """
        # A container is preempter
        count = self._containers.count(container)
        if (count > 0):
            self._containers.remove(container)

    # --- Getters/Setters
    #
