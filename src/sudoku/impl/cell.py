from sudoku.exceptions import SymbolNotPossible

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

    def iterate_groups(self):
        """
        :return: An iterator over all the groups this cell is part of.
        :rtype: iterable of :class:`CellGroup`-s
        """
        return (group for group in self._groups)

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
