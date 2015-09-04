import pytest

from sudoku.exceptions import InvalidAlphabet, NoPossibleSymbols
from sudoku.impl.board import BoardImpl

__author__ = 'Eli Daian <elidaian@gmail.com>'


def test_board_is_valid_empty(board):
    assert board.is_valid()
    assert not board.is_final()


def test_board_invalid_alphabet():
    with pytest.raises(InvalidAlphabet):
        board = BoardImpl(3, 3, '1234')


def test_board_is_valid_partially_empty_valid(board):
    board[0, 0] = '2'
    board[0, 1] = '1'
    board[0, 2] = '3'
    board[0, 3] = '4'

    board[1, 0] = '3'
    board[1, 1] = '4'
    board[1, 2] = '2'
    board[1, 3] = '1'

    assert board.is_valid()
    assert not board.is_final()


def test_board_is_valid_no_empty_valid(board):
    board[0, 0] = '2'
    board[0, 1] = '1'
    board[0, 2] = '3'
    board[0, 3] = '4'

    board[1, 0] = '3'
    board[1, 1] = '4'
    board[1, 2] = '2'
    board[1, 3] = '1'

    board[2, 0] = '1'
    board[2, 1] = '2'
    board[2, 2] = '4'
    board[2, 3] = '3'

    board[3, 0] = '4'
    board[3, 1] = '3'
    board[3, 2] = '1'
    board[3, 3] = '2'

    assert board.is_valid()
    assert board.is_final()


def test_board_is_full_empty(board):
    assert not board.is_full()
    assert not board.is_final()
    assert board.is_empty()


def test_board_is_full_partially_empty(board):
    board[0, 0] = '2'
    board[0, 1] = '1'
    board[0, 2] = '3'
    board[0, 3] = '4'

    board[1, 0] = '3'
    board[1, 1] = '4'
    board[1, 2] = '2'
    board[1, 3] = '1'

    assert not board.is_full()
    assert not board.is_final()
    assert not board.is_empty()


def test_board_is_full_full(board):
    board[0, 0] = '2'
    board[0, 1] = '1'
    board[0, 2] = '3'
    board[0, 3] = '4'

    board[1, 0] = '3'
    board[1, 1] = '4'
    board[1, 2] = '2'
    board[1, 3] = '1'

    board[2, 0] = '1'
    board[2, 1] = '2'
    board[2, 2] = '4'
    board[2, 3] = '3'

    board[3, 0] = '4'
    board[3, 1] = '3'
    board[3, 2] = '1'
    board[3, 3] = '2'

    assert board.is_full()
    assert board.is_final()
    assert not board.is_empty()


def test_board_solve_possible_empty_board(board):
    board.solve_possible()
    assert board.is_empty()


def test_board_solve_possible_partial1(board):
    """
    Solve the board from this state:
    [[1,  , 2, 3],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ]]
    To this state:
    [[1, 4, 2, 3],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ]]
    """
    board[0, 0] = '1'
    board[0, 2] = '2'
    board[0, 3] = '3'

    board.solve_possible()

    assert not board.is_empty()
    assert not board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '1'
    assert board[0, 1] == '4'
    assert board[0, 2] == '2'
    assert board[0, 3] == '3'
    assert board[1, 0] is None
    assert board[1, 1] is None
    assert board[1, 2] is None
    assert board[1, 3] is None
    assert board[2, 0] is None
    assert board[2, 1] is None
    assert board[2, 2] is None
    assert board[2, 3] is None
    assert board[3, 0] is None
    assert board[3, 1] is None
    assert board[3, 2] is None
    assert board[3, 3] is None


def test_board_solve_possible_partial2(board):
    """
    Solve the board from this state:
    [[1,  ,  ,  ],
     [2, 3,  ,  ],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ]]
    To this state:
    [[1, 4,  ,  ],
     [2, 3,  ,  ],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ]]
    """
    board[0, 0] = '1'
    board[1, 0] = '2'
    board[1, 1] = '3'

    board.solve_possible()

    assert not board.is_empty()
    assert not board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '1'
    assert board[0, 1] == '4'
    assert board[0, 2] is None
    assert board[0, 3] is None
    assert board[1, 0] == '2'
    assert board[1, 1] == '3'
    assert board[1, 2] is None
    assert board[1, 3] is None
    assert board[2, 0] is None
    assert board[2, 1] is None
    assert board[2, 2] is None
    assert board[2, 3] is None
    assert board[3, 0] is None
    assert board[3, 1] is None
    assert board[3, 2] is None
    assert board[3, 3] is None


