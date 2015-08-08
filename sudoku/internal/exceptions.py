__author__ = "Eli Daian <elidaian@gmail.com>"


class SymbolNotPossible(ValueError):
    """
    This exception is raised when a symbol is being assigned to a cell, but this symbol cannot
    be assigned to this cell.
    """
    pass
