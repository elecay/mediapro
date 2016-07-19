# -*- coding: utf-8 -*-
"""
Utils methods.
"""
import logging
from errors import MediaProError

LOGGER = logging.getLogger()
DEFAULT_ROWS = 50


def pagination_builder(request):
    """
    Creates pagination dict with 'page' and 'rows' values. The first page is 1.
    By default 'page' is 1 and 'rows' is 50.
    :param request: the HTTP request
    :return: a dict with 'page' and 'rows' attributes.
    """
    response = dict()
    try:
        page = int(request.get_argument('page', default=1, strip=False))
        page = page if page >= 0 else 1
        response['skip'] = (page-1) * DEFAULT_ROWS
    except Exception:
        raise MediaProError(MediaProError.INVALID_PAGE)

    try:
        rows = int(request.get_argument('rows', default=DEFAULT_ROWS, strip=False))
        rows = rows if rows >= 0 else DEFAULT_ROWS
        response['limit'] = rows
    except Exception:
        raise MediaProError(MediaProError.INVALID_ROWS)

    return response
