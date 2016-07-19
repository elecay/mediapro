# -*- coding: utf-8 -*-
"""
Custom errors factory.
"""


class MediaProError(Exception):

    GENERIC = ('An unexpected error has occurred.', 500, 0)
    START_FUTURE = ('"start" should be a future datetime.', 400, 1)
    START_MANDATORY = ('"start" is a mandatory field.', 400, 2)
    STATUS_VALID = (
        '"status" should be one of this: {0}, {1}, {2} or {3}.', 400, 3)
    STATUS_MANDATORY = ('"status" is a mandatory field.', 400, 4)
    WORKER_MANDATORY = ('"worker" is a mandatory field.', 400, 5)
    INVALID_ID = ('Invalid id format.', 400, 6)
    TITLE_STRING = ('"title" should be a string.', 400, 7)
    PAYLOAD_DICT = ('"payload" should be a dictionary.', 400, 8)
    START_TIMESTAMP = ('"start" should be a timestamp.', 400, 9)
    WORKER_STRING = ('"worker" should be a string.', 400, 10)
    STATUS_STRING = ('"status" should be a string.', 400, 11)
    INVALID_PAGE = ('Invalid "page" parameter.', 400, 12)
    INVALID_ROWS = ('Invalid "rows" parameter.', 400, 13)

    def __init__(self, error, params=()):
        self.message = error[0].format(*params)
        self.http_code = error[1]
        self.internal_code = error[2]
        super(Exception, self).__init__(self.message)
