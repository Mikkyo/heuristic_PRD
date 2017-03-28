#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area

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
        resource = new Resource()
        for i in range(0, len(self._containers)):
            resource.add(self._containers[i].capacity)
        return resource

    # Method to get available resources
    def get_available_resources(self):
        resource = new Ressource().copy(self._max_resource).sub(self.get_used_resources())
        return resource

    # Method to add a container
    def add_container(self, container):
        self._containers.append(container)

    # Method to remove a container
    def remove_container(self, container):
        # A container is preempter
        index = self._containers.index(container)
        if(index > -1):
            self._containers.splice(index, 1)

    # --- Getters/Setters
    #