def test_board_solve_possible_partial3(board):
    """
    Solve the board from this state:
    [[1,  ,  ,  ],
     [2,  ,  ,  ],
     [3,  ,  ,  ],
     [ ,  ,  ,  ]]
    To this state:
    [[1,  ,  ,  ],
     [2,  ,  ,  ],
     [3,  ,  ,  ],
     [4,  ,  ,  ]]
    """
    board[0, 0] = '1'
    board[1, 0] = '2'
    board[2, 0] = '3'

    board.solve_possible()

    assert not board.is_empty()
    assert not board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '1'
    assert board[0, 1] is None
    assert board[0, 2] is None
    assert board[0, 3] is None
    assert board[1, 0] == '2'
    assert board[1, 1] is None
    assert board[1, 2] is None
    assert board[1, 3] is None
    assert board[2, 0] == '3'
    assert board[2, 1] is None
    assert board[2, 2] is None
    assert board[2, 3] is None
    assert board[3, 0] == '4'
    assert board[3, 1] is None
    assert board[3, 2] is None
    assert board[3, 3] is None


def test_board_solve_possible_partial4(board):
    """
    Solve the board from this state:
    [[1,  ,  ,  ],
     [ , 3,  , 1],
     [3,  ,  ,  ],
     [4,  ,  ,  ]]
    To this state:
    [[1, 4,  ,  ],
     [2, 3, 4, 1],
     [3,  ,  , 4],
     [4,  ,  ,  ]]
    """
    board[0, 0] = '1'
    board[1, 1] = '3'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[3, 0] = '4'

    board.solve_possible()

    assert not board.is_empty()
    assert not board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '1'
    assert board[0, 1] == '4'
    assert board[0, 2] is None
    assert board[0, 3] is None
    assert board[1, 0] == '2'
    assert board[1, 1] == '3'
    assert board[1, 2] == '4'
    assert board[1, 3] == '1'
    assert board[2, 0] == '3'
    assert board[2, 1] is None
    assert board[2, 2] is None
    assert board[2, 3] == '4'
    assert board[3, 0] == '4'
    assert board[3, 1] is None
    assert board[3, 2] is None
    assert board[3, 3] is None


def test_board_solve_possible_full1(board):
    """
    Solve the board from this state:
    [[ , 4, 1, 3],
     [ ,  ,  , 2],
     [ , 1,  ,  ],
     [4, 2,  ,  ]]
    To this state:
    [[2, 4, 1, 3],
     [1, 3, 4, 2],
     [3, 1, 2, 4],
     [4, 2, 3, 1]]
    """
    board[0, 1] = '4'
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 3] = '2'
    board[2, 1] = '1'
    board[3, 0] = '4'
    board[3, 1] = '2'

    board.solve_possible()

    assert not board.is_empty()
    assert board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '2'
    assert board[0, 1] == '4'
    assert board[0, 2] == '1'
    assert board[0, 3] == '3'
    assert board[1, 0] == '1'
    assert board[1, 1] == '3'
    assert board[1, 2] == '4'
    assert board[1, 3] == '2'
    assert board[2, 0] == '3'
    assert board[2, 1] == '1'
    assert board[2, 2] == '2'
    assert board[2, 3] == '4'
    assert board[3, 0] == '4'
    assert board[3, 1] == '2'
    assert board[3, 2] == '3'
    assert board[3, 3] == '1'


def test_board_solve_possible_full2(board):
    """
    Solve the board from this state:
    [[ ,  , 2, 1],
     [ ,  ,  ,  ],
     [ , 1,  , 4],
     [ , 3,  ,  ]]
    To this state:
    [[3, 4, 2, 1],
     [1, 2, 4, 3],
     [2, 1, 3, 4],
     [4, 3, 1, 2]]
    """
    board[0, 2] = '2'
    board[0, 3] = '1'
    board[2, 1] = '1'
    board[2, 3] = '4'
    board[3, 1] = '3'

    board.solve_possible()

    assert not board.is_empty()
    assert board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '3'
    assert board[0, 1] == '4'
    assert board[0, 2] == '2'
    assert board[0, 3] == '1'
    assert board[1, 0] == '1'
    assert board[1, 1] == '2'
    assert board[1, 2] == '4'
    assert board[1, 3] == '3'
    assert board[2, 0] == '2'
    assert board[2, 1] == '1'
    assert board[2, 2] == '3'
    assert board[2, 3] == '4'
    assert board[3, 0] == '4'
    assert board[3, 1] == '3'
    assert board[3, 2] == '1'
    assert board[3, 3] == '2'


def test_board_solve_possible_full3(board):
    """
    Solve the board from this state:
    [[ ,  ,  , 2],
     [4,  ,  , 1],
     [3, 1,  ,  ],
     [ , 4,  ,  ]]
    To this state:
    [[1, 3, 4, 2],
     [4, 2, 3, 1],
     [3, 1, 2, 4],
     [2, 4, 1, 3]]
    """
    board[0, 3] = '2'
    board[1, 0] = '4'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[2, 1] = '1'
    board[3, 1] = '4'

    board.solve_possible()

    assert not board.is_empty()
    assert board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '1'
    assert board[0, 1] == '3'
    assert board[0, 2] == '4'
    assert board[0, 3] == '2'
    assert board[1, 0] == '4'
    assert board[1, 1] == '2'
    assert board[1, 2] == '3'
    assert board[1, 3] == '1'
    assert board[2, 0] == '3'
    assert board[2, 1] == '1'
    assert board[2, 2] == '2'
    assert board[2, 3] == '4'
    assert board[3, 0] == '2'
    assert board[3, 1] == '4'
    assert board[3, 2] == '1'
    assert board[3, 3] == '3'


