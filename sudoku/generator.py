"""
This module generates sudoku boards.

:var DEFAULT_ALPHABET: The default alphabet used when no alphabet is given for generating the board.
:type DEFAULT_ALPHABET: str
"""
__author__ = 'Eli Daian <elidaian@gmail.com>'

from board import Board

DEFAULT_ALPHABET = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _construct_board(block_width, block_height):

def generate(block_width, block_height, alphabet=None):
    """
    Generate a new sudoku board.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board, or ``None`` for the default.
    :type alphabet: str
    :return: The generated board.
    :rtype: Board
    """

    board_size = block_height * block_width
    board_square_size = board_size * board_size

    if alphabet is None:
        if board_size > len(DEFAULT_ALPHABET):
            raise IndexError, "Board too long for default alphabet"
        alphabet = DEFAULT_ALPHABET[:board_size]

