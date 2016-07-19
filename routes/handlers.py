# -*- coding: utf-8 -*-
import tornado.web

from errors import MediaProError
from utils import LOGGER
from core.repository import JSONEncoder, JSONDecoder


class TasksHandler(tornado.web.RequestHandler):
    """
    Handler for Tasks HTTP Requests.
    """
    def initialize(self, service):
        self.service = service

    def get(self):
        """
        Returns all tasks using pagination and filtering.
        Example of usage:
            /api/tasks?to=1469930541448&status=SCHEDULED&worker=task_worker_001
        Valid filter params are:
            page: int
            rows: int
            worker: str
            status: str
            from: int (timestamp)
            to: int (timestamp)
        :return: all tasks using pagination.
        """
        try:
            response = [doc for doc in self.service.find(self)]
            respond_success(self, response)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)

    def post(self):
        """
        Creates a new Task.
        :return:  the Task created.
        """
        try:
            task = JSONDecoder().decode(self.request.body)
            task_id = self.service.insert(task).inserted_id
            task['_id'] = task_id
            respond_success(self, task)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)


class TaskHandler(tornado.web.RequestHandler):
    """
    Handler for single Task HTTP Requests.
    """
    def initialize(self, service):
        self.service = service

    def get(self, _id):
        """
        Return a single Task given an id.
        :param _id: the id of the Task to return.
        :return: a Task
        """
        try:
            response = self.service.find_by_id(_id)
            respond_success(self, response, 200)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)

    def patch(self, _id):
        """
        Updates a Task given one or more fields.
        :param _id: the id of the Taks to update.
        :return: the Task updated.
        """
        try:
            task = JSONDecoder().decode(self.request.body)
            self.service.update_by_id(_id, task)
            respond_success(self, task)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)

    def delete(self, _id):
        """
        Deletes a Task.
        :param _id: the id of the Task to delete.
        :return: a message if the deletion was successfully or not.
        """
        try:
            result = self.service.delete_by_id(_id)
            response = {
                'message': "The task with id: {0} has been deleted.".format(
                    _id)
            }
            if result.deleted_count == 0:
                response['message'] = "No task has been deleted. This could "\
                                      "due there is no task with such id or "\
                                      "the task has a RUNNING status."
            respond_success(self, response, 200)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)


class TaskPayloadHandler(tornado.web.RequestHandler):
    """
    Handler for Tasks Payloads HTTP Requests.
    """
    def initialize(self, service):
        self.service = service

    def post(self, _id):
        """
        Adds or replace payload first level key, and returns the modified task
        :param _id: the id of the Task to update its payload.
        :return: the modified Task
        """
        try:
            payload = JSONDecoder().decode(self.request.body)
            task = self.service.update_payload_by_task_id(_id, payload)
            respond_success(self, task)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)

    def delete(self, _id, key):
        """
        Deletes a certain first level key from the payload if it exists.
        :param _id: the id of the Task to delete its payload
        :param key: the key to delete
        :return: the modified Task
        """
        try:
            task = self.service.remove_payload_key_by_task_id(_id, key)
            respond_success(self, task)
        except MediaProError as error:
            respond_error(self, error)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            error = MediaProError(MediaProError.GENERIC)
            respond_error(self, error)


def respond_success(response, data, code=200):
    response.set_status(code)
    response.write(JSONEncoder().encode({
        'data': data,
        'error': None
    }))
    response.finish()


def respond_error(response, error):
    response.set_status(error.http_code)
    response.write(JSONEncoder().encode({
        'data': None,
        'error': {
            'message': error.message,
            'code': error.internal_code
        }
    }))
    response.finish()
