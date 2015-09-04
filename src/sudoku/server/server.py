from functools import wraps
from itertools import imap

from flask.app import Flask
from flask.globals import session, g, request
from flask.helpers import url_for, flash, send_from_directory
from flask.templating import render_template

from werkzeug.utils import redirect

from sudoku.exceptions import ErrorWithMessage
from sudoku.generator import generate
from sudoku.server import db
from sudoku.server.converters import BooleanConverter, IntegersListConverter
from sudoku.server.users import PERM_CREATE_BOARD, PERM_MANAGE_USERS, UserPermission

__author__ = "Eli Daian <elidaian@gmail.com>"

INSITE_BOARD_VIEW = 0
PRINT_BOARD_VIEW = 1

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("sudoku.cfg", silent=True)
app.url_map.converters["bool"] = BooleanConverter
app.url_map.converters["list"] = IntegersListConverter

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


def view_many_boards(board_ids, solution, mode, root):
    """
    View many boards.
    """
    boards = [(db.get_user_board(g.db, board_id, session["user"]), board_id)
              for board_id in board_ids]

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view_many", boards=boards, is_solution=solution,
                               root=root, user=user, board_ids=board_ids)
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
    session.clear()
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
            if app.debug:
                raise
            flash("Internal server error", "danger")
    user = db.get_user(g.db, session["user"])
    return render_template("create_board.html", just_created=just_created,
                           user=user)


@app.route("/view/list", defaults={"many": False})
@app.route("/view/list/<bool:many>")
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
    return redirect(url_for("view_set_of_boards", board_ids=session["last_boards"], solution=False))


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

    solution = "solution" in request.form

    return redirect(url_for("view_set_of_boards", board_ids=board_ids, solution=solution))


@app.route("/view/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/view/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def view_set_of_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, INSITE_BOARD_VIEW, False)


@app.route("/print/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/print/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, PRINT_BOARD_VIEW, False)


@app.route("/pdf/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/pdf/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return "Not implemented (yet)"


# Here come functions to be added
@app.route("/register", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def register_user():
    """
    Register a new user account.
    """
    user = db.get_user(g.db, session["user"])

    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        password2 = request.form.get("password2", None)

        if not username:
            flash("Username cannot be empty", "danger")
            return redirect(url_for("register_user"))
        if not password:
            flash("Password cannot be empty", "warning")
            return redirect(url_for("register_user"))
        if password != password2:
            flash("Passwords do not match", "warning")
            return redirect(url_for("register_user"))

        display = request.form.get("display", None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]
        message, status = db.register_user(g.db, username, password, display, permissions)
        flash(message, "success" if status else "danger")

    return render_template("register.html", user=user, permissions=UserPermission.PERMISSIONS)


@app.route("/manage")
@must_login(PERM_MANAGE_USERS)
def manage_users():
    """
    Manage the other users.
    """
    users = db.list_users(g.db)
    user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="main", users=users, user=user)


@app.route("/manage/<int:user_id>", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def edit_user(user_id):
    """
    Edit a user.
    """
    user = db.get_user(g.db, session["user"])

    if request.method == "POST":
        password = request.form.get("password", None)
        display = request.form.get("display", None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]

        if password:
            password2 = request.form.get("password2", None)

            if password != password2:
                flash("Passwords mismatch", "warning")
                return redirect(url_for("edit_user", user_id=user_id))

            db.edit_user_with_password(g.db, user_id, password, display, permissions)
        else:
            db.edit_user_without_password(g.db, user_id, display, permissions)

        flash("User updated successfully", "success")
        return redirect(url_for("manage_users"))

    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    edited_user, num_boards = user_details

    return render_template("manage.html", function="edit", user=user, user_id=user_id, edited_user=edited_user,
                           num_boards=num_boards, permissions=UserPermission.PERMISSIONS)


@app.route("/manage/delete/<int:user_id>", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def delete_user(user_id):
    """
    Delete a user.
    """
    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    user_to_delete, num_boards = user_details

    if request.method == "POST":
        user_id2 = int(request.form.get("user_id", -1))
        approved = bool(request.form.get("approved", False))

        if approved and user_id == user_id:
            db.delete_user(g.db, user_id)
            flash("User %s has been deleted successfully" % user_to_delete.display, "success")
        else:
            flash("User not deleted", "warning")
        return redirect(url_for("manage_users"))

    user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="delete", user=user, user_to_delete=user_to_delete,
                           num_boards=num_boards, user_id=user_id)


@app.route("/list_other")
def list_other_boards():
    pass


@app.route("/fonts/<path:filename>")
def get_font(filename):
    """
    Get a file from the fonts directory.
    """
    return send_from_directory("fonts", filename)


if __name__ == "__main__":
    app.run()
