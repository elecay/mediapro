# -*- coding: utf-8 -*-
from core.repository import FullAccessRepository
import configuration


class TaskRepository(FullAccessRepository):
    """
    Provides a full repository for Tasks.
    """
    def __init__(self):
        FullAccessRepository.__init__(self, configuration.MONGO_DB,
                                      configuration.COLLECTION_TASKS)
