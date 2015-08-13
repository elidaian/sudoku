from functools import wraps
from json import dumps, loads
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


def parse_board_ids(list_func):
    """
    Parse the requested board IDs.
    """
    if request.method == "POST":
        board_ids = [int(board_id) for board_id in request.form.iterkeys() if board_id.isdigit()]
        board_ids.sort()
    elif "boards" in request.args:
        try:
            json = request.args["boards"].decode('base64').decode('zlib')
            board_ids = loads(json)
        except:
            flash("Unknown boards", "warning")
            return redirect(url_for(list_func, many=1))
    else:
        return redirect(url_for(list_func, many=1))
    return board_ids


def view_many_boards(board_ids, boards, solution, mode, root):
    """
    View many boards.
    """
    solution = bool(solution)
    boards_str = dumps(board_ids).encode("zlib").encode("base64")

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view_many", boards=boards, is_solution=solution,
                               boards_str=boards_str, root=root, curr_user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template("print_board.html", multi_board=True, boards=boards, is_solution=solution)
    elif mode == PDF_BOARD_VIEW:
        return "Not supported (yet)"
        # filename = "solutions.pdf" if solution else "boards.pdf"
        # return pdf_renderer.render_pdf_template("pdf_board.tex", texenv,
        #                                         filename=filename,
        #                                         boards=boards, id=board_id,
        #                                         is_solution=solution,
        #                                         multi_board=True)
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
    boards = dumps(session["last_boards"]).encode("zlib").encode("base64")
    return redirect(url_for("view_board_set", boards=boards))


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


@app.route("/view/custom", methods=["GET", "POST"],
           defaults={"solution": 0, "mode": INSITE_BOARD_VIEW})
@app.route("/view/custom/<int:solution>",
           defaults={"mode": INSITE_BOARD_VIEW})
@app.route("/view/custom/<int:solution>/<int:mode>")
@must_login(PERM_CREATE_BOARD)
def view_board_set(solution, mode):
    board_ids = parse_board_ids("list_boards")
    if type(board_ids) is not list:
        return board_ids  # this is a redirection
    if len(board_ids) == 1:
        return redirect(url_for("view_specific_board", board_id=board_ids[0],
                                solution=solution, mode=mode))

    board_rows = [(db.get_user_board(g.db, board_id, session["user"]), board_id)
                  for board_id in board_ids]
    return view_many_boards(board_ids, board_rows, solution, mode, False)

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
