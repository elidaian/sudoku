import pytest
from sudoku.generator import generate

__author__ = "Eli Daian <elidaian@gmail.com>"


@pytest.fixture
def generated_board():
    '''
    :return: A generated board.
    :rtype: :class:`~board.Board`
    '''
    return generate(2, 2)
