#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from enums.TaskStatus import TaskStatus

class TaskDAG:
    """Class to represent a container"""

    # --- Attributes
    # Private
    _tasks = None # All the tasks

    # Constants


    # --- Constructor
    def __init__(self, tasks):
        self._tasks = tasks

    # --- Methods
    # Method to get the root tasks
    def get_root_tasks(self):
        root_task = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_root():
                root_task.append(self._tasks[i])
        return root_task

    # Method to get the leaf tasks
    def get_leaf_tasks(self):
        leaf_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_ready():
                leaf_tasks.append(self._tasks[i])
        return leaf_tasks

    # Method to get all the ready tasks
    def get_ready_tasks(self):
        ready_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_ready():
                ready_tasks.append(self._tasks[i])
        return ready_tasks

    # Method to get the current tasks
    def get_current_tasks(self):
        current_tasks = []
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_current_root():
                current_tasks.append(self._tasks[i])
        return current_tasks

    # Method to check if all tasks are finished
    def are_all_tasks_finished(self):
        for i in range(0, len(self._tasks)):
            if self._tasks[i].is_finished() is False:
                return False
        return True

    # Method to init all tasks
    def init(self):
        for i in range(0, len(self._tasks)):
            self._tasks[i].status = TaskStatus.PENDING

        root_tasks = self.get_root_tasks()
        for i in range(0, len(root_tasks)):
            self._tasks[i].status = TaskStatus.READY

    # Method to update tasks
    def update_tasks(self, simulation_date):
        for i in range(0, len(self._tasks)):
            self._tasks[i].update(simulation_date)

    # Method to update all tasks
    def update(self, simulation_date):
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




