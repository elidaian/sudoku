"""
This module generates sudoku boards.

:var DEFAULT_ALPHABET: The default alphabet used when no alphabet is given for generating the board.
:type DEFAULT_ALPHABET: str
"""
from random import choice

from exceptions import NoPossibleSymbols
from sudoku.impl.board import BoardImpl

__author__ = "Eli Daian <elidaian@gmail.com>"

from board import Board, SimpleBoard

DEFAULT_ALPHABET = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
""" Default alphabet to be used if no alphabet is given. """


def _find_next_symbol_to_assign(board, possible_positions):
    """
    Find an empty cell in the board, and generate a random symbol to assign in it.
    :param board: The board.
    :type board: :class:`~impl.BoardImpl`
    :param possible_positions: The possible locations for assignment.
    :type possible_positions: list
    :return: A tuple, consisting of the cell position (another tuple) and the symbol to assign in it.
    :rtype: tuple
    """

    # Find the position for assigning
    pos = choice(possible_positions)

    # Select a symbol to assign
    symbol = choice(list(board.get_possible_symbols(*pos)))
    return pos, symbol


def _construct_assignments(block_width, block_height, alphabet):
    """
    Construct a series of assignments in the board, for generating a problem that is solvable
    to a full solution.

    This function returns a list of tuples, each tuple consisting of a cell position (a tuple itself),
    and the symbol assigned to this cell.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board.
    :type alphabet: str
    :return: As explained above.
    :rtype: list
    """

    # Maximal number of failures from a clean board
    MAX_TRIALS = 10

    # Initialize parameters for the loop
    solution = BoardImpl(block_width, block_height, alphabet)
    trials = 0
    assignments = []
    possible_positions = solution.get_empty_cells_positions()


    # Main loop for assigning values
    while not solution.is_final():
        problem = solution

        pos, symbol = _find_next_symbol_to_assign(problem, possible_positions)
        problem_with_assignment = problem.copy()
        problem_with_assignment[pos] = symbol

        solution = problem_with_assignment.copy()
        try:
            solution.solve_possible()
        except NoPossibleSymbols:  # No possible solution for this board with this assignment
            if trials < MAX_TRIALS and len(possible_positions) > 1:
                # Roll back this assignment, there are more assignments to try
                solution = problem
                trials += 1
                possible_positions.remove(pos)
            else:
                # Roll back all assignments, create with a clean board
                solution = BoardImpl(block_width, block_height, alphabet)
                trials = 0
                assignments = []
                possible_positions = solution.get_empty_cells_positions()
        else:
            # Board is still solvable
            assignments.append((pos, symbol))
            possible_positions = solution.get_empty_cells_positions()

    return assignments


def _construct_from_assignments(block_width, block_height, alphabet, assignments):
    """
    Construct a board from a series of assignments.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board.
    :type alphabet: str
    :param assignments: The assignments series, as returned from :meth:`__construct_assignments`.
    :type assignments: list
    :return: The constructed board.
    :rtype: :class:`~impl.BoardImpl`.
    """
    board = BoardImpl(block_width, block_height, alphabet)
    for pos, symbol in assignments:
        board[pos] = symbol
    return board


def _remove_unneeded_assignments(block_width, block_height, alphabet, assignments):
    """
    Remove the unneeded assignments from an assignments series.

    An unneeded assignment is an assignment that is not needed for the board to remain solvable.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board.
    :type alphabet: str
    :param assignments: The assignments series, as returned from :meth:`__construct_assignments`.
    :type assignments: list
    :return: The assignments with the unneeded assignments removed.
    :rtype: list
    """

    i = 0
    pure_assignments = list(assignments)

    while i < len(pure_assignments):
        without = pure_assignments[:i] + pure_assignments[i + 1:]
        board = _construct_from_assignments(block_width, block_height, alphabet, without)
        board.solve_possible()

        if board.is_final():
            # This assignment is not needed
            pure_assignments.pop(i)
        else:
            # This assignment is needed
            i += 1

    return pure_assignments


def _construct_board(block_width, block_height, alphabet):
    """
    Construct a new board, that consists of a problem ans solution.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board.
    :type alphabet: str
    :return: A tuple of the problem and solution board strings.
    :rtype: tuple of str-s.
    """

    # Create assignments series
    assignments = _construct_assignments(block_width, block_height, alphabet)

    # Removed unnecessary assignments from this list
    pure_assignments = _remove_unneeded_assignments(block_width, block_height, alphabet, assignments)

    # Generate the problem ans solution
    problem = _construct_from_assignments(block_width, block_height, alphabet, pure_assignments)
    solution = problem.copy()
    solution.solve_possible()
    assert solution.is_final(), "Cannot solve problem, this is a BUG"

    return str(problem), str(solution)


def generate(block_width, block_height, alphabet=None):
    """
    Generate a new sudoku board.
    :param block_width: The block width in the board.
    :type block_width: int
    :param block_height: The block height in the board.
    :type block_height: int
    :param alphabet: The symbols for use in the board, or ``None`` for the default.
    :type alphabet: str
    :return: The generated board.
    :rtype: Board
    """

    board_size = block_height * block_width

    if alphabet is None:
        if board_size > len(DEFAULT_ALPHABET):
            raise IndexError, "Board too long for default alphabet"
        alphabet = DEFAULT_ALPHABET[:board_size]

    problem, solution = _construct_board(block_width, block_height, alphabet)

    problem_board = SimpleBoard(block_width, block_height, problem)
    solution_board = SimpleBoard(block_width, block_height, solution)
    return Board(block_width, block_height, problem_board, solution_board)
