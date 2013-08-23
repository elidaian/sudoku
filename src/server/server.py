"""
server.py

 Created on: Aug 9 2013
     Author: eli
"""

from flask import g
from flask import Flask
from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from functools import wraps
import os

import pysudoku

import config
import db
import users
import util

app = Flask(__name__)
app.config.from_object(config)

def init_db(root_user, root_password):
    """
    Initialize the application DB.
    """
    db.init_db(app, root_user, root_password)

@app.before_request
def open_db():
    """
    Initialize a DB connection before any request.
    """
    g.db = db.connect_db(app)

@app.teardown_request
def close_db(exception):
    """
    Close the DB connection after any request.
    """
    conn = getattr(g, "db", None)
    if conn is not None:
        conn.close()

def must_login(func):
    """
    Wraps a page that requires a logged in viewer.
    """
    @wraps(func)
    def wrapped():
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.url))
        else:
            return func()
    return wrapped

@app.route("/")
@must_login
def main_page():
    """
    Application root.
    Displays available boards, and link for board generation.
    """
#     if not session.get("logged_in"):
#         return redirect(url_for("login"))
    return render_template("main_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Show the login page and handle login requests.
    """
    error = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            
            user = db.login(g.db, username, password)
            if user is None:
                error = "Invalid login credentials"
            else:
                flash("You were logged in successfully!")
                session["logged_in"] = True
                session["user"] = user
                
                if request.args.get("next", None):
                    return redirect(request.args["next"])
                return redirect(url_for("main_page"))
        except KeyError:
            error = "Missing username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    """
    Log out and end the current session (if any).
    """
    if session.has_key("user"):
        del session["user"]
    session["logged_in"] = False
    flash("You have been logged out")
    return redirect(url_for("main_page"))

@app.route("/create_board", methods=["GET", "POST"])
@must_login
def create_board():
    """
    Create a new board or some new boards.
    """
    error = None
    if request.method == "POST":
        try:
            board_type = request.form["type"]
            if board_type == "regular":
                width = 3
                height = 3
            elif board_type == "dodeka":
                width = 4
                height = 3
            elif board_type == "custom":
                width = int(request.form["width"])
                height = int(request.form["height"])
            else:
                raise util.ErrorWithMessage, "Invalid board type"
            count = int(request.form["count"])
            
            boards = pysudoku.create_board(width, height, count)
            board_ids = [db.insert_board(g.db, session["user"].id, board)
                         for board in boards]
            g.db.commit()
            flash("Created boards %s" % ", ".join(map(str, board_ids)))
        except util.ErrorWithMessage as e:
            error = e.message
        except (KeyError, ValueError):
            error = "Invalid request data"
        except:
            error = "Internal server error"
    return render_template("create_board.html", error=error)

@app.route("/register", methods=["GET", "POST"])
@must_login
def register_user():
    """
    Register a new user account.
    """
    """
    Show the login page and handle login requests.
    """
    error = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            display = request.form["display"]
            if not display:
                display = None
            
            permissions = []
            for permission in users.UserPermission.PERMISSIONS:
                if request.form.has_key(permission.name) and \
                        request.form[permission.name] == str(permission.flag):
                    permissions.append(permission)
            
            message, status = db.register_user(g.db, username, password, display,
                                               permissions)
            if status:
                flash(message)
            else:
                error = message
        except KeyError:
            error = "Missing username or password"
    return render_template("register.html", users=users, error=error)

@app.route("/other")
@must_login
def other_user():
    """
    View other user's boards.
    """
    return "Not yet implemented"

@app.route('/reset')
@must_login
def reset():
    """
    Reset the DB.
    """
    init_db("eli", "eli")
    flash("The DB has been reset")
    return redirect(url_for("logout"))

if __name__ == "__main__":
    app.run()
