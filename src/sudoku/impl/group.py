from itertools import ifilter

__author__ = "Eli Daian <elidaian@gmail.com>"


class CellGroup(object):
    """
    A group of cells, in which two cells cannot have the same value.
    """

    def __init__(self, cells=None):
        """
        Initialize this cell group.
        :param cells: The cells in this group, or ``None`` if unknown.
        :type cells: set of sudoku.impl.cell.Cell
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
        :type cell: sudoku.impl.cell.Cell
        """
        self._cells.add(cell)
        cell.add_group(self)
        self.update_taken_symbols()
        self.update_possible_symbols()

    def iterate_cells(self):
        """
        :return: An iterable over all cells in this group.
        :rtype: iterable of :class:`Cell`-s
        """
        return (cell for cell in self._cells)

    def iterate_empty_cells(self):
        """
        :return: An iterable over all empty cells in this group.
        :rtype: iterable of :class:`Cell`-s
        """
        return ifilter(lambda cell: cell.symbol is None, self.iterate_cells())

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

    def remove_assigned_cells(self):
        """
        Remove cells that have an assigned symbol from this group.
        :return: ``True`` iff cells were removed from this group.
        :rtype: bool
        """
        cells = list(self._cells)
        for cell in ifilter(lambda cell: cell.symbol is not None, cells):
            cell.remove_group(self)
            self._cells.remove(cell)
            for other_cell in self._cells:
                alphabet = set(other_cell.alphabet)
                alphabet.discard(cell.symbol)
                other_cell.reset_alphabet(alphabet)
        return len(cells) != len(self._cells)
