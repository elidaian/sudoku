from functools import wraps
from flask.app import Flask
from flask.globals import session, g, request
from flask.helpers import url_for, flash
from flask.templating import render_template
from werkzeug.utils import redirect
from sudoku.server import db

__author__ = "Eli Daian <elidaian@gmail.com>"

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("sudoku.cfg", silent=True)


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


@app.route("/")
def main_page():
    """
    Webserver index page.
    """
    if session.get("logged_in", False):
        user = db.get_user(g.db, session["user"])
    else:
        user = None
    return render_template("main_page.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Show the login page and handle login requests.
    """
    if request.method == "POST":
        try:
            username = request.form.get("username", None)
            password = request.form.get("password",None)

            if username is None or password is None:
                flash("Invalid data", "danger")
                return redirect(url_for("login"))

            user = db.login(g.db, username, password)
            if user is None:
                flash("Invalid login credentials", "danger")
            else:
                flash("You were logged in successfully!", "success")
                session["logged_in"] = True
                session["user"] = user.id

                if request.args.get("next", None):
                    return redirect(request.args["next"])
                return redirect(url_for("main_page"))
        except KeyError:
            flash("Missing username or password", "info")
    return render_template("login.html")


if __name__ == "__main__":
    app.run()
