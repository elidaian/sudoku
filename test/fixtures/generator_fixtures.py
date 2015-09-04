import pytest

from edsudoku.generator import generate

__author__ = 'Eli Daian <elidaian@gmail.com>'


@pytest.fixture
def generated_board():
    """
    :return: A generated board.
    :rtype: :class:`~board.Board`
    """
    return generate(2, 2)


@pytest.fixture
def generated_board9():
    """
    :return: A generated board of regular size.
    :rtype: :class:`~board.Board`
    """
    return generate(3, 3)


@pytest.fixture
def generated_dodeka():
    """
    :return: A generated dodeka board.
    :rtype: :class:`~board.Board`
    """
    return generate(3, 4)
