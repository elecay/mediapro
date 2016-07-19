# -*- coding: utf-8 -*-
import time

from errors import MediaProError


def validate_task(task):
    """
    * start (required) is a timestamp and must be a future datetime
    * title (optional) is a string
    * worker (required) is a string of the name of the worker which runs the
    task
    * status (required) is a string and must be "SCHEDULED" or "RUNNING" or
    "SUCCEEDED" or "FAILED"
    * payload (optional) is a dictionary which stores application layer data
    :param task: the task to validate
    :return:
    """
    fields = ['start', 'worker', 'status', 'payload', 'title']
    for field in fields:
        valid_field(task, field)


def valid_field(task, field):
    if 'start' is field:
        valid_start(task)
    elif 'worker' == field:
        valid_worker(task)
    elif 'status' == field:
        valid_status(task)
    elif 'payload' == field:
        valid_payload(task)
    elif 'title' == field:
        valid_title(task)


def valid_start(task):
    if 'start' in task:
        if not isinstance(task['start'], int):
            raise MediaProError(MediaProError.START_TIMESTAMP)
        now = time.time() * 1000  # milliseconds since epoch
        if now > float(task['start']):
            raise MediaProError(MediaProError.START_FUTURE)
    else:
        raise MediaProError(MediaProError.START_MANDATORY)


def valid_worker(task):
    if 'worker' not in task:
        raise MediaProError(MediaProError.WORKER_MANDATORY)
    else:
        if not isinstance(task['worker'], str):
            raise MediaProError(MediaProError.WORKER_STRING)


def valid_title(task):
    if 'title' in task:
        if not isinstance(task['title'], str):
            raise MediaProError(MediaProError.TITLE_STRING)


def valid_status(task):
    _valid_status = ["SCHEDULED", "RUNNING", "SUCCEEDED", "FAILED"]
    if 'status' in task:
        if not isinstance(task['status'], str):
            raise MediaProError(MediaProError.STATUS_STRING)
        if task['status'] not in _valid_status:
            raise MediaProError(MediaProError.STATUS_VALID, _valid_status)
    else:
        raise MediaProError(MediaProError.STATUS_MANDATORY)


def valid_payload(task):
    if 'payload' in task:
        if not isinstance(task['payload'], dict):
            raise MediaProError(MediaProError.PAYLOAD_DICT)
