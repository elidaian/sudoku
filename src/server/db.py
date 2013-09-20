"""
db.py

 Created on: Aug 17 2013
     Author: eli
"""

from contextlib import closing
import hashlib
import sqlite3

import users

LOGIN_QUERY = """
select id, display, permissions from users
where username = :username and password = :password
"""

REGISTER_USER = """
insert into users(username, password, display, permissions)
values (:username, :password, :display, :permissions)
"""

LIST_USERS = """
select id, username, display from users
"""

GET_USER_DETAILS = """
select username, display, permissions,
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
    """
    db = sqlite3.connect(app.config["DATABASE"])
    db.row_factory = sqlite3.Row
    db.text_factory = str
    return db

def hash_password(password):
    return buffer(hashlib.sha512(password).digest())

def login(db, username, password):
    """
    Get user information (if available) given the username and password,
    or None if the login credentials are invalid.
    """
    info = {"username": username,
            "password": hash_password(password)}
    cur = db.execute(LOGIN_QUERY, info)
    entry = cur.fetchone()
    if entry is not None:
        return users.User(entry["id"], username, entry["display"],
                          entry["permissions"])
    else:
        return None

def register_user(db, username, password, display, permissions):
    """
    Register a new user given its details.
    """
    
    try:
        details = {"username"   : username,
                   "password"   : hash_password(password),
                   "display"    : display,
                   "permissions": users.UserPermission.get_mask(permissions)}
        db.execute(REGISTER_USER, details)
        db.commit()
        return "User %s successfully created!" % (display if display else username), True
    except sqlite3.IntegrityError as e:
        return "Unable to register %s" % username, False

def list_users(db):
    """
    List the existing users.
    """
    cur = db.cursor()
    cur.execute(LIST_USERS)
    return cur.fetchall()

def get_user_details(db, user_id):
    """
    Get the details of a user.
    """
    details = {"user_id": user_id}
    cur = db.cursor()
    cur.execute(GET_USER_DETAILS, details)
    return cur.fetchone()

def edit_user_with_password(db, user_id, password, display, permissions):
    """
    Edit a user and set its password.
    """
    details = {"user_id"    : user_id,
               "password"   : hash_password(password),
               "display"    : display,
               "permissions": users.UserPermission.get_mask(permissions)}
    db.execute(EDIT_USER_WITH_PASSWORD, details)
    db.commit()

def edit_user_without_password(db, user_id, display, permissions):
    """
    Edit a user without changing its password.
    """
    details = {"user_id"     : user_id,
               "display"     : display,
               "permissions" : users.UserPermission.get_mask(permissions)}
    db.execute(EDIT_USER_WITHOUT_PASSWORD, details)
    db.commit()

def delete_user(db, user_id):
    """
    Delete a user and his boards.
    """
    details = {"user_id": user_id}
    cur = db.cursor()
    cur.execute(DELETE_USER, details)
    cur.execute(DELETE_USER_BOARDS, details)
    db.commit()

def insert_board(db, uid, board):
    """
    Insert a new board to the DB, and return its ID.
    """
    
    details = {"uid": uid,
               "problem": board.get_problem(),
               "solution": board.get_solution(),
               "block_width": board.get_block_width(),
               "block_height": board.get_block_height()}
    cur = db.cursor()
    cur.execute(INSERT_BOARD, details)
    return cur.lastrowid

def list_user_boards(db, uid):
    details = {"uid": uid}
    cur = db.cursor()
    cur.execute(LIST_USER_BOARDS, details)
    return cur.fetchall()

def get_user_board(db, board_id, uid):
    details = {"id": board_id,
               "uid": uid}
    cur = db.cursor()
    cur.execute(GET_USER_BOARD, details)
    return cur.fetchone()

def list_all_boards(db):
    cur = db.cursor()
    cur.execute(LIST_ALL_BOARDS)
    return cur.fetchall()

def get_board(db, board_id):
    details = {"id": board_id}
    cur = db.cursor()
    cur.execute(GET_BOARD, details)
    return cur.fetchone()

def init_db(app, root_user, root_password):
    """
    Initialize the application DB.
    """
    with closing(connect_db(app)) as db:
        with open("schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()
        register_user(db, root_user, root_password, None,
                      users.UserPermission.PERMISSIONS)
