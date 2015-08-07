__author__ = 'Eli Daian <elidaian@gmail.com>'

import pytest

from sudoku.internal.impl import Cell, CellGroup, BoardImpl


def test_cell_legal_alphabet(alphabet):
    cell = Cell(0, 0, alphabet, '2')


def test_cell_illegal_alphabet(alphabet):
    with pytest.raises(AssertionError):
        cell = Cell(0, 0, alphabet, 'A')


def test_cell_set_symbol_legal(alphabet):
    cell = Cell(0, 0, alphabet)

    cell.set_symbol('1')
    cell.set_symbol('2')


def test_cell_set_symbol_illegal1(alphabet):
    cell = Cell(0, 0, alphabet, '2')

    with pytest.raises(AssertionError):
        cell.set_symbol('a')


def test_cell_set_symbol_illegal2(alphabet):
    cell = Cell(0, 0, alphabet)

    with pytest.raises(AssertionError):
        cell.set_symbol('a')


def test_cell_set_symbol_legal1(alphabet):
    cell = Cell(0, 0, alphabet, '2')

    cell.set_symbol('2')
    cell.set_symbol('1')
    cell.set_symbol('3')
    cell.set_symbol('1')


def test_cell_set_symbol_legal2(alphabet):
    cell = Cell(0, 0, alphabet)

    cell.set_symbol('2')
    cell.set_symbol('1')
    cell.set_symbol('3')
    cell.set_symbol('1')


def test_cell_group_is_valid_empty_cells(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.is_valid()


def test_cell_group_is_valid_partially_empty_valid(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    cells[0].set_symbol('0')
    cells[1].set_symbol('1')

    assert group.is_valid()


# def test_cell_group_is_valid_partially_empty_invalid(alphabet10):
#     cells = [Cell(0, y, alphabet10) for y in xrange(10)]
#     group = CellGroup(set(cells))
# 
#     cells[0].set_symbol('0')
#     cells[1].set_symbol('1')
#     cells[5].set_symbol('0')
# 
#     assert not group.is_valid()


def test_cell_group_is_valid_no_empty_valid(alphabet10):
    cells = [Cell(0, y, alphabet10, str(y)) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.is_valid()


# def test_cell_group_is_valid_no_empty_invalid(alphabet10):
#     cells = [Cell(0, y, alphabet10, str(y)) for y in xrange(10)]
#     group = CellGroup(set(cells))
# 
#     cells[4].set_symbol('5')
# 
#     assert not group.is_valid()


def test_cell_group_update_possible_symbols_full_group(alphabet10):
    cells = [Cell(0, y, alphabet10, str(y)) for y in xrange(10)]
    group = CellGroup(set(cells))

    for cell in cells:
        assert cell.get_num_possible_symbols() == 0


def test_cell_group_update_possible_symbols_empty_group(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    for cell in cells:
        assert cell.get_possible_symbols() == set(alphabet10)


def test_cell_group_update_possible_symbols_partially_empty(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    cells[2].set_symbol('2')
    cells[4].set_symbol('7')


def test_board_is_valid_empty(board):
    assert board.is_valid()
    assert not board.is_final()


def test_board_is_valid_patrially_empty_valid(board):
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
    Solve the board from this state:
    [[1,  ,  ,  ],
     [ , 3,  , 1],
     [3,  ,  ,  ],
     [4,  ,  ,  ]]
    To this state:
    [[1, 4,  ,  ],
     [2, 3, 4, 1],
     [3,  ,  ,  ],
     [4,  ,  ,  ]]
    '''
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
    assert board[2, 3] is None
    assert board[3, 0] == '4'
    assert board[3, 1] is None
    assert board[3, 2] is None
    assert board[3, 3] is None


def test_board_solve_possible_full1(board):
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
