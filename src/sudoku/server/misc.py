from functools import wraps

from flask.globals import session, request, g
from flask.helpers import url_for, flash, send_from_directory
from werkzeug.utils import redirect

from sudoku.server import db, app

__author__ = "Eli Daian <elidaian@gmail.com>"


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


def must_login(permission=None):
    """
    Wraps a page that requires a logged in viewer.
    If permission is given, the viewing user must have the given permission.
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not session.get("logged_in"):
                return redirect(url_for("login", next=request.url))
            elif permission is not None and not db.get_user(g.db, session["user"]).has_permission(permission):
                flash("Permission denied", "danger")
                return redirect(url_for("main_page"))
            else:
                return func(*args, **kwargs)

        return wrapped

    return wrapper


@app.route("/fonts/<path:filename>")
def get_font(filename):
    """
    Get a file from the fonts directory.
    """
    return send_from_directory("fonts", filename)
