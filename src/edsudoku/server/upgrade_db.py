from argparse import ArgumentParser
from datetime import datetime
from itertools import izip
import sqlite3

from sqlalchemy.engine import create_engine

from sqlalchemy.orm.session import sessionmaker

from edsudoku.server.boards import DBBoard
from edsudoku.server.database import Base
from edsudoku.server.users import User

__author__ = 'Eli Daian <elidaian@gmail.com>'


def _parse_args():
    """
    Parse command line arguments.

    :return: The parsed arguments.
    :rtype: :class:`argparse.Namespace`
    """

    parser = ArgumentParser(description='Upgrade an old DB to a new one')
    parser.add_argument('-i', '--old-db',
                        required=True,
                        metavar='FILE',
                        dest='old',
                        help='Old DB filename')
    parser.add_argument('-o', '--new-db',
                        required=True,
                        metavar='DB STRING',
                        dest='new',
                        help='New DB connection string')
    parser.add_argument('-d', '--drop-new',
                        action='store_true',
                        dest='drop',
                        help='Use for dropping all information in the new DB (if exist)')
    return parser.parse_args()


def _read_old_db(filename):
    """
    Read the old DB.

    :param filename: The old DB filename.
    :type filename: str
    :return: The list of users, and the list of boards.
    :rtype: tuple
    """

    conn = sqlite3.connect(filename)
    try:
        conn.row_factory = sqlite3.Row
        users = [dict(izip(row.keys(), row)) for row in conn.execute('SELECT * FROM users')]
        boards = [dict(izip(row.keys(), row)) for row in conn.execute('SELECT * FROM boards')]
        return users, boards
    finally:
        conn.close()


def _create_new_db(users, boards, connection_string, drop):
    """
    Fill the new DB with the data.

    :param users: The users to insert.
    :type users: list
    :param boards: The boards to insert.
    :type boards: list
    :param connection_string:
    :type connection_string:
    :param drop: If ``True``, the new DB will be dropped before filled.
    :type drop: bool
    """

    engine = create_engine(connection_string, convert_unicode=True)
    Session = sessionmaker(bind=engine)

    if drop:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session()
    try:
        # Add the users
        for user in users:
            session.add(User(id=user['id'], username=user['username'], _password=user['password'], _salt=None,
                             _display=user['display'], permissions_mask=user['permissions']))
        session.commit()

        # Add the boards
        for board in boards:
            create_time = datetime.strptime(board['create_time'], '%Y-%m-%d %H:%M:%S')
            session.add(DBBoard(id=board['id'], user_id=board['uid'], create_time=create_time,
                                block_width=board['block_width'], block_height=board['block_height'],
                                _problem=board['problem'], _solution=board['solution']))
        session.commit()
    finally:
        session.close()


def main():
    """
    Main entry point for this script.
    """
    args = _parse_args()
    users, boards = _read_old_db(args.old)
    _create_new_db(users, boards, args.new, args.drop)


if __name__ == '__main__':
    main()
