"""
server.py

 Created on: Aug 9 2013
     Author: eli
"""

import cPickle
from flask import Flask
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from functools import wraps

import pysudoku

import db
import pdf_renderer
import users
import util

### CONSTANTS ###

BOARD_MODES = util.enum("INSITE", "PRINT", "PDF")

### FUNCTIONS ###

app = Flask(__name__)
app.config.from_envvar("SUDOKU_SERVER_CONF_FILE")

texenv = pdf_renderer.create_env(app)

def get_board_from_board_row(board_row):
    """
    Get a Board object from a board row (from the DB).
    """
    return pysudoku.Board(board_row["problem"], board_row["solution"],
                          board_row["block_width"], board_row["block_height"])

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

def sslify(func):
    """
    Redirects the viewer to the SSL version of the site if the configuration
    requires it.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        if app.config["REQUIRE_SSL"]:
            if request.url.startswith("http://"):
                return redirect(request.url.replace("http://", "https://", 1))
        return func(*args, **kwargs)
    return wrapped

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

def view_one_board(board_id, board_row, solution, mode, root):
    """
    View a single board.
    """
    solution = bool(solution)
    
    if board_row is None:
        flash("Board not found", "warning")
        return redirect(url_for("main_page"))
    board = get_board_from_board_row(board_row)
    
    if mode == BOARD_MODES.INSITE:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view", board=board,
                               id=board_id, is_solution=solution, modes=BOARD_MODES,
                               root=root, curr_user=user)
    elif mode == BOARD_MODES.PRINT:
        return render_template("print_board.html", multi_board=False, board=board,
                               id=board_id, is_solution=solution)
    elif mode == BOARD_MODES.PDF:
        filename = "solution.pdf" if solution else "board.pdf"
        return pdf_renderer.render_pdf_template("pdf_board.tex", texenv,
                                                filename=filename,
                                                board=board, id=board_id,
                                                is_solution=solution,
                                                multi_board=False)
    else:
        flash("Invalid mode", "warning")
        return redirect(url_for("main_page"))

def parse_board_ids(list_func):
    """
    Parse the requested board IDs.
    """
    if request.method == "POST":
        board_ids = [int(board_id) for board_id in request.form.iterkeys()
                     if board_id.isdigit()]
        board_ids.sort()
    elif request.args.has_key("boards"):
        try:
            pickled = request.args["boards"].decode('base64').decode('zlib')
            board_ids = cPickle.loads(pickled)
        except:
            flash("Unknown boards", "warning")
            return redirect(url_for(list_func, many=1))
    else:
        return redirect(url_for(list_func, many=1))
    return board_ids

def view_many_boards(board_ids, board_rows, solution, mode, root):
    """
    View many boards.
    """
    solution = bool(solution)
    boards = [(get_board_from_board_row(board_row), board_id)
              for board_row, board_id in board_rows if board_row]
    boards_str = cPickle.dumps(board_ids).encode('zlib').encode('base64')
    
    if mode == BOARD_MODES.INSITE:
        user = db.get_user(g.db, session["user"])
        return render_template("view_board.html", function="view_many", boards=boards,
                               id=board_id, is_solution=solution, modes=BOARD_MODES,
                               boards_str=boards_str, root=root, curr_user=user)
    elif mode == BOARD_MODES.PRINT:
        return render_template("print_board.html", multi_board=True, boards=boards,
                               id=board_id, is_solution=solution)
    elif mode == BOARD_MODES.PDF:
        filename = "solutions.pdf" if solution else "boards.pdf"
        return pdf_renderer.render_pdf_template("pdf_board.tex", texenv,
                                                filename=filename,
                                                boards=boards, id=board_id,
                                                is_solution=solution,
                                                multi_board=True)
    else:
        flash("Invalid mode", "warning")
        return redirect(url_for("main_page"))

@app.route("/")
@sslify
def main_page():
    """
    Application root.
    Displays available boards, and link for board generation.
    """
    if session.get("logged_in", False):
        user = db.get_user(g.db, session["user"])
    else:
        user = None
    return render_template("main_page.html", curr_user=user)

@app.route("/login", methods=["GET", "POST"])
@sslify
def login():
    """
    Show the login page and handle login requests.
    """
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            
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
@sslify
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
@sslify
@must_login(users.PERM_CREATE_BOARD)
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
                raise util.ErrorWithMessage, "Invalid board type"
            count = int(request.form["count"])
            
            boards = pysudoku.create_board(width, height, count)
            board_ids = [db.insert_board(g.db, session["user"], board)
                         for board in boards]
            g.db.commit()
            session["last_boards"] = board_ids
            if len(board_ids) == 1:
                flash("Created one board", "success")
            else:
                flash("Created %d boards" % len(board_ids), "success")
            just_created = True
        except util.ErrorWithMessage as e:
            flash(e.message, "danger")
        except (KeyError, ValueError):
            flash("Invalid request data", "danger")
        except:
            flash("Internal server error", "danger")
    user = db.get_user(g.db, session["user"])
    return render_template("create_board.html", just_created=just_created,
                           curr_user=user)

@app.route("/view")
@sslify
@must_login(users.PERM_CREATE_BOARD)
def view_board():
    """
    View a board.
    """
    if request.args.has_key("board_id"):
        return redirect(url_for("view_specific_board",
                                board_id=request.args["board_id"],
                                solution=request.args.get("solution", "0")))
    
    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", function="main", root=False,
                           curr_user=user)

@app.route("/view/list", defaults={"many": 0})
@app.route("/view/list/<int:many>")
@sslify
@must_login(users.PERM_CREATE_BOARD)
def list_boards(many):
    """
    List the available user boards.
    """
    
    boards = db.list_user_boards(g.db, session["user"])
    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", boards=boards,
                           function="list_many" if many else "list", root=False,
                           curr_user=user)

@app.route("/view/last")
@sslify
@must_login(users.PERM_CREATE_BOARD)
def view_last_boards():
    """
    View the last created boards.
    """
    if not session.has_key("last_boards"):
        flash("You have not created any board in this session", "info")
        return redirect(url_for("view_board"))
    boards = cPickle.dumps(session["last_boards"]).encode('zlib').encode('base64')
    return redirect(url_for("view_board_set", boards=boards))

@app.route("/view/<int:board_id>",
           defaults={"solution": 0, "mode": BOARD_MODES.INSITE})
@app.route("/view/<int:board_id>/<int:solution>",
           defaults={"mode": BOARD_MODES.INSITE})
@app.route("/view/<int:board_id>/<int:solution>/<int:mode>")
@sslify
@must_login(users.PERM_CREATE_BOARD)
def view_specific_board(board_id, solution, mode):
    """
    View a board.
    """
    board_row = db.get_user_board(g.db, board_id, session["user"])
    return view_one_board(board_id, board_row, solution, mode, False)

@app.route("/view/custom", methods=["GET", "POST"],
           defaults={"solution": 0, "mode": BOARD_MODES.INSITE})
@app.route("/view/custom/<int:solution>",
           defaults={"mode": BOARD_MODES.INSITE})
@app.route("/view/custom/<int:solution>/<int:mode>")
@sslify
@must_login(users.PERM_CREATE_BOARD)
def view_board_set(solution, mode):
    board_ids = parse_board_ids("list_boards")
    if type(board_ids) is not list:
        return board_ids        # this is a redirection
    if len(board_ids) == 1:
        return redirect(url_for("view_specific_board", board_id=board_ids[0],
                                solution=solution, mode=mode))
    
    board_rows = [(db.get_user_board(g.db, board_id, session["user"]), board_id)
                  for board_id in board_ids]
    return view_many_boards(board_ids, board_rows, solution, mode, False)

@app.route("/register", methods=["GET", "POST"])
@sslify
@must_login(users.PERM_MANAGE_USERS)
def register_user():
    """
    Register a new user account.
    """
    curr_user = db.get_user(g.db, session["user"])
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password2"]
            if username == "":
                flash("Username cannot be empty", "danger")
                return render_template("register.html", users=users,
                                       curr_user=curr_user)
            if password != password2:
                flash("Passwords do not match", "warning")
                return render_template("register.html", users=users,
                                       curr_user=curr_user)
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
            flash(message, "success" if status else "danger")
        except KeyError:
            flash("Missing username or password", "warning")
    return render_template("register.html", users=users, curr_user=curr_user)

@app.route("/manage")
@sslify
@must_login(users.PERM_MANAGE_USERS)
def manage_users():
    """
    Manage the other users.
    """
    users = db.list_users(g.db)
    curr_user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="main", users=users,
                           curr_user=curr_user)

@app.route("/manage/<int:user_id>", methods=["GET", "POST"])
@sslify
@must_login(users.PERM_MANAGE_USERS)
def edit_user(user_id):
    """
    Edit a user.
    """
    
    if request.method == "POST":
        try:
            password = request.form["password"]
            if password != "":
                has_password = True
                password2 = request.form["password2"]
                if password != password2:
                    flash("Passwords mismatch", "warning")
                    return redirect(url_for(edit_user, user_id=user_id))
            else:
                has_password = False
            display = request.form["display"]
            if not display:
                display = None
            
            permissions = []
            for permission in users.UserPermission.PERMISSIONS:
                if request.form.has_key(permission.name) and \
                        request.form[permission.name] == str(permission.flag):
                    permissions.append(permission)
            
            if has_password:
                db.edit_user_with_password(g.db, user_id, password, display, permissions)
            else:
                db.edit_user_without_password(g.db, user_id, display, permissions)
            
            flash("User updated successfully", "success")
        except KeyError:
            flash("Invalid sent form", "danger")
    
    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    user = users.User(user_id, user_details["username"],
                      user_details["display"], user_details["permissions"])
    curr_user = db.get_user(g.db, session["user"])
    
    return render_template("manage.html", function="edit", user_id=user_id,
                           user=user, user_details=user_details,
                           users=users, curr_user=curr_user)

@app.route("/manage/delete/<int:user_id>", methods=["GET", "POST"])
@sslify
@must_login(users.PERM_MANAGE_USERS)
def delete_user(user_id):
    """
    Delete a user.
    """
    
    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    user = users.User(user_id, user_details["username"],
                      user_details["display"], user_details["permissions"])
    
    if request.method == "POST":
        try:
            user_id2 = int(request.form["user_id"])
            approved = int(request.form["approved"])
            if user_id != user_id2 or approved != 1:
                raise RuntimeError
            
            db.delete_user(g.db, user_id)
            flash("User %s has been deleted successfully" % user.display, "success")
            return redirect(url_for("manage_users"))
        except:
            flash("Unknown data received", "danger")
    
    curr_user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="delete", user_id=user_id,
                           user=user, user_details=user_details,
                           curr_user=curr_user)

@app.route("/other")
@sslify
@must_login(users.PERM_SHOW_OTHER_USER_BOARDS)
def other_user():
    """
    View other user's boards.
    """
    if request.args.has_key("board_id"):
        return redirect(url_for("other_specific_board",
                                board_id=request.args["board_id"],
                                solution=request.args.get("solution", "0")))
    
    curr_user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", function="main", root=True,
                           curr_user=curr_user)

@app.route("/other/list", defaults={"many": 0})
@app.route("/other/list/<int:many>")
@sslify
@must_login(users.PERM_SHOW_OTHER_USER_BOARDS)
def list_other_boards(many):
    """
    List all the boards of the other users.
    """
    boards = db.list_all_boards(g.db)
    curr_user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", boards=boards,
                           function="list_many" if many else "list", root=True,
                           curr_user=curr_user)

@app.route("/other/<int:board_id>",
           defaults={"solution": 0, "mode": BOARD_MODES.INSITE})
@app.route("/other/<int:board_id>/<int:solution>",
           defaults={"mode": BOARD_MODES.INSITE})
@app.route("/other/<int:board_id>/<int:solution>/<int:mode>")
@sslify
@must_login(users.PERM_SHOW_OTHER_USER_BOARDS)
def other_specific_board(board_id, solution, mode):
    """
    View a specific board of other users.
    """
    board_row = db.get_board(g.db, board_id)
    return view_one_board(board_id, board_row, solution, mode, True)

@app.route("/other/custom", methods=["GET", "POST"],
           defaults={"solution": 0, "mode": BOARD_MODES.INSITE})
@app.route("/other/custom/<int:solution>",
           defaults={"mode": BOARD_MODES.INSITE})
@app.route("/other/custom/<int:solution>/<int:mode>")
@sslify
@must_login(users.PERM_SHOW_OTHER_USER_BOARDS)
def other_board_set(solution, mode):
    board_ids = parse_board_ids("list_other_boards")
    if type(board_ids) is not list:
        return board_ids        # this is a redirection
    if len(board_ids) == 1:
        return redirect(url_for("other_specific_board", board_id=board_ids[0],
                                solution=solution, mode=mode))
    
    board_rows = [(db.get_board(g.db, board_id), board_id) for board_id in board_ids]
    return view_many_boards(board_ids, board_rows, solution, mode, True)

@app.route("/fonts/<path:filename>")
def get_font(filename):
    """
    Get a file from the fonts directory.
    """
    return send_from_directory("fonts", filename)

if __name__ == "__main__":
    app.run()