def test_board_solve_possible_full4(board):
    """
    Solve the board from this state:
    [[ ,  , 1, 3],
     [ , 3,  ,  ],
     [ , 2,  ,  ],
     [4, 1,  ,  ]]
    To this state:
    [[2, 4, 1, 3],
     [1, 3, 2, 4],
     [3, 2, 4, 1],
     [4, 1, 3, 2]]
    """
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 1] = '3'
    board[2, 1] = '2'
    board[3, 0] = '4'
    board[3, 1] = '1'

    board.solve_possible()

    assert not board.is_empty()
    assert board.is_full()
    assert board.is_valid()

    assert board[0, 0] == '2'
    assert board[0, 1] == '4'
    assert board[0, 2] == '1'
    assert board[0, 3] == '3'
    assert board[1, 0] == '1'
    assert board[1, 1] == '3'
    assert board[1, 2] == '2'
    assert board[1, 3] == '4'
    assert board[2, 0] == '3'
    assert board[2, 1] == '2'
    assert board[2, 2] == '4'
    assert board[2, 3] == '1'
    assert board[3, 0] == '4'
    assert board[3, 1] == '1'
    assert board[3, 2] == '3'
    assert board[3, 3] == '2'


def test_board_solve_regular_full1(board9):
    """
    Solve the board from this state:
    [[ ,  ,  ,  ,  , 9,  , 7, 5],
     [ ,  ,  , 3,  ,  , 2,  ,  ],
     [ ,  , 1, 2,  , 4,  ,  ,  ],
     [9,  ,  ,  ,  ,  ,  ,  ,  ],
     [ ,  ,  , 6,  ,  ,  ,  , 1],
     [2,  ,  ,  ,  ,  , 5,  ,  ],
     [4, 9,  ,  , 1, 2,  ,  , 7],
     [ , 7,  ,  ,  , 8,  , 3,  ],
     [ ,  ,  ,  , 9,  , 1,  ,  ]]
    To this state:
    [[3, 6, 2, 1, 8, 9, 4, 7, 5],
     [7, 4, 9, 3, 5, 6, 2, 1, 8],
     [8, 5, 1, 2, 7, 4, 3, 6, 9],
     [9, 1, 6, 8, 4, 5, 7, 2, 3],
     [5, 3, 4, 6, 2, 7, 8, 9, 1],
     [2, 8, 7, 9, 3, 1, 5, 4, 6],
     [4, 9, 3, 5, 1, 2, 6, 8, 7],
     [1, 7, 5, 4, 6, 8, 9, 3, 2],
     [6, 2, 8, 7, 9, 3, 1, 5, 4]]
    """
    board9[0, 5] = '9'
    board9[0, 7] = '7'
    board9[0, 8] = '5'
    board9[1, 3] = '3'
    board9[1, 6] = '2'
    board9[2, 2] = '1'
    board9[2, 3] = '2'
    board9[2, 5] = '4'
    board9[3, 0] = '9'
    board9[4, 3] = '6'
    board9[4, 8] = '1'
    board9[5, 0] = '2'
    board9[5, 6] = '5'
    board9[6, 0] = '4'
    board9[6, 1] = '9'
    board9[6, 4] = '1'
    board9[6, 5] = '2'
    board9[6, 8] = '7'
    board9[7, 1] = '7'
    board9[7, 5] = '8'
    board9[7, 7] = '3'
    board9[8, 4] = '9'
    board9[8, 6] = '1'

    board9.solve_possible()

    assert not board9.is_empty()
    assert board9.is_full()
    assert board9.is_valid()

    assert board9[0, 0] == '3'
    assert board9[0, 1] == '6'
    assert board9[0, 2] == '2'
    assert board9[0, 3] == '1'
    assert board9[0, 4] == '8'
    assert board9[0, 5] == '9'
    assert board9[0, 6] == '4'
    assert board9[0, 7] == '7'
    assert board9[0, 8] == '5'
    assert board9[1, 0] == '7'
    assert board9[1, 1] == '4'
    assert board9[1, 2] == '9'
    assert board9[1, 3] == '3'
    assert board9[1, 4] == '5'
    assert board9[1, 5] == '6'
    assert board9[1, 6] == '2'
    assert board9[1, 7] == '1'
    assert board9[1, 8] == '8'
    assert board9[2, 0] == '8'
    assert board9[2, 1] == '5'
    assert board9[2, 2] == '1'
    assert board9[2, 3] == '2'
    assert board9[2, 4] == '7'
    assert board9[2, 5] == '4'
    assert board9[2, 6] == '3'
    assert board9[2, 7] == '6'
    assert board9[2, 8] == '9'
    assert board9[3, 0] == '9'
    assert board9[3, 1] == '1'
    assert board9[3, 2] == '6'
    assert board9[3, 3] == '8'
    assert board9[3, 4] == '4'
    assert board9[3, 5] == '5'
    assert board9[3, 6] == '7'
    assert board9[3, 7] == '2'
    assert board9[3, 8] == '3'
    assert board9[4, 0] == '5'
    assert board9[4, 1] == '3'
    assert board9[4, 2] == '4'
    assert board9[4, 3] == '6'
    assert board9[4, 4] == '2'
    assert board9[4, 5] == '7'
    assert board9[4, 6] == '8'
    assert board9[4, 7] == '9'
    assert board9[4, 8] == '1'
    assert board9[5, 0] == '2'
    assert board9[5, 1] == '8'
    assert board9[5, 2] == '7'
    assert board9[5, 3] == '9'
    assert board9[5, 4] == '3'
    assert board9[5, 5] == '1'
    assert board9[5, 6] == '5'
    assert board9[5, 7] == '4'
    assert board9[5, 8] == '6'
    assert board9[6, 0] == '4'
    assert board9[6, 1] == '9'
    assert board9[6, 2] == '3'
    assert board9[6, 3] == '5'
    assert board9[6, 4] == '1'
    assert board9[6, 5] == '2'
    assert board9[6, 6] == '6'
    assert board9[6, 7] == '8'
    assert board9[6, 8] == '7'
    assert board9[7, 0] == '1'
    assert board9[7, 1] == '7'
    assert board9[7, 2] == '5'
    assert board9[7, 3] == '4'
    assert board9[7, 4] == '6'
    assert board9[7, 5] == '8'
    assert board9[7, 6] == '9'
    assert board9[7, 7] == '3'
    assert board9[7, 8] == '2'
    assert board9[8, 0] == '6'
    assert board9[8, 1] == '2'
    assert board9[8, 2] == '8'
    assert board9[8, 3] == '7'
    assert board9[8, 4] == '9'
    assert board9[8, 5] == '3'
    assert board9[8, 6] == '1'
    assert board9[8, 7] == '5'
    assert board9[8, 8] == '4'


