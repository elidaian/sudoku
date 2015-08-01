'''
Provides implementation for internal board, cell, etc.
'''
from operator import and_

__author__ = 'Eli Daian <elidaian@gmail.com>'


class Cell(object):
    '''
    A sudoku board cell.
    '''

    def __init__(self, x, y, symbol=None):
        '''
        Create a new cell.
        :param x: The X coordinate of this cell.
        :type x: int
        :param y: The Y coordinate of this cell.
        :type y: int
        :param symbol: The cell value, or ``None`` if unknown.
        :type symbol: str or None
        '''
        self.x = x
        self.y = y
        self.symbol = symbol

    def __repr__(self):
        '''
        :return: A readable representation of this cell.
        :rtype: str
        '''
        return 'Cell at <%d, %d> with value \'%s\'' % (self.x, self.y, self.symbol)

    def set_symbol(self, symbol):
        '''
        Set a new symbol.
        :param symbol: The new symbol, or ``None``.
        :type symbol: str
        '''
        self.symbol = symbol

    def is_empty(self):
        '''
        :return: ``True`` iff this cell has no assigned symbol.
        :rtype: bool
        '''
        return self.symbol is None


class CellGroup(object):
    '''
    A group of cells, in which two cells cannot have the same value.
    '''

    def __init__(self, cells=None):
        '''
        Initialize this cell group.
        :param cells: The cells in this group, or ``None`` if unknown.
        :type cells: set of Cell
        '''
        self._cells = cells or set()

    def add(self, cell):
        '''
        Add a cell to this cell group.
        :param cell: The cell to add.
        :type cell: Cell
        '''
        self._cells.add(cell)

    def is_valid(self):
        '''
        :return: ``True`` iff there are no two cells in this group with the same symbol.
        :rtype: bool
        '''

        seen_symbols = set()

        for cell in self._cells:
            if cell.symbol:
                if cell.symbol in seen_symbols:
                    return False
                seen_symbols.add(cell.symbol)

        return True


class BoardImpl(object):
    '''
    A full implementation of a sudoku board.
    '''

    def __init__(self, block_width, block_height):
        '''
        Create an empty board with the given dimensions.
        :param block_width: The block width of the board.
        :type block_width: int
        :param block_height: The block height of the board.
        :type block_height: int
        '''

        self._block_width = block_width
        self._block_height = block_height

        # Create the board cells
        self._cells = [[Cell(x, y) for y in xrange(self.cols)] for x in xrange(self.rows)]

        # Create the board groups
        self._groups = []
        self._init_groups()

    def _init_groups(self):
        '''
        Initialize the groups for this board.
        '''
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
        '''
        :return: The block height.
        :rtype: int
        '''
        return self._block_height

    @property
    def block_width(self):
        '''
        :return: The block width.
        :rtype: int
        '''
        return self._block_width

    @property
    def rows(self):
        '''
        :return: The number of rows in the board.
        :rtype: int
        '''
        return self.block_width * self.block_width

    @property
    def cols(self):
        '''
        :return: The number of columns in the board.
        :rtype: int
        '''
        return self.rows  # A board is quadratic

    @property
    def block_rows(self):
        '''
        :return: The number of rows of blocks in this board.
        :rtype: int
        '''
        return self.rows / self.block_height

    @property
    def block_cols(self):
        '''
        :return: The number of columns of blocks in this board.
        :rtype: int
        '''
        return self.cols / self.block_width

    def is_valid(self):
        '''
        :return: ``True`` iff the assigned symbol of all cells is valid.
        :rtype: bool
        '''
        for group in self._groups:
            if not group.is_valid():
                return False
        return True

    def is_full(self):
        '''
        :return: ``True`` iff all cells have assigned symbol.
        :rtype: bool
        '''
        for cells_row in self._cells:
            for cell in cells_row:
                if not cell.symbol:
                    return False
        return True

    def is_final(self):
        '''
        :return: ``True`` iff all cells have assigned symbol and their assigned symbols are valid togethoer.
        :rtype: bool
        '''
        return self.is_full() and self.is_valid()

    def __setitem__(self, pos, symbol):
        '''
        Set the value of a cell in the board.
        :param pos: The position of the cell in the board.
        :type pos: tuple of ints
        :param symbol: The new symbol value.
        :type symbol: str
        '''
        row, col = pos
        self._cells[row][col].set_symbol(symbol)

    def __getitem__(self, pos):
        '''
        Get the value of a cell, or ``None`` if the cell has no symbol assigned.
        :param pos: The position of the cell in the board.
        :type pos: tuple of ints
        :return: The cell symbol value.
        :rtype: str or None
        '''
        row, col = pos
        return self._cells[row][col].symbol
