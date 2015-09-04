import pytest

from edsudoku.impl.board import BoardImpl

__author__ = 'Eli Daian <elidaian@gmail.com>'


@pytest.fixture
def alphabet():
    return '1234'


@pytest.fixture
def alphabet9():
    return '123456789'


@pytest.fixture
def alphabet10():
    return '0123456789'


@pytest.fixture
def board(alphabet):
    return BoardImpl(2, 2, alphabet)


@pytest.fixture
def board9(alphabet9):
    return BoardImpl(3, 3, alphabet9)