def test_board_solve_regular_full2(board9):
    """
    Solve the board from this state:

    [[5,  ,  ,  ,  , 8,  , 4,  ],
     [3,  ,  ,  ,  , 7,  , 9,  ],
     [6,  ,  ,  , 2,  ,  ,  , 5],
     [ , 3,  ,  ,  ,  ,  ,  , 8],
     [ ,  , 6, 5, 9, 1, 4,  ,  ],
     [7, 1,  ,  ,  ,  , 2,  ,  ],
     [1,  , 2, 8,  ,  , 6,  , 4],
     [ ,  ,  , 9,  ,  , 5,  , 7],
     [ , 5,  ,  ,  , 3, 9,  , 1]]
    To this state:
    [[5, 2, 9, 1, 3, 8, 7, 4, 6],
     [3, 4, 1, 6, 5, 7, 8, 9, 2],
     [6, 7, 8, 4, 2, 9, 3, 1, 5],
     [9, 3, 5, 7, 4, 2, 1, 6, 8],
     [2, 8, 6, 5, 9, 1, 4, 7, 3],
     [7, 1, 4, 3, 8, 6, 2, 5, 9],
     [1, 9, 2, 8, 7, 5, 6, 3, 4],
     [8, 6, 3, 9, 1, 4, 5, 2, 7],
     [4, 5, 7, 2, 6, 3, 9, 8, 1]]
    """
    board9[0, 0] = '5'
    board9[0, 5] = '8'
    board9[0, 7] = '4'
    board9[1, 0] = '3'
    board9[1, 5] = '7'
    board9[1, 7] = '9'
    board9[2, 0] = '6'
    board9[2, 4] = '2'
    board9[2, 8] = '5'
    board9[3, 1] = '3'
    board9[3, 8] = '8'
    board9[4, 2] = '6'
    board9[4, 3] = '5'
    board9[4, 4] = '9'
    board9[4, 5] = '1'
    board9[4, 6] = '4'
    board9[5, 0] = '7'
    board9[5, 1] = '1'
    board9[5, 6] = '2'
    board9[6, 0] = '1'
    board9[6, 2] = '2'
    board9[6, 3] = '8'
    board9[6, 6] = '6'
    board9[6, 8] = '4'
    board9[7, 3] = '9'
    board9[7, 6] = '5'
    board9[7, 8] = '7'
    board9[8, 1] = '5'
    board9[8, 5] = '3'
    board9[8, 6] = '9'
    board9[8, 8] = '1'

    board9.solve_possible()

    assert not board9.is_empty()
    assert board9.is_full()
    assert board9.is_valid()

    assert board9[0, 0] == '5'
    assert board9[0, 1] == '2'
    assert board9[0, 2] == '9'
    assert board9[0, 3] == '1'
    assert board9[0, 4] == '3'
    assert board9[0, 5] == '8'
    assert board9[0, 6] == '7'
    assert board9[0, 7] == '4'
    assert board9[0, 8] == '6'
    assert board9[1, 0] == '3'
    assert board9[1, 1] == '4'
    assert board9[1, 2] == '1'
    assert board9[1, 3] == '6'
    assert board9[1, 4] == '5'
    assert board9[1, 5] == '7'
    assert board9[1, 6] == '8'
    assert board9[1, 7] == '9'
    assert board9[1, 8] == '2'
    assert board9[2, 0] == '6'
    assert board9[2, 1] == '7'
    assert board9[2, 2] == '8'
    assert board9[2, 3] == '4'
    assert board9[2, 4] == '2'
    assert board9[2, 5] == '9'
    assert board9[2, 6] == '3'
    assert board9[2, 7] == '1'
    assert board9[2, 8] == '5'
    assert board9[3, 0] == '9'
    assert board9[3, 1] == '3'
    assert board9[3, 2] == '5'
    assert board9[3, 3] == '7'
    assert board9[3, 4] == '4'
    assert board9[3, 5] == '2'
    assert board9[3, 6] == '1'
    assert board9[3, 7] == '6'
    assert board9[3, 8] == '8'
    assert board9[4, 0] == '2'
    assert board9[4, 1] == '8'
    assert board9[4, 2] == '6'
    assert board9[4, 3] == '5'
    assert board9[4, 4] == '9'
    assert board9[4, 5] == '1'
    assert board9[4, 6] == '4'
    assert board9[4, 7] == '7'
    assert board9[4, 8] == '3'
    assert board9[5, 0] == '7'
    assert board9[5, 1] == '1'
    assert board9[5, 2] == '4'
    assert board9[5, 3] == '3'
    assert board9[5, 4] == '8'
    assert board9[5, 5] == '6'
    assert board9[5, 6] == '2'
    assert board9[5, 7] == '5'
    assert board9[5, 8] == '9'
    assert board9[6, 0] == '1'
    assert board9[6, 1] == '9'
    assert board9[6, 2] == '2'
    assert board9[6, 3] == '8'
    assert board9[6, 4] == '7'
    assert board9[6, 5] == '5'
    assert board9[6, 6] == '6'
    assert board9[6, 7] == '3'
    assert board9[6, 8] == '4'
    assert board9[7, 0] == '8'
    assert board9[7, 1] == '6'
    assert board9[7, 2] == '3'
    assert board9[7, 3] == '9'
    assert board9[7, 4] == '1'
    assert board9[7, 5] == '4'
    assert board9[7, 6] == '5'
    assert board9[7, 7] == '2'
    assert board9[7, 8] == '7'
    assert board9[8, 0] == '4'
    assert board9[8, 1] == '5'
    assert board9[8, 2] == '7'
    assert board9[8, 3] == '2'
    assert board9[8, 4] == '6'
    assert board9[8, 5] == '3'
    assert board9[8, 6] == '9'
    assert board9[8, 7] == '8'
    assert board9[8, 8] == '1'


