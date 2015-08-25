from itertools import chain, imap, product, ifilter
from operator import and_

from sudoku.exceptions import InvalidAlphabet, NoPossibleSymbols
from sudoku.impl import Cell, CellGroup

__author__ = "Eli Daian <elidaian@gmail.com>"


class BoardImpl(object):
    """
    A full implementation of a sudoku board.
    """

    def __init__(self, block_width, block_height, alphabet):
        """
        Create an empty board with the given dimensions.
        :param block_width: The block width of the board.
        :type block_width: int
        :param block_height: The block height of the board.
        :type block_height: int
        :param alphabet: The possible symbols in the board.
        :type alphabet: str
        """

        self._block_width = block_width
        self._block_height = block_height
        self._alphabet = alphabet

        if len(alphabet) != self.rows:
            raise InvalidAlphabet("Alphabet length mismatch")

        # Create the board cells
        self._cells = [[Cell(x, y, self._alphabet) for y in xrange(self.cols)] for x in xrange(self.rows)]

        # Create the board groups
        self._groups = []
        self._init_groups()

    def _init_groups(self):
        """
        Initialize the groups for this board.
        """
        # A group for each row
        for r in xrange(self.rows):
            cells = set(self._cells[r])
            self._groups.append(CellGroup(cells))

        # A group for each column
        for c in xrange(self.cols):
            cells = set(self._cells[r][c] for r in xrange(self.rows))
            self._groups.append(CellGroup(cells))

        # A group for each block
        for block_r in xrange(self.block_rows):
            base_r = block_r * self.block_height
            for block_c in xrange(self.block_cols):
                base_c = block_c * self.block_width
                cells = set()
                for r in xrange(base_r, base_r + self.block_height):
                    for c in xrange(base_c, base_c + self.block_width):
                        cells.add(self._cells[r][c])
                self._groups.append(CellGroup(cells))

    @property
    def block_height(self):
        """
        :return: The block height.
        :rtype: int
        """
        return self._block_height

    @property
    def block_width(self):
        """
        :return: The block width.
        :rtype: int
        """
        return self._block_width

    @property
    def rows(self):
        """
        :return: The number of rows in the board.
        :rtype: int
        """
        return self.block_width * self.block_height

    @property
    def cols(self):
        """
        :return: The number of columns in the board.
        :rtype: int
        """
        return self.rows  # A board is quadratic

    @property
    def block_rows(self):
        """
        :return: The number of rows of blocks in this board.
        :rtype: int
        """
        return self.rows / self.block_height

    @property
    def block_cols(self):
        """
        :return: The number of columns of blocks in this board.
        :rtype: int
        """
        return self.cols / self.block_width

    def _iter_cells(self):
        """
        :return: An iterable over all the cells in this board.
        :rtype: iterable of :class:`Cell`-s.
        """
        return chain.from_iterable(self._cells)

    def _iter_empty_cells(self):
        """
        :return: An iterable over all the cells with no assigned symbol.
        :rtype: iterable of :class:`Cell`-s
        """
        return ifilter(lambda cell: cell.symbol is None, self._iter_cells())

    def is_valid(self):
        """
        :return: ``True`` iff the assigned symbol of all cells is valid.
        :rtype: bool
        """
        for group in self._groups:
            if not group.is_valid():
                return False
        return True

    def is_full(self):
        """
        :return: ``True`` iff all cells have assigned symbol.
        :rtype: bool
        """
        return reduce(and_, imap(lambda x: bool(x.symbol), self._iter_cells()), True)

    def is_empty(self):
        """
        :return: ``True`` iff all cells do not have assigned symbol.
        :rtype: bool
        """
        return reduce(and_, imap(lambda x: x.symbol is None, self._iter_cells()), True)

    def _fill_one_possible(self):
        """
        Fill cells with a single possible value.
        :return: ``True`` iff a change to the board was done.
        :rtype: bool
        """

        changed = False

        for cell in self._iter_empty_cells():
            num_possible_symbols = cell.get_num_possible_symbols()
            if num_possible_symbols == 1:
                cell.set_symbol(cell.get_possible_symbol())
                changed = True
            elif num_possible_symbols <= 0:
                raise NoPossibleSymbols("Cell has no possible symbols")

        return changed

    def _split_groups(self):
        """
        Split groups where possible.

        A group of size $n$ can be split if there is a subgroup of size $0 < k < n$ cells in this group, such that
        these cells have the same $k$ possible symbols. In this case, this group can be considered as two different
        groups. The subgroup with a possible alphabet of the $k$ symbols, and the complementary subgroup.
        :return: ``True`` iff a change to the board was done.
        :rtype: bool
        """

        changed = False

        groups = list(self._groups)
        for group in groups:
            possibles_to_cells = group.create_possible_symbols_to_cells_mapping()
            if len(possibles_to_cells) == 1:
                continue

            for possible_symbols, cells in possibles_to_cells.iteritems():
                if len(possible_symbols) == len(cells):
                    changed = True

                    # Create the new subgroup
                    new_group = CellGroup(cells)
                    self._groups.append(new_group)

                    # Remove all cells from the old group, and remove the old group
                    new_group.remove_as_subgroup(self._groups)

                    # Cannot split this group into more groups, go to the next group
                    break

        return changed

    def _remove_assigned_from_groups(self):
        """
        Remove cells with assigned values from the groups.
        :return: ``True`` iff a change has been done.
        :rtype: bool
        """
        changed = False
        for group in self._groups:
            changed = group.remove_assigned_cells() or changed
        return changed

    def _remove_from_other_groups(self):
        """
        If a symbol is possible in only $n$ cells of a group, and all these $n$ cells are also a part of another group,
        this symbol should not be possible in any other cell of the other group.
        :return: ``True`` iff a change has been done.
        :rtype: bool
        """
        changed = False

        for group in self._groups:
            symbols_to_cells = group.create_symbol_to_possible_cell_mapping()
            for symbol, cells in symbols_to_cells.iteritems():
                if len(cells) == 1:
                    cells.pop().set_symbol(symbol)
                    changed = True
                    break

                for other_group in self._groups:
                    if group is other_group:
                        # This is not interesting
                        continue

                    if cells.issubset(other_group.cells):
                        for cell in other_group.iterate_empty_cells():
                            if cell in cells:
                                continue
                            if symbol in cell.get_possible_symbols():
                                cell.remove_possible_symbol(symbol)
                                changed = True

        return changed

    def _remove_empty_groups(self):
        """
        Remove empty groups from this board.
        """
        groups = list(self._groups)
        for group in groups:
            if len(group) == 0:
                self._groups.remove(group)

    def solve_possible(self):
        """
        Fill the board with the possible assignments, without guessing the solution.
        An exception will be raised if there is a cell with no possible symbol to fill with.
        """
        changed = True
        while changed:
            changed = self._fill_one_possible()
            if not changed:
                changed = self._split_groups()
            if not changed:
                changed = self._remove_assigned_from_groups()
            if not changed:
                changed = self._remove_from_other_groups()
            self._remove_empty_groups()

    def is_final(self):
        """
        :return: ``True`` iff all cells have assigned symbol and their assigned symbols are valid togethoer.
        :rtype: bool
        """
        return self.is_full() and self.is_valid()

    def __setitem__(self, pos, symbol):
        """
        Set the value of a cell in the board.
        :param pos: The position of the cell in the board.
        :type pos: tuple of ints
        :param symbol: The new symbol value.
        :type symbol: str
        """
        row, col = pos
        self._cells[row][col].set_symbol(symbol)

    def __getitem__(self, pos):
        """
        Get the value of a cell, or ``None`` if the cell has no symbol assigned.
        :param pos: The position of the cell in the board.
        :type pos: tuple of ints
        :return: The cell symbol value.
        :rtype: str or None
        """
        row, col = pos
        return self._cells[row][col].symbol

    def get_num_possible_symbols(self, row, col):
        """
        Get the number of possible symbols in a given cell.
        :param row: The cell row.
        :type row: int
        :param col: The cell column.
        :type col: int
        :return: The number of possible symbols in this cell.
        :rtype: int
        """
        return self._cells[row][col].get_num_possible_symbols()

    def get_possible_symbols(self, row, col):
        """
        Get the possible symbols in a given cell.
        :param row: The cell row.
        :type row: int
        :param col: The cell column.
        :type col: int
        :return: The possible symbol in this cell.
        :rtype: set
        """
        return self._cells[row][col].get_possible_symbols()

    def copy(self):
        """
        :return: A new :class:`BoardImpl` object, that is an exact copy of this object.
        :rtype: :class:`BoardImpl`
        """

        board = BoardImpl(self._block_width, self._block_height, self._alphabet)
        for cell in self._iter_cells():
            if cell.symbol:
                board[cell.x, cell.y] = cell.symbol
        return board

    def __str__(self):
        """
        :return: A string representing this board, with spaces in the unknown cells. The entire board will be returned
            as a single line string, with no spaces between the lines and blocks.
        :rtype: str
        """
        return "".join(cell.symbol or " " for cell in self._iter_cells())

    def get_empty_cells_positions(self):
        """
        :return: A list of positions of cells without an assigned symbol.
        :rtype: set of tuples
        """
        return [(row, col) for row, col in product(xrange(self.rows), xrange(self.cols))
                if not self._cells[row][col].symbol]
