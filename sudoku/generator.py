'''
This module generates sudoku boards.

:var DEFAULT_ALPHABET: The default alphabet used when no alphabet is given for generating the board.
:type DEFAULT_ALPHABET: str
'''
from random import randint, choice
from internal.impl import BoardImpl

__author__ = 'Eli Daian <elidaian@gmail.com>'

from board import Board

DEFAULT_ALPHABET = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
''' Default alphabet to be used if no alphabet is given. '''


def _construct_board(block_width, block_height, alphabet):
    '''
    Construct a new board, that consists of a problem ans solution.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board.
    :type alphabet: str
    :return: A tuple of the problem and solution board strings.
    :rtype: tuple of str-s.
    '''

    solution = BoardImpl(block_width, block_height, alphabet)

    while not solution.is_final():
        problem = solution

        pos = None
        while not pos:
            row = randint(0, problem.rows - 1)
            col = randint(0, problem.cols - 1)

            if problem.get_num_possible_symbols(row, col) > 1:
                pos = (row, col)

        symbol = choice(problem.get_possible_symbols(*pos))
        problem[pos] = symbol

        solution = problem.copy()
        solution.solve_possible()

    return str(problem), str(solution)

def generate(block_width, block_height, alphabet=None):
    '''
    Generate a new sudoku board.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board, or ``None`` for the default.
    :type alphabet: str
    :return: The generated board.
    :rtype: Board
    '''

    board_size = block_height * block_width
    board_square_size = board_size * board_size

    if alphabet is None:
        if board_size > len(DEFAULT_ALPHABET):
            raise IndexError, 'Board too long for default alphabet'
        alphabet = DEFAULT_ALPHABET[:board_size]
