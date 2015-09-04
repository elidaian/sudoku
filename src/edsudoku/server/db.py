from contextlib import closing
import hashlib
import sqlite3
from edsudoku.board import SimpleBoard, Board
from edsudoku.server.users import User, UserPermission

__author__ = 'Eli Daian <elidaian@gmail.com>'

LOGIN_QUERY = """
select id, display, permissions from users
where username = :username and password = :password
"""

USER_QUERY = """
select username, display, permissions from users
where id = :id
"""

REGISTER_USER = """
insert into users(username, password, display, permissions)
values (:username, :password, :display, :permissions)
"""

LIST_USERS = """
select id, username, display, permissions from users
"""

GET_USER_DETAILS = """
select id, username, display, permissions,
    (select count(*) from boards where uid = users.id) as num_boards from users
where users.id = :user_id
"""

EDIT_USER_WITH_PASSWORD = """
update users
set password = :password,
    display = :display,
    permissions = :permissions
where id = :user_id
"""

EDIT_USER_WITHOUT_PASSWORD = """
update users
set display = :display,
    permissions = :permissions
where id = :user_id
"""

DELETE_USER = """
delete from users
where id = :user_id
"""

DELETE_USER_BOARDS = """
delete from boards
where uid = :user_id
"""

INSERT_BOARD = """
insert into boards(uid, problem, solution, block_width, block_height)
values (:uid, :problem, :solution, :block_width, :block_height)
"""

LIST_USER_BOARDS = """
select id, create_time, block_width, block_height from boards
where uid = :uid
"""

GET_USER_BOARD = """
select problem, solution, block_width, block_height from boards
where id = :id and uid = :uid
"""

LIST_ALL_BOARDS = """
select boards.id, create_time, block_width, block_height, users.username, users.display
from boards join users on boards.uid = users.id
"""

GET_BOARD = """
select problem, solution, block_width, block_height from boards
where id = :id
"""


def connect_db(app):
    """
    Create a new DB connection.

    :param app: The Flask application object.
    :type app: :class:`flask.Flask`
    :return: A DB connection object.
    :rtype: :class:`sqlite3.Connection`
    """
    print 'connecting to %s' % app.config['DATABASE']
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    db.text_factory = str
    return db


def hash_password(password):
    """
    Hash a password to protect it.

    :param password: The password.
    :type password: str
    :return: The hashed password.
    :rtype: buffer
    """
    return buffer(hashlib.sha512(password).digest())


def login(db, username, password):
    """
    Get user information (if available) given the username and password,
    or ``None`` if the login credentials are invalid.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param username: The username.
    :type username: str
    :param password: The password.
    :type password: str
    :return: The user object, or ``None`` if not found.
    :rtype: :class:`~users.User`
    """
    info = {'username': username,
            'password': hash_password(password)}
    cur = db.execute(LOGIN_QUERY, info)
    entry = cur.fetchone()
    if entry is not None:
        return User(entry['id'], username, entry['display'], entry['permissions'])
    else:
        return None


def get_user(db, user_id):
    """
    Get user information (if available) given the user id, or ``None`` if
    this user does not exist.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :return: The user object, or ``None`` if not found.
    :rtype: :class:`~users.User`
    """
    info = {'id': user_id}
    cur = db.execute(USER_QUERY, info)
    entry = cur.fetchone()
    if entry is not None:
        return User(user_id, entry['username'], entry['display'], entry['permissions'])
    else:
        return None


def register_user(db, username, password, display, permissions):
    """
    Register a new user given its details.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param username: The username.
    :type username: str
    :param password: The password.
    :type password: str
    :param display: The user display (nickname).
    :type display: str
    :param permissions: The granted permissions for this user.
    :type permissions: list of :class:`~users.UserPermission`-s
    :return: A string describing the registration status of this user.
    :rtype: str
    """

    try:
        details = {'username': username,
                   'password': hash_password(password),
                   'display': display,
                   'permissions': UserPermission.get_mask(permissions)}
        db.execute(REGISTER_USER, details)
        db.commit()
        return 'User %s successfully created!' % (display if display else username), True
    except sqlite3.IntegrityError:
        return 'Unable to register %s' % username, False


def list_users(db):
    """
    List the existing users in the DB.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :return: A list of registered users.
    :rtype: list of :class:`~users.User`-s
    """
    cur = db.cursor()
    cur.execute(LIST_USERS)
    return [User(row['id'], row['username'], row['display'], row['permissions']) for row in cur.fetchall()]


