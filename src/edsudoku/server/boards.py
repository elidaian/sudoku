from datetime import datetime

from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, Text

from edsudoku.board import Board
from edsudoku.server.database import Base

__author__ = 'Eli Daian <elidaian@gmail.com>'


class DBBoard(Base):
    """
    Boards representation in the DB.

    :cvar ~edsudoku.server.boards.DBBoard.id: The board ID in the DB.
    :vartype ~edsudoku.server.boards.DBBoard.id: int
    :cvar user_id: The ID of the owner of this board.
    :vartype user_id: int
    :cvar user: The owner of this board.
    :vartype user: :class:`~edsudoku.server.users.User`
    :cvar create_time: The creation time of this board.
    :vartype create_time: :class:`datetime.datetime`
    :cvar ~edsudoku.server.boards.DBBoard.block_width: The block width in this board.
    :vartype ~edsudoku.server.boards.DBBoard.block_width: int
    :cvar ~edsudoku.server.boards.DBBoard.block_height: The block height in this board.
    :vartype ~edsudoku.server.boards.DBBoard.block_height: int
    :cvar _problem: A representation of the problem of this board.
    :vartype _problem: str
    :cvar _solution: A representation of the solution of this board, or ``None`` if not available.
    :vartype _solution: str
    """

    __tablename__ = 'boards'

    #: The board ID in the DB.
    id = Column(Integer, primary_key=True)

    #: The ID of the owner of this board.
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    #: The owner of this board.
    user = relationship('User', backref=backref('boards', cascade='all, delete, delete-orphan'))

    #: The creation time of this board.
    create_time = Column(DateTime, nullable=False, default=datetime.now)

    #: The block width in this board.
    block_width = Column(Integer, nullable=False)

    #: The block height in the board.
    block_height = Column(Integer, nullable=False)

    #: A representation of the problem of this board.
    _problem = Column(Text, nullable=False)

    #: A representation of the solution of this board, or ``None`` if not available.
    _solution = Column(Text)

    @staticmethod
    def create_board(user, board):
        """
        Create a new board, and add it to the DB.

        :param user: The owner of this board.
        :type user: :class:`~edsudoku.server.users.User`
        :param board: The board itself.
        :type board: :class:`~edsudoku.board.Board`
        :return: The created board in the DB.
        :rtype: :class:`~edsudoku.server.boards.DBBoard`
        """
        db_board = DBBoard(user=user, block_width=board.block_width, block_height=board.block_height,
                           _problem=str(board.problem), _solution=str(board.solution))
        db_board.add()
        return db_board

    @property
    def board(self):
        """
        :return: A ``edsudoku`` style board.
        :rtype: :class:`~edsudoku.board.Board`
        """
        return Board.from_strings(self.block_width, self.block_height, self._problem, self._solution)