def test_board_solve_regular_full3(board9):
    """
    Solve the board from this state:
    [[ ,  , 5, 1,  ,  , 3,  ,  ],
     [ ,  , 9, 6,  ,  ,  ,  , 7],
     [ ,  ,  ,  ,  , 7, 1, 9,  ],
     [ , 6,  ,  ,  ,  ,  ,  , 8],
     [ ,  ,  ,  ,  ,  ,  , 3,  ],
     [ , 4,  , 5, 9, 1,  ,  ,  ],
     [ ,  ,  ,  ,  ,  , 6, 7,  ],
     [4,  ,  ,  ,  ,  ,  ,  , 2],
     [ , 8,  ,  , 7,  ,  ,  ,  ]]
    To this state:
    [[8, 7, 5, 1, 2, 9, 3, 6, 4],
     [1, 3, 9, 6, 5, 4, 2, 8, 7],
     [6, 2, 4, 3, 8, 7, 1, 9, 5],
     [5, 6, 1, 7, 3, 2, 9, 4, 8],
     [7, 9, 2, 8, 4, 6, 5, 3, 1],
     [3, 4, 8, 5, 9, 1, 7, 2, 6],
     [2, 5, 3, 4, 1, 8, 6, 7, 9],
     [4, 1, 7, 9, 6, 3, 8, 5, 2],
     [9, 8, 6, 2, 7, 5, 4, 1, 3]]
    """
    board9[0, 2] = '5'
    board9[0, 3] = '1'
    board9[0, 6] = '3'
    board9[1, 2] = '9'
    board9[1, 3] = '6'
    board9[1, 8] = '7'
    board9[2, 5] = '7'
    board9[2, 6] = '1'
    board9[2, 7] = '9'
    board9[3, 1] = '6'
    board9[3, 8] = '8'
    board9[4, 7] = '3'
    board9[5, 1] = '4'
    board9[5, 3] = '5'
    board9[5, 4] = '9'
    board9[5, 5] = '1'
    board9[6, 6] = '6'
    board9[6, 7] = '7'
    board9[7, 0] = '4'
    board9[7, 8] = '2'
    board9[8, 1] = '8'
    board9[8, 4] = '7'

    board9.solve_possible()

    assert not board9.is_empty()
    assert board9.is_full()
    assert board9.is_valid()

    assert board9[0, 0] == '8'
    assert board9[0, 1] == '7'
    assert board9[0, 2] == '5'
    assert board9[0, 3] == '1'
    assert board9[0, 4] == '2'
    assert board9[0, 5] == '9'
    assert board9[0, 6] == '3'
    assert board9[0, 7] == '6'
    assert board9[0, 8] == '4'
    assert board9[1, 0] == '1'
    assert board9[1, 1] == '3'
    assert board9[1, 2] == '9'
    assert board9[1, 3] == '6'
    assert board9[1, 4] == '5'
    assert board9[1, 5] == '4'
    assert board9[1, 6] == '2'
    assert board9[1, 7] == '8'
    assert board9[1, 8] == '7'
    assert board9[2, 0] == '6'
    assert board9[2, 1] == '2'
    assert board9[2, 2] == '4'
    assert board9[2, 3] == '3'
    assert board9[2, 4] == '8'
    assert board9[2, 5] == '7'
    assert board9[2, 6] == '1'
    assert board9[2, 7] == '9'
    assert board9[2, 8] == '5'
    assert board9[3, 0] == '5'
    assert board9[3, 1] == '6'
    assert board9[3, 2] == '1'
    assert board9[3, 3] == '7'
    assert board9[3, 4] == '3'
    assert board9[3, 5] == '2'
    assert board9[3, 6] == '9'
    assert board9[3, 7] == '4'
    assert board9[3, 8] == '8'
    assert board9[4, 0] == '7'
    assert board9[4, 1] == '9'
    assert board9[4, 2] == '2'
    assert board9[4, 3] == '8'
    assert board9[4, 4] == '4'
    assert board9[4, 5] == '6'
    assert board9[4, 6] == '5'
    assert board9[4, 7] == '3'
    assert board9[4, 8] == '1'
    assert board9[5, 0] == '3'
    assert board9[5, 1] == '4'
    assert board9[5, 2] == '8'
    assert board9[5, 3] == '5'
    assert board9[5, 4] == '9'
    assert board9[5, 5] == '1'
    assert board9[5, 6] == '7'
    assert board9[5, 7] == '2'
    assert board9[5, 8] == '6'
    assert board9[6, 0] == '2'
    assert board9[6, 1] == '5'
    assert board9[6, 2] == '3'
    assert board9[6, 3] == '4'
    assert board9[6, 4] == '1'
    assert board9[6, 5] == '8'
    assert board9[6, 6] == '6'
    assert board9[6, 7] == '7'
    assert board9[6, 8] == '9'
    assert board9[7, 0] == '4'
    assert board9[7, 1] == '1'
    assert board9[7, 2] == '7'
    assert board9[7, 3] == '9'
    assert board9[7, 4] == '6'
    assert board9[7, 5] == '3'
    assert board9[7, 6] == '8'
    assert board9[7, 7] == '5'
    assert board9[7, 8] == '2'
    assert board9[8, 0] == '9'
    assert board9[8, 1] == '8'
    assert board9[8, 2] == '6'
    assert board9[8, 3] == '2'
    assert board9[8, 4] == '7'
    assert board9[8, 5] == '5'
    assert board9[8, 6] == '4'
    assert board9[8, 7] == '1'
    assert board9[8, 8] == '3'


