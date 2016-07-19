# -*- coding: utf-8 -*-
"""
Some unit testing.
"""
import unittest
import validators
from errors import MediaProError


class ValidatorTest(unittest.TestCase):

    def test_fail_start_not_found(self):
        task = {
            'worker': 'a worker',
            'status': 'RUNNING'
        }
        try:
            validators.validate_task(task)
            self.assertFalse(True, 'This task is not valid.')
        except MediaProError as error:
            self.assertEquals(error, MediaProError.START_MANDATORY[0])
        except Exception:
            self.assertFalse(True, 'Wrong Exception.')

    def test_fail_start_past(self):
        task = {
            'worker': 'a worker',
            'status': 'RUNNING',
            'start': 0
        }
        try:
            validators.validate_task(task)
            self.assertFalse(True, 'This task is not valid.')
        except MediaProError as error:
            self.assertEquals(error, MediaProError.START_FUTURE[0])
        except Exception:
            self.assertFalse(True, 'Wrong Exception.')

    def test_fail_start_format(self):
        task = {
            'worker': 'a worker',
            'status': 'RUNNING',
            'start': '123123123123'
        }
        try:
            validators.validate_task(task)
            self.assertFalse(True, 'This task is not valid.')
        except MediaProError as error:
            self.assertEquals(error, MediaProError.START_TIMESTAMP[0])
        except Exception:
            self.assertFalse(True, 'Wrong Exception.')

    def test_success_start_future(self):
        task = {
            'worker': 'a worker',
            'status': 'RUNNING',
            'start': 1568952820 * 1000
        }
        try:
            validators.validate_task(task)
        except MediaProError as error:
            self.assertFalse(True, 'Wrong Exception.')
        except Exception:
            self.assertFalse(True, 'Wrong Exception.')

if __name__ == "__main__":
    unittest.main()
