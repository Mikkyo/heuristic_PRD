#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from enums.TaskStatus import TaskStatus

class TaskDAG:
    """Class to represent a DAG [Direct Acyclic Graph] for a Task"""

    # --- Attributes
    # Private
    _tasks = None # All the tasks

    # Constants


    # --- Constructor
    def __init__(self, tasks):
        """"
        TaskDAG Constructor
        :param: tasks: Task Array
        """
        self._tasks = tasks

    # --- Methods
    def get_root_tasks(self):
        """
        Method to get the root tasks
        :return: Task Array
        """
        root_task = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_root():
                root_task.append(self._tasks[i])
        return root_task

    def get_leaf_tasks(self):
        """
        Method to get the leaf tasks
        :return Task Array
        """
        leaf_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_ready():
                leaf_tasks.append(self._tasks[i])
        return leaf_tasks

    def get_ready_tasks(self):
        """
        Method to get all the ready tasks
        :return Task Array
        """
        ready_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_ready():
                ready_tasks.append(self._tasks[i])
        return ready_tasks

    def get_current_tasks(self):
        """
        Method to get the current tasks
        :return Task Array
        """
        current_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_current_root():
                current_tasks.append(self._tasks[i])
        return current_tasks

    def are_all_tasks_finished(self):
        """
        Method to check if all tasks are finished
        :return Bool
        """
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_finished() is False:
                return False
        return True

    def init(self):
        """
        Method to init all tasks
        """
        for i in range(0, len(self._tasks)):
            self._tasks[i].status = TaskStatus.PENDING

        root_tasks = self.get_root_tasks()
        for i in range(0, len(root_tasks)):
            self._tasks[i].status = TaskStatus.READY

    def update_tasks(self, simulation_date):
        """
        Method to update tasks
        :param simulation_date: Integer
        """
        for i in range(0, len(self._tasks)):
            self._tasks[i].update(simulation_date)

    def update(self, simulation_date):
        """
        Method to update all tasks
        :param simulation_date: Integer
        """
        #Reset all start date
        for i in range(0, len(self._tasks)):
            self._tasks[i].reset_start_dates()

        # Top-Down Update Min Start Dates
        curr_tasks = self.get_current_tasks()
        for i in range(0, len(curr_tasks)):
            if curr_tasks[i].is_running() is False:
                curr_tasks[i].set_min_start_date(simulation_date)

        # Compute overall max end Date
        max_end_date = 0
        leaf_tasks = self.get_leaf_tasks()
        for i in range(0, len(leaf_tasks)):
            leaf_task = leaf_tasks[i]
            max_end_date = max(leaf_task.min_start_date + leaf_task.duration, max_end_date)

        # Bottom-Up Update max start date
        for i in range(0, len(leaf_tasks)):
            leaf_task = leaf_tasks[i]
            leaf_task.set_max_start_date(max_end_date - leaf_task.duration)

        # Update the criticality of tasks
        for i in range(0, len(self._tasks)):
            self._tasks[i].computer_criticality()


    # --- Getters/Setters




