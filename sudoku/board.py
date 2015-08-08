__author__ = "Eli Daian <elidaian@gmail.com>"


class SimpleBoard(object):
    """
    Represents a sudoku board.

    This board is a simple board - a problem or solution board.
    """

    def __init__(self, block_width, block_height, data=None):
        """
        Create a new sudoku board.

        :param block_width: The block width in the board.
        :type block_width: int
        :param block_height: The block height in the board.
        :type block_height: int
        :param data: The board data, or ``None`` for an empty board.
        :type data: str
        """
        self._block_width = block_width
        self._block_height = block_height
        self._data = data or (" " * (block_width * block_width * block_height * block_height))

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
        return self.block_width * self.block_width

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

    def _get_index(self, row, col):
        """
        Get the index of a cell in the board, given its row and column.
        :param row: The row of the cell.
        :type row: int
        :param col: The column of the cell.
        :type col: int
        :return: The index inside ``self._data``.
        :rtype: int
        """
        return row * self.cols + col

    def __getitem__(self, pos):
        """
        Get a board cell.
        :param pos: The cell coordinates.
        :type pos: tuple of strings
        :return: The cell data.
        :rtype: str
        """
        row, col = pos
        return self._data[self._get_index(row, col)]

    def __setitem__(self, pos, value):
        """
        Set a board cell.
        :param pos: The cell coordinates.
        :type pos: tuple of strings
        :param value: The new cell value.
        :type value: str
        :return: The new cell value.
        :rtype: str
        """
        row, col = pos
        self._data[self._get_index(row, col)] = value
        return value

    def __repr__(self):
        """
        :return: The board representation.
        :rtype: str
        """

        # Define the separators
        vsep = "-"
        hsep = "|"

        # Build the board
        board_list = [[self[r, c] for c in xrange(self.cols)] for r in xrange(self.rows)]
        return vsep.join([hsep.join(row) for row in board_list])


class Board(object):
    """
    Represents a sudoku board, with a problem and solution.
    """

    DIMENSION_MISMATCH_ERROR = "Dimension mismatch"

    def __init__(self, block_width, block_height, problem, solution=None):
        """
        Create a new sudoku board with problem and solution.

        :param block_width: The block width in the board.
        :type block_width: int
        :param block_height: The block height in the board.
        :type block_height: int
        :param problem: The board problem.
        :type problem: SimpleBoard
        :param solution: The board solution, or ``None`` if unknown.
        :type solution: SimpleBoard
        """
        assert problem.block_width == block_width, self.DIMENSION_MISMATCH_ERROR
        assert problem.block_height == block_height, self.DIMENSION_MISMATCH_ERROR
        assert solution is None or solution.block_width == block_height, self.DIMENSION_MISMATCH_ERROR
        assert solution is None or solution.block_height == block_height, self.DIMENSION_MISMATCH_ERROR

        self._block_width = block_width
        self._block_height = block_height
        self._problem = problem
        self._solution = solution or problem

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
        return self.block_width * self.block_width

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

    @property
    def problem(self):
        """
        :return: The problem board.
        :rtype: SimpleBoard
        """
        return self._problem

    @property
    def solution(self):
        """
        :return: The solution board.
        :rtype: SimpleBoard
        """
        return self._solution
