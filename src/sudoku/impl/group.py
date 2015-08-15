from collections import defaultdict
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

    def __len__(self):
        """
        :return: The number of cells in this group.
        :rtype: int
        """
        return len(self._cells)

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

    def create_possible_symbols_to_cells_mapping(self):
        """
        Create a mapping from ``frozenset``-s of possible symbols to a lists of cells, that these are their possible
        symbols.
        :return: This mapping.
        :rtype: dict
        """
        possibles_to_cells = defaultdict(list)
        for cell in self.iterate_empty_cells():
            possible_symbols = cell.get_possible_symbols()
            possibles_to_cells[frozenset(possible_symbols)].append(cell)
        return possibles_to_cells

    def create_symbol_to_possible_cell_mapping(self):
        """
        Create a mapping from symbols to a list of cells, in which this symbol is a possible assignment.
        :return: This mapping.
        :rtype: dict
        """
        symbols_to_cells = defaultdict(list)
        for cell in self.iterate_empty_cells():
            for symbol in cell.get_possible_symbols():
                symbols_to_cells[symbol].append(cell)
        return symbols_to_cells

    def remove_as_subgroup(self, other_groups):
        """
        Remove this group from other groups, when this group is a subgroup of another group.
        :param other_groups: The other groups, to look for.
        :type other_groups: list of :class:`CellGroup`-s
        """
        symbols_to_exclude = reduce(lambda alphabet, cell: alphabet.union(cell.get_possible_symbols()),
                                    self._cells, set())
        my_cells = set(self._cells)

        for group in other_groups:
            if my_cells.issubset(group._cells) and self is not group:
                # Remove my cells from the other group
                for cell in self._cells:
                    cell.remove_group(group)
                    group._cells.remove(cell)

                # Update the alphabets in the other group
                for cell in group._cells:
                    new_alphabet = set(cell.alphabet).difference(symbols_to_exclude)
                    cell.reset_alphabet(new_alphabet)

                # Update the possible symbols in the other group
                group.update_taken_symbols()
                group.update_possible_symbols()

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

    def contains_cells(self, cells):
        """
        Check if a group of cells is a subgroup of this group.
        :param cells: The group of cells.
        :type cells: list
        :return: ``True`` if the given group of cells is a subgroup of this group.
        :rtype: bool
        """
        return set(self._cells).issuperset(cells)
