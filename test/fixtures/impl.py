from internal.impl import BoardImpl

__author__ = 'Eli Daian <elidaian@gmail.com>'

import pytest


@pytest.fixture
def alphabet():
    return "1234"


@pytest.fixture
def alphabet10():
    return "0123456789"


@pytest.fixture
def board(alphabet):
    return BoardImpl(2, 2, alphabet)
