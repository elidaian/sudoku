from sudoku.impl import Cell, CellGroup

__author__ = 'Eli Daian <elidaian@gmail.com>'


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


def test_cell_group_is_valid_no_empty_valid(alphabet10):
    cells = [Cell(0, y, alphabet10, str(y)) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.is_valid()


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


def test_cell_group_contains_cells_true_all(alphabet10):
    cells = set([Cell(0, y, alphabet10) for y in xrange(10)])
    group = CellGroup(set(cells))

    assert group.contains_cells(cells)


def test_cell_group_contains_cells_true_part(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert group.contains_cells(set(cells[2:5]))


def test_cell_group_contains_cells_false(alphabet10):
    cells = [Cell(0, y, alphabet10) for y in xrange(10)]
    group = CellGroup(set(cells))

    assert not group.contains_cells(set([Cell(x, 0, alphabet10) for x in xrange(10)]))


def test_cell_group_contains_cells_false_addition(alphabet10):
    cells = set([Cell(0, y, alphabet10) for y in xrange(10)])
    group = CellGroup(set(cells))
    cells.add(Cell(1, 0, alphabet10))

    assert not group.contains_cells(cells)

# def test_cell_group_is_valid_partially_empty_invalid(alphabet10):
#     cells = [Cell(0, y, alphabet10) for y in xrange(10)]
#     group = CellGroup(set(cells))
#
#     cells[0].set_symbol('0')
#     cells[1].set_symbol('1')
#     cells[5].set_symbol('0')
#
#     assert not group.is_valid()


# def test_cell_group_is_valid_no_empty_invalid(alphabet10):
#     cells = [Cell(0, y, alphabet10, str(y)) for y in xrange(10)]
#     group = CellGroup(set(cells))
#
#     cells[4].set_symbol('5')
#
#     assert not group.is_valid()
