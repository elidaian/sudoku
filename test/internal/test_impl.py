__author__ = 'Eli Daian <elidaian@gmail.com>'

from sudoku.internal.impl import Cell, CellGroup, BoardImpl


def test_cell_group_is_valid_empty_cells():
    cells = [Cell(0, y) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.is_valid()


def test_cell_group_is_valid_partially_empty_valid():
    cells = [Cell(0, y) for y in xrange(10)]
    group = CellGroup(set(cells))

    cells[0].set_symbol('0')
    cells[1].set_symbol('1')

    assert group.is_valid()


def test_cell_group_is_valid_partially_empty_invalid():
    cells = [Cell(0, y) for y in xrange(10)]
    group = CellGroup(set(cells))

    cells[0].set_symbol('0')
    cells[1].set_symbol('1')
    cells[5].set_symbol('0')

    assert not group.is_valid()


def test_cell_group_is_valid_no_empty_valid():
    cells = [Cell(0, y, str(y)) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.is_valid()


def test_cell_group_is_valid_no_empty_invalid():
    cells = [Cell(0, y, str(y)) for y in xrange(10)]
    group = CellGroup(set(cells))

    cells[4].set_symbol('5')

    assert not group.is_valid()


def test_board_is_valid_empty():
    board = BoardImpl(2, 2)

    assert board.is_valid()
    assert not board.is_final()


def test_board_is_valid_patrially_empty_valid():
    board = BoardImpl(2, 2)

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


def test_board_is_valid_partially_empty_invalid():
    board = BoardImpl(2, 2)

    board[0, 0] = '2'
    board[0, 1] = '1'
    board[0, 2] = '3'
    board[0, 3] = '4'

    board[1, 0] = '1'

    assert not board.is_valid()
    assert not board.is_final()


def test_board_is_valid_no_empty_valid():
    board = BoardImpl(2, 2)

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


def test_board_is_valid_no_empty_invalid():
    board = BoardImpl(2, 2)

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
    board[3, 2] = '3'
    board[3, 3] = '2'

    assert not board.is_valid()
    assert not board.is_final()

def test_board_is_full_empty():
    board = BoardImpl(2, 2)

    assert not board.is_full()
    assert not board.is_final()

def test_board_is_full_partially_empty():
    board = BoardImpl(2, 2)

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

def test_board_is_full_full():
    board = BoardImpl(2, 2)

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