def test_board_solve_regular_full4(board9):
    """
    Solve the board from this state:
    [[ ,  ,  ,  ,  , 1,  , 9,  ],
     [ ,  , 6, 8, 7,  ,  ,  ,  ],
     [1,  , 5,  ,  ,  ,  ,  ,  ],
     [ , 9,  ,  ,  , 3, 4,  , 5],
     [ ,  , 8,  , 9,  ,  ,  ,  ],
     [ ,  ,  , 5,  ,  ,  , 1,  ],
     [5,  , 7, 9,  ,  , 3,  , 2],
     [ ,  ,  ,  , 6,  , 5,  , 7],
     [2,  ,  ,  ,  ,  ,  ,  ,  ]]
    To this state:
    [[8, 4, 2, 3, 5, 1, 7, 9, 6],
     [9, 3, 6, 8, 7, 4, 2, 5, 1],
     [1, 7, 5, 6, 2, 9, 8, 3, 4],
     [6, 9, 1, 2, 8, 3, 4, 7, 5],
     [4, 5, 8, 1, 9, 7, 6, 2, 3],
     [7, 2, 3, 5, 4, 6, 9, 1, 8],
     [5, 6, 7, 9, 1, 8, 3, 4, 2],
     [3, 1, 9, 4, 6, 2, 5, 8, 7],
     [2, 8, 4, 7, 3, 5, 1, 6, 9]]
    """
    board9[0, 5] = '1'
    board9[0, 7] = '9'
    board9[1, 2] = '6'
    board9[1, 3] = '8'
    board9[1, 4] = '7'
    board9[2, 0] = '1'
    board9[2, 2] = '5'
    board9[3, 1] = '9'
    board9[3, 5] = '3'
    board9[3, 6] = '4'
    board9[3, 8] = '5'
    board9[4, 2] = '8'
    board9[4, 4] = '9'
    board9[5, 3] = '5'
    board9[5, 7] = '1'
    board9[6, 0] = '5'
    board9[6, 2] = '7'
    board9[6, 3] = '9'
    board9[6, 6] = '3'
    board9[6, 8] = '2'
    board9[7, 4] = '6'
    board9[7, 6] = '5'
    board9[7, 8] = '7'
    board9[8, 0] = '2'

    board9.solve_possible()

    assert not board9.is_empty()
    assert board9.is_full()
    assert board9.is_valid()

    assert board9[0, 0] == '8'
    assert board9[0, 1] == '4'
    assert board9[0, 2] == '2'
    assert board9[0, 3] == '3'
    assert board9[0, 4] == '5'
    assert board9[0, 5] == '1'
    assert board9[0, 6] == '7'
    assert board9[0, 7] == '9'
    assert board9[0, 8] == '6'
    assert board9[1, 0] == '9'
    assert board9[1, 1] == '3'
    assert board9[1, 2] == '6'
    assert board9[1, 3] == '8'
    assert board9[1, 4] == '7'
    assert board9[1, 5] == '4'
    assert board9[1, 6] == '2'
    assert board9[1, 7] == '5'
    assert board9[1, 8] == '1'
    assert board9[2, 0] == '1'
    assert board9[2, 1] == '7'
    assert board9[2, 2] == '5'
    assert board9[2, 3] == '6'
    assert board9[2, 4] == '2'
    assert board9[2, 5] == '9'
    assert board9[2, 6] == '8'
    assert board9[2, 7] == '3'
    assert board9[2, 8] == '4'
    assert board9[3, 0] == '6'
    assert board9[3, 1] == '9'
    assert board9[3, 2] == '1'
    assert board9[3, 3] == '2'
    assert board9[3, 4] == '8'
    assert board9[3, 5] == '3'
    assert board9[3, 6] == '4'
    assert board9[3, 7] == '7'
    assert board9[3, 8] == '5'
    assert board9[4, 0] == '4'
    assert board9[4, 1] == '5'
    assert board9[4, 2] == '8'
    assert board9[4, 3] == '1'
    assert board9[4, 4] == '9'
    assert board9[4, 5] == '7'
    assert board9[4, 6] == '6'
    assert board9[4, 7] == '2'
    assert board9[4, 8] == '3'
    assert board9[5, 0] == '7'
    assert board9[5, 1] == '2'
    assert board9[5, 2] == '3'
    assert board9[5, 3] == '5'
    assert board9[5, 4] == '4'
    assert board9[5, 5] == '6'
    assert board9[5, 6] == '9'
    assert board9[5, 7] == '1'
    assert board9[5, 8] == '8'
    assert board9[6, 0] == '5'
    assert board9[6, 1] == '6'
    assert board9[6, 2] == '7'
    assert board9[6, 3] == '9'
    assert board9[6, 4] == '1'
    assert board9[6, 5] == '8'
    assert board9[6, 6] == '3'
    assert board9[6, 7] == '4'
    assert board9[6, 8] == '2'
    assert board9[7, 0] == '3'
    assert board9[7, 1] == '1'
    assert board9[7, 2] == '9'
    assert board9[7, 3] == '4'
    assert board9[7, 4] == '6'
    assert board9[7, 5] == '2'
    assert board9[7, 6] == '5'
    assert board9[7, 7] == '8'
    assert board9[7, 8] == '7'
    assert board9[8, 0] == '2'
    assert board9[8, 1] == '8'
    assert board9[8, 2] == '4'
    assert board9[8, 3] == '7'
    assert board9[8, 4] == '3'
    assert board9[8, 5] == '5'
    assert board9[8, 6] == '1'
    assert board9[8, 7] == '6'
    assert board9[8, 8] == '9'


