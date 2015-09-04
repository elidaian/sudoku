__author__ = 'Eli Daian <elidaian@gmail.com>'

import itertools


def enum(*sequential, **named):
    """
    Create an enumeration.
    :param sequential: The sequential arguments.
    :type sequential: list
    :param named: The named arguments.
    :type named: dict
    :return: Enum
    """
    sequential_dict = itertools.izip(sequential, xrange(len(sequential)))
    return type('Enum', (), dict(sequential_dict, named))
