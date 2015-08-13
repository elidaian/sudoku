from functools import wraps
from itertools import imap
from flask.app import Flask
from flask.globals import session, g, request
from flask.helpers import url_for, flash
from flask.templating import render_template
from werkzeug.utils import redirect
from sudoku.exceptions import ErrorWithMessage
from sudoku.generator import generate
from sudoku.server import db
from sudoku.server.users import PERM_CREATE_BOARD

__author__ = "Eli Daian <elidaian@gmail.com>"

INSITE_BOARD_VIEW = 0
PRINT_BOARD_VIEW = 1

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


def export_board_ids(board_ids):
    """
    Export a list of board IDs to an URL safe version.
    :param board_ids: The list of board IDs.
    :type board_ids: list
    :return: The URL form of the board IDs.
    :rtype: str
    """
    return "+".join(imap(str, board_ids))


def import_board_ids(url_board_ids):
    """
    Import a list of board IDs from an URL safe version.
    :param url_board_ids: The URL form of the board IDs.
    :type url_board_ids: str
    :return: A list of board IDs.
    :rtype: list
    """
    return map(int, url_board_ids.split("+"))


def view_one_board(board_id, solution, mode, root):
    """
    View a single board.
    """
    board = db.get_user_board(g.db, board_id, session["user"])

    if board is None:
        flash("Board not found", "warning")
        return redirect(url_for("main_page"))

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view", board=board, id=board_id, is_solution=solution,
                               root=root, user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template("print_board.html", multi_board=False, board=board, id=board_id, is_solution=solution)
    else:
        flash("Invalid mode", "warning")
        return redirect(url_for("main_page"))


def view_many_boards(url_board_ids, solution, mode, root):
    """
    View many boards.
    """
    board_ids = import_board_ids(url_board_ids)
    boards = [(db.get_user_board(g.db, board_id, session["user"]), board_id)
              for board_id in board_ids]

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view_many", boards=boards, is_solution=solution,
                               root=root, user=user, url_board_ids=url_board_ids)
    elif mode == PRINT_BOARD_VIEW:
        return render_template("print_board.html", multi_board=True, boards=boards, is_solution=solution)
    else:
        flash("Invalid mode", "warning")
        return redirect(url_for("main_page"))


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
            password = request.form.get("password", None)

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


@app.route("/logout")
def logout():
    """
    Log out and end the current session (if any).
    """
    if session.has_key("user"):
        flash("You have been logged out", "success")
        del session["user"]
    session["logged_in"] = False
    return redirect(url_for("main_page"))


@app.route("/create_board", methods=["GET", "POST"])
@must_login(PERM_CREATE_BOARD)
def create_board():
    """
    Create a new board or some new boards.
    """
    just_created = False
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
                raise ErrorWithMessage("Invalid board type")
            count = int(request.form["count"])

            boards = [generate(width, height) for i in xrange(count)]
            board_ids = [db.insert_board(g.db, session["user"], board)
                         for board in boards]
            g.db.commit()
            session["last_boards"] = board_ids
            if len(board_ids) == 1:
                flash("Created one board", "success")
            else:
                flash("Created %d boards" % len(board_ids), "success")
            just_created = True
        except ErrorWithMessage as e:
            flash(e.message, "danger")
        except (KeyError, ValueError):
            flash("Invalid request data", "danger")
        except:
            flash("Internal server error", "danger")
    user = db.get_user(g.db, session["user"])
    return render_template("create_board.html", just_created=just_created,
                           user=user)


@app.route("/view/list", defaults={"many": 0})
@app.route("/view/list/<int:many>")
@must_login(PERM_CREATE_BOARD)
def list_boards(many):
    """
    List the available user boards.
    """

    boards = db.list_user_boards(g.db, session["user"])
    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", boards=boards, function="list_many" if many else "list",
                           root=False, user=user)


@app.route("/view/last")
@must_login(PERM_CREATE_BOARD)
def view_last_boards():
    """
    View the last created boards.
    """
    if "last_boards" not in session:
        flash("You have not created any board in this session", "info")
        return redirect(url_for("view_board"))
    url_board_ids = export_board_ids(session["last_boards"])
    return redirect(url_for("view_set_of_boards", url_board_ids=url_board_ids, solution=False))


@app.route("/view")
@must_login(PERM_CREATE_BOARD)
def view_board():
    """
    View a board.
    """
    if "board_id" in request.args:
        is_solution = bool(request.args.get("solution", False))
        return redirect(url_for("view_specific_board", board_id=request.args["board_id"], solution=is_solution))

    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", function="main", root=False, user=user)


@app.route("/view/<int:board_id>", defaults={"solution": False})
@app.route("/view/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def view_specific_board(board_id, solution):
    """
    View one board insite.
    """
    return view_one_board(board_id, solution, INSITE_BOARD_VIEW, False)


@app.route("/print/<int:board_id>", defaults={"solution": False})
@app.route("/print/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def print_specific_board(board_id, solution):
    """
    Print one board.
    """
    return view_one_board(board_id, solution, PRINT_BOARD_VIEW, False)


@app.route("/pdf/<int:board_id>", defaults={"solution": False})
@app.route("/pdf/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def pdf_specific_board(board_id, solution):
    """
    Get the PDF of one board.
    """
    return "Not supported (yet)"


@app.route("/view/custom", methods=["POST"])
@must_login(PERM_CREATE_BOARD)
def view_set():
    """
    Get the reslts of the "View set of boards" form, and redirect to the right location.
    """
    board_ids = [int(board_id) for board_id in request.form.iterkeys() if board_id.isdigit()]
    board_ids.sort()
    url_board_ids = export_board_ids(board_ids)

    solution = "solution" in request.form

    return redirect(url_for("view_set_of_boards", url_board_ids=url_board_ids, solution=solution))


@app.route("/view/custom/<url_board_ids>", defaults={"solution": False})
@app.route("/view/solution/custom/<url_board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def view_set_of_boards(url_board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(url_board_ids, solution, INSITE_BOARD_VIEW, False)


@app.route("/print/custom/<url_board_ids>", defaults={"solution": False})
@app.route("/print/solution/custom/<url_board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_boards(url_board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(url_board_ids, solution, PRINT_BOARD_VIEW, False)


@app.route("/pdf/custom/<url_board_ids>", defaults={"solution": False})
@app.route("/pdf/solution/custom/<url_board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_boards(url_board_ids, solution):
    """
    View a set of boards insite.
    """
    board_ids = import_board_ids(url_board_ids)
    return "Not implemented (yet)"


# Here come functions to be added
@app.route("/register")
def register_user():
    pass


@app.route("/manage")
def manage_users():
    pass


@app.route("/list_other")
def list_other_boards():
    pass


if __name__ == "__main__":
    app.run()