def test_board_solve_possible_impossible(board):
    """
    Try solving the following board:
    [[1,  , 2, 3],
     [ , 4,  ,  ],
     [ ,  ,  ,  ],
     [ ,  ,  ,  ]]
     Since this board is impossible to get solved, an exception is expected to be raised.
    """
    board[0, 0] = '1'
    board[0, 2] = '2'
    board[0, 3] = '3'
    board[1, 1] = '4'

    with pytest.raises(NoPossibleSymbols):
        board.solve_possible()


def test_board_copy_empty(board):
    board2 = board.copy()

    for row in xrange(4):
        for col in xrange(4):
            assert board[row, col] == board2[row, col]


def test_board_copy1(board):
    board[0, 3] = '2'
    board[1, 0] = '4'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[2, 1] = '1'
    board[3, 1] = '4'

    board2 = board.copy()

    for row in xrange(4):
        for col in xrange(4):
            assert board[row, col] == board2[row, col]


def test_board_copy2(board):
    board[0, 0] = '1'
    board[0, 1] = '3'
    board[0, 2] = '4'
    board[0, 3] = '2'
    board[1, 0] = '4'
    board[1, 1] = '2'
    board[1, 2] = '3'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[2, 1] = '1'
    board[2, 2] = '2'
    board[2, 3] = '4'
    board[3, 0] = '2'
    board[3, 1] = '4'
    board[3, 2] = '1'
    board[3, 3] = '3'

    board2 = board.copy()

    for row in xrange(4):
        for col in xrange(4):
            assert board[row, col] == board2[row, col]


