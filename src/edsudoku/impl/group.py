from collections import defaultdict
from itertools import ifilter

__author__ = 'Eli Daian <elidaian@gmail.com>'


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
        self.cells = set(cells) or set()
        self._taken_symbols = set()
        for cell in self.cells:
            cell.add_group(self)

    def __len__(self):
        """
        :return: The number of cells in this group.
        :rtype: int
        """
        return len(self.cells)

    def add(self, cell):
        """
        Add a cell to this cell group.

        :param cell: The cell to add.
        :type cell: sudoku.impl.cell.Cell
        """
        self.cells.add(cell)
        cell.add_group(self)

    def iterate_cells(self):
        """
        :return: An iterable over all cells in this group.
        :rtype: iterable of :class:`Cell`-s
        """
        return (cell for cell in self.cells)

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

        for cell in self.cells:
            if cell.symbol:
                if cell.symbol in seen_symbols:
                    return False
                seen_symbols.add(cell.symbol)

        return True

    def take_symbol(self, symbol):
        """
        Take a symbol from all cells in the group.

        :param symbol: The symbol to take.
        :type symbol: str
        """
        if symbol not in self._taken_symbols:
            for cell in self.cells:
                cell.remove_possible_symbol(symbol)
            self._taken_symbols.add(symbol)

    def get_taken_symbols(self):
        """
        :return: The symbols that are already taken in this group.
        :rtype: set
        """
        return self._taken_symbols

    def create_possible_symbols_to_cells_mapping(self):
        """
        Create a mapping from ``frozenset``-s of possible symbols to a lists of cells, that these are their possible
        symbols.

        :return: This mapping.
        :rtype: dict
        """
        possibles_to_cells = defaultdict(set)
        for cell in self.iterate_empty_cells():
            possibles_to_cells[frozenset(cell.get_possible_symbols())].add(cell)
        return possibles_to_cells

    def create_symbol_to_possible_cell_mapping(self):
        """
        Create a mapping from symbols to a list of cells, in which this symbol is a possible assignment.

        :return: This mapping.
        :rtype: dict
        """
        symbols_to_cells = defaultdict(set)
        for cell in self.iterate_empty_cells():
            for symbol in cell.get_possible_symbols():
                symbols_to_cells[symbol].add(cell)
        return symbols_to_cells

    def remove_as_subgroup(self, other_groups):
        """
        Remove this group from other groups, when this group is a subgroup of another group.

        :param other_groups: The other groups, to look for.
        :type other_groups: list of :class:`CellGroup`-s
        """
        symbols_to_exclude = reduce(lambda alphabet, cell: alphabet.union(cell.get_possible_symbols()),
                                    self.cells, set())
        my_cells = set(self.cells)

        for group in other_groups:
            if my_cells.issubset(group.cells) and self is not group:
                # Remove my cells from the other group
                for cell in self.cells:
                    cell.remove_group(group)
                    group.cells.remove(cell)

                # Update the alphabets in the other group
                for cell in group.cells:
                    cell.remove_possible_symbols(symbols_to_exclude)

    def remove_assigned_cells(self):
        """
        Remove cells that have an assigned symbol from this group.

        :return: ``True`` iff cells were removed from this group.
        :rtype: bool
        """
        cells = list(self.cells)
        for cell in ifilter(lambda cell: cell.symbol is not None, cells):
            cell.remove_group(self)
            self.cells.remove(cell)
        return len(cells) != len(self.cells)

    def contains_cells(self, cells):
        """
        Check if a group of cells is a subgroup of this group.

        :param cells: The group of cells.
        :type cells: set
        :return: ``True`` if the given group of cells is a subgroup of this group.
        :rtype: bool
        """
        return cells.issubset(self.cells)
