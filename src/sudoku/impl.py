"""
Provides implementation for internal board, cell, etc.
"""
from itertools import chain, imap
from operator import and_

from exceptions import SymbolNotPossible, NoPossibleSymbols, InvalidAlphabet

__author__ = "Eli Daian <elidaian@gmail.com>"


class Cell(object):
    """
    A sudoku board cell.
    """

    def __init__(self, x, y, alphabet, symbol=None):
        """
        Create a new cell.
        :param x: The X coordinate of this cell.
        :type x: int
        :param y: The Y coordinate of this cell.
        :type y: int
        :param alphabet: The possible symbols in the board.
        :type alphabet: str
        :param symbol: The cell value, or ``None`` if unknown.
        :type symbol: str or None
        """
        self.x = x
        self.y = y
        self.alphabet = alphabet
        self.symbol = symbol

        self._groups = []
        self._possible_symbols = set(alphabet)

        if symbol:
            if symbol not in alphabet:
                raise SymbolNotPossible("Illegal symbol given")
            self._possible_symbols.remove(symbol)

    def __repr__(self):
        """
        :return: A readable representation of this cell.
        :rtype: str
        """
        return "Cell at <%d, %d> with value \"%s\"" % (self.x, self.y, self.symbol)

    def set_symbol(self, symbol):
        """
        Set a new symbol.
        :param symbol: The new symbol, or ``None``.
        :type symbol: str
        """

        if symbol == self.symbol:
            return

        if symbol is not None and symbol not in self._possible_symbols:
            raise SymbolNotPossible("Illegal symbol given")
        self.symbol = symbol

        for group in self._groups:
            group.update_taken_symbols()
        for group in self._groups:
            group.update_possible_symbols()

    def add_group(self, group):
        """
        Add this cell to a group.
        :param group: The group this cell is now part of.
        :type group: CellGroup
        """
        self._groups.append(group)

    def update_possible_symbols(self):
        """
        Update the possible symbols for this cell, looking at the taken symbols
        in all other groups.
        """

        taken_symbols = set()
        possible_symbols = set(self.alphabet)

        # Look at the taken symbols
        for group in self._groups:
            taken_symbols = taken_symbols.union(group.taken_symbols())

        self._possible_symbols = possible_symbols.difference(taken_symbols)

    def get_possible_symbols(self):
        """
        Get the set of possible symbols for this cell.
        :note: The set of possible symbols might not be up to date.
        :return: The set of possible symbols for this cell.
        :rtype: set of string
        """
        return self._possible_symbols

    def get_num_possible_symbols(self):
        """
        :return: The number of possible symbols for this cell.
        :rtype: int
        """
        return len(self._possible_symbols)

    def get_possible_symbol(self):
        """
        Get the only possible symbol for this cell. If more than one symbol is
        possible, an exception will be raised.
        :return: The only possible symbol.
        :rtype: str
        """
        assert len(self._possible_symbols) == 1, "There is more than one possible symbol"
        for symbol in self._possible_symbols:
            return symbol

    def is_empty(self):
        """
        :return: ``True`` iff this cell has no assigned symbol.
        :rtype: bool
        """
        return self.symbol is None


class CellGroup(object):
    """
    A group of cells, in which two cells cannot have the same value.
    """

    def __init__(self, cells=None):
        """
        Initialize this cell group.
        :param cells: The cells in this group, or ``None`` if unknown.
        :type cells: set of Cell
        """
        self._cells = cells or set()
        for cell in self._cells:
            cell.add_group(self)
        self.update_taken_symbols()
        self.update_possible_symbols()

    def add(self, cell):
        """
        Add a cell to this cell group.
        :param cell: The cell to add.
        :type cell: Cell
        """
        self._cells.add(cell)
        cell.add_group(self)
        self.update_taken_symbols()
        self.update_possible_symbols()

    def is_valid(self):
        """
        :return: ``True`` iff there are no two cells in this group with the same symbol.
        :rtype: bool
        """

        seen_symbols = set()

        for cell in self._cells:
            if cell.symbol:
                if cell.symbol in seen_symbols:
                    return False
                seen_symbols.add(cell.symbol)

        return True

    def taken_symbols(self):
        """
        :return: A set of the taken symbols in this cell group.
        :rtype: set of strings.
        """

        return self._taken_symbols

    def update_taken_symbols(self):
        """
        Update the set of taken symbols in this cell group.
        """
        self._taken_symbols = set(cell.symbol for cell in self._cells if cell.symbol)

    def update_possible_symbols(self):
        """
        Update the possible symbols of each cell in this cell group.
        """
        for cell in self._cells:
            cell.update_possible_symbols()


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

    def solve_possible(self):
        """
        Fill the cells with only one single possible symbol.
        An exception will be raised if there is a cell with no possible symbol to fill with.
        """
        changed = True
        while changed:
            changed = False
            for cell in self._iter_cells():
                if cell.symbol:
                    continue

                num_possible_symbols = cell.get_num_possible_symbols()
                if num_possible_symbols == 1:
                    cell.set_symbol(cell.get_possible_symbol())
                    changed = True
                elif num_possible_symbols <= 0:
                    raise NoPossibleSymbols("Cell has no possible symbols")

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