def get_user_details(db, user_id):
    """
    Get the details of a user.

    The details of a user, consists, in addition to the username and display, of the following information:

    * The number of boards this user has.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :return: The query result, or ``None`` if not found.
    :rtype: tuple of :class:`~users.User` and int
    """
    details = {'user_id': user_id}
    cur = db.cursor()
    cur.execute(GET_USER_DETAILS, details)
    row = cur.fetchone()
    if not row:
        return None
    return User(row['id'], row['username'], row['display'], row['permissions']), row['num_boards']


def edit_user_with_password(db, user_id, password, display, permissions):
    """
    Edit a user and set his new password.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :param password: The new user password.
    :type password: str
    :param display: The new user display.
    :type display: str
    :param permissions: The new user permissions.
    :type permissions: list of :class:`~users.UserPermission`-s
    """
    details = {'user_id': user_id,
               'password': hash_password(password),
               'display': display,
               'permissions': UserPermission.get_mask(permissions)}
    db.execute(EDIT_USER_WITH_PASSWORD, details)
    db.commit()


def edit_user_without_password(db, user_id, display, permissions):
    """
    Edit a user without changing his password.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :param display: The new user display.
    :type display: str
    :param permissions: The new user permissions.
    :type permissions: list of :class:`~users.UserPermission`-s
    """
    details = {'user_id': user_id,
               'display': display,
               'permissions': UserPermission.get_mask(permissions)}
    db.execute(EDIT_USER_WITHOUT_PASSWORD, details)
    db.commit()


def delete_user(db, user_id):
    """
    Delete a user and all his boards.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    """
    details = {'user_id': user_id}
    cur = db.cursor()
    cur.execute(DELETE_USER, details)
    cur.execute(DELETE_USER_BOARDS, details)
    db.commit()


def insert_board(db, user_id, board):
    """
    Insert a new board to the DB, and return its ID.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :param board: The board to insert.
    :type board: :class:`~board.Board`
    :return: The inserted board ID.
    :rtype: int
    """

    details = {'uid': user_id,
               'problem': str(board.problem),
               'solution': str(board.solution),
               'block_width': board.block_width,
               'block_height': board.block_height}
    cur = db.cursor()
    cur.execute(INSERT_BOARD, details)
    return cur.lastrowid


def list_user_boards(db, user_id):
    """
    List all boards of a user.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param user_id: The user ID in the DB.
    :type user_id: int
    :return: The boards (as dicts).
    :rtype: list
    """
    details = {'uid': user_id}
    cur = db.cursor()
    cur.execute(LIST_USER_BOARDS, details)
    return cur.fetchall()


def get_user_board(db, board_id, user_id):
    """
    Get a board of a specific user.

    :note: The user ID is given here to protect this user from getting other user's boards.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param board_id: The board ID.
    :type board_id: int
    :param user_id: The user ID in the DB.
    :type user_id: int
    :return: The board, or ``None`` if board does not exist.
    :rtype: :class:`~board.Board`
    """
    details = {'id': board_id,
               'uid': user_id}
    cur = db.cursor()
    cur.execute(GET_USER_BOARD, details)

    raw_board = cur.fetchone()
    if not raw_board:
        return None

    block_width = raw_board['block_width']
    block_height = raw_board['block_height']

    problem = SimpleBoard(block_width, block_height, raw_board['problem'])
    solution = SimpleBoard(block_width, block_height, raw_board['solution'])
    return Board(block_width, block_height, problem, solution)


def list_all_boards(db):
    """
    List all boards (of all users) in the DB.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :return: The boards (as dicts).
    :rtype: list
    """
    cur = db.cursor()
    cur.execute(LIST_ALL_BOARDS)
    return cur.fetchall()


def get_board(db, board_id):
    """
    Get a board from the DB.

    :param db: The DB connection object.
    :type db: :class:`sqlite3.Connection`
    :param board_id: The board ID.
    :type board_id: int
    :return: The board, or ``None`` if board does not exist.
    :rtype: :class:`~board.Board`
    """
    details = {'id': board_id}
    cur = db.cursor()
    cur.execute(GET_BOARD, details)

    raw_board = cur.fetchone()
    if not raw_board:
        return None

    block_width = raw_board['block_width']
    block_height = raw_board['block_height']

    problem = SimpleBoard(block_width, block_height, raw_board['problem'])
    solution = SimpleBoard(block_width, block_height, raw_board['solution'])
    return Board(block_width, block_height, problem, solution)


def init_db(app, root_user, root_password):
    """
    Initialize the application DB.

    This function creates a single user in the DB. This user is referred as the *root user*, and he has any possible
    permission.

    :param app: The Flask application.
    :type app: :class:`flask.Flask`
    :param root_user: The root user name.
    :type root_user: str
    :param root_password: The root user password.
    :type root_password: str
    """
    with closing(connect_db(app)) as db:
        with app.open_resource('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        register_user(db, root_user, root_password, None, UserPermission.PERMISSIONS)
