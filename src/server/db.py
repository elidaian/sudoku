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

def connect_db(app):
    """
    Create a new DB connection.
    """
    db = sqlite3.connect(app.config["DATABASE"])
    db.row_factory = sqlite3.Row
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
