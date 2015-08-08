__author__ = "Eli Daian <elidaian@gmail.com>"


def _assign_board_from_generated_board(board, board_impl):
    """
    Assign the data from a board into board_impl.
    :param board: The input board.
    :type board: :class:`~board.Board`
    :param board_impl: The output board.
    :type board_impl: :class:`~internal.impl.BoardImpl`
    """
    assert board.block_width == board_impl.block_width
    assert board.block_height == board.block_height

    for row in xrange(board.rows):
        for col in xrange(board.cols):
            if board[row, col] != " ":
                board_impl[row, col] = board[row, col]


def test_generator_solution_of_problem(generated_board):
    """
    Test that a generated board has a solution for the problem.
    """
    for row in xrange(generated_board.rows):
        for col in xrange(generated_board.cols):
            if generated_board.problem[row, col] != " ":
                assert generated_board.problem[row, col] == generated_board.solution[row, col]


def test_generator_solvable(generated_board, board):
    """
    Test that a generated board is solvable, and that the solution is the returned solution.
    """

    _assign_board_from_generated_board(generated_board.problem, board)
    board.solve_possible()

    assert board.is_final()
    for row in xrange(generated_board.rows):
        for col in xrange(generated_board.cols):
            assert board[row, col] == generated_board.solution[row, col]


def test_generator_problem_not_full(generated_board, board):
    """
    Test that the generated problem is not a full board; neither an empty one.
    """
    _assign_board_from_generated_board(generated_board.problem, board)
    assert not board.is_full()
    assert not board.is_empty()
