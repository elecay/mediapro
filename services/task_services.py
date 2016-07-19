# -*- coding: utf-8 -*-
from repositories import TaskRepository
from translators.task_translators import TaskTranslator
import validators
import utils


class TaskServices:
    def __init__(self):
        self.repository = TaskRepository()

    def find(self, request):
        pagination = utils.pagination_builder(request)
        _filter = self.filter_builder(request)
        return self.repository.find(_filter, skip=pagination['skip'],
                                    limit=pagination['limit'])

    def find_by_id(self, _id):
        return self.repository.find_one(_id)

    def insert(self, task):
        new_task = dict()
        TaskTranslator.translate(task, new_task)
        validators.validate_task(new_task)
        return self.repository.insert(task)

    def delete_by_id(self, _id):
        return self.repository.delete_by_id(_id)

    def update_by_id(self, _id, task):
        task_update = self.task_patch_builder(_id, task)
        return self.repository.update_by_id(_id, task_update)

    def update_payload_by_task_id(self, _id, payload):
        to_update_task = self.repository.find_one(_id)
        if 'payload' not in to_update_task:
            to_update_task['payload'] = dict()
        for key in payload.keys():
            to_update_task['payload'][key] = payload[key]
        self.repository.update_by_id(_id,
                                     {'payload': to_update_task['payload']})
        return to_update_task

    def remove_payload_key_by_task_id(self, _id, key):
        to_update_task = self.repository.find_one(_id)
        if 'payload' in to_update_task:
            to_update_task['payload'].pop(key, None)
        self.repository.update_by_id(_id,
                                     {'payload': to_update_task['payload']})
        return to_update_task

    def task_patch_builder(self, _id, task):
        to_update_task = self.repository.find_one(_id)
        TaskTranslator.translate(task, to_update_task)
        validators.validate_task(to_update_task)
        return to_update_task

    @staticmethod
    def filter_builder(request):
        response = dict()
        # String filters
        string_filters = ['worker', 'status']
        for _filter in string_filters:
            filter_param = request.get_argument(_filter, default=None,
                                                strip=False)
            if filter_param is not None:
                response[_filter] = filter_param
        # Date filters
        date_filter = dict()
        from_date = request.get_argument('from', default=None, strip=False)
        if from_date is not None:
            date_filter['from'] = float(from_date)
        to_date = request.get_argument('to', default=None, strip=False)
        if to_date is not None:
            date_filter['to'] = float(to_date)
        if len(date_filter) > 0:
            response['start'] = date_filter
        return response
