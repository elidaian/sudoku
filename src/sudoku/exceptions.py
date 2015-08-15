__author__ = "Eli Daian <elidaian@gmail.com>"


class SymbolNotPossible(ValueError):
    """
    This exception is raised when a symbol is being assigned to a cell, but this symbol cannot
    be assigned to this cell.
    """
    pass


class NoPossibleSymbols(ValueError):
    """
    This exception is raised when a board is trying to get solved, but there is at least one cell
    with no possible symbols to assign in it.
    """
    pass


class InvalidAlphabet(ValueError):
    """
    This exception is raised when the given alphabet is invalid.

    Usually, this means that the alphabet length does not match the board dimensions.
    """
    pass


class IllegalAlphabet(Exception):
    """
    This exception is raised when the alphabet of a cell is reset with an invalid new alphabet.
    """
    pass


class ErrorWithMessage(Exception):
    """
    This exception is raised inside the server.

    It contains a message that should be sent to the client.
    """
    pass