def test_board_copy3(board):
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 1] = '3'
    board[2, 1] = '2'
    board[3, 0] = '4'
    board[3, 1] = '1'

    board2 = board.copy()

    for row in xrange(4):
        for col in xrange(4):
            assert board[row, col] == board2[row, col]


def test_board_copy4(board):
    board[0, 0] = '2'
    board[0, 1] = '4'
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 0] = '1'
    board[1, 1] = '3'
    board[1, 2] = '2'
    board[1, 3] = '4'
    board[2, 0] = '3'
    board[2, 1] = '2'
    board[2, 2] = '4'
    board[2, 3] = '1'
    board[3, 0] = '4'
    board[3, 1] = '1'
    board[3, 2] = '3'
    board[3, 3] = '2'

    board2 = board.copy()

    for row in xrange(4):
        for col in xrange(4):
            assert board[row, col] == board2[row, col]


def test_board_str_empty(board):
    assert ' ' * 16 == str(board)


def test_board_str1(board):
    board[0, 3] = '2'
    board[1, 0] = '4'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[2, 1] = '1'
    board[3, 1] = '4'

    assert '   24  131   4  ' == str(board)


def test_board_str2(board):
    board[0, 0] = '1'
    board[0, 1] = '3'
    board[0, 2] = '4'
    board[0, 3] = '2'
    board[1, 0] = '4'
    board[1, 1] = '2'
    board[1, 2] = '3'
    board[1, 3] = '1'
    board[2, 0] = '3'
    board[2, 1] = '1'
    board[2, 2] = '2'
    board[2, 3] = '4'
    board[3, 0] = '2'
    board[3, 1] = '4'
    board[3, 2] = '1'
    board[3, 3] = '3'

    assert '1342423131242413' == str(board)


def test_board_str3(board):
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 1] = '3'
    board[2, 1] = '2'
    board[3, 0] = '4'
    board[3, 1] = '1'

    assert '  13 3   2  41  ' == str(board)


def test_board_str4(board):
    board[0, 0] = '2'
    board[0, 1] = '4'
    board[0, 2] = '1'
    board[0, 3] = '3'
    board[1, 0] = '1'
    board[1, 1] = '3'
    board[1, 2] = '2'
    board[1, 3] = '4'
    board[2, 0] = '3'
    board[2, 1] = '2'
    board[2, 2] = '4'
    board[2, 3] = '1'
    board[3, 0] = '4'
    board[3, 1] = '1'
    board[3, 2] = '3'
    board[3, 3] = '2'

    assert '2413132432414132' == str(board)

# def test_board_is_valid_partially_empty_invalid(board):
#     board[0, 0] = '2'
#     board[0, 1] = '1'
#     board[0, 2] = '3'
#     board[0, 3] = '4'
#
#     board[1, 0] = '1'
#
#     assert not board.is_valid()
#     assert not board.is_final()


# def test_board_is_valid_no_empty_invalid(board):
#     board[0, 0] = '2'
#     board[0, 1] = '1'
#     board[0, 2] = '3'
#     board[0, 3] = '4'
#
#     board[1, 0] = '3'
#     board[1, 1] = '4'
#     board[1, 2] = '2'
#     board[1, 3] = '1'
#
#     board[2, 0] = '1'
#     board[2, 1] = '2'
#     board[2, 2] = '4'
#     board[2, 3] = '3'
#
#     board[3, 0] = '4'
#     board[3, 1] = '3'
#     board[3, 2] = '3'
#     board[3, 3] = '2'
#
#     assert not board.is_valid()
#     assert not board.is_final()
