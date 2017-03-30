#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Import Area
from enum import Enum

class TaskStatus(Enum):
    """Class to represent all status of a task"""

    # --- Attributes
    UNKNOWN = 0
    PENDING = 1
    READY = 2
    SCHEDULED = 3
    RUNNING = 4
    FINISHED = 5
