from flask.globals import g, session, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from sudoku.server import db, app
from sudoku.server.misc import must_login
from sudoku.server.users import PERM_SHOW_OTHER_USER_BOARDS, PERM_CREATE_BOARD
from sudoku.server.view_boards import view_one_board, INSITE_BOARD_VIEW, PRINT_BOARD_VIEW, view_many_boards

__author__ = "Eli Daian <elidaian@gmail.com>"


@app.route("/other/list", defaults={"many": False})
@app.route("/other/list/<bool:many>")
@must_login(PERM_SHOW_OTHER_USER_BOARDS)
def list_other_boards(many):
    """
    List all the boards of the other users.
    """
    boards = db.list_all_boards(g.db)
    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", boards=boards, function="list_many" if many else "list",
                           root=True, user=user)


@app.route("/other/view")
@must_login(PERM_CREATE_BOARD)
def view_other_board():
    """
    View a board.
    """
    if "board_id" in request.args:
        is_solution = bool(request.args.get("solution", False))
        return redirect(url_for("view_specific_board", board_id=request.args["board_id"], solution=is_solution))

    user = db.get_user(g.db, session["user"])
    return render_template("view_board.html", function="main", root=True, user=user)


@app.route("/other/view/<int:board_id>", defaults={"solution": False})
@app.route("/other/view/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def view_specific_other_board(board_id, solution):
    """
    View one board insite.
    """
    return view_one_board(board_id, solution, INSITE_BOARD_VIEW, True)


@app.route("/other/print/<int:board_id>", defaults={"solution": False})
@app.route("/other/print/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def print_specific_other_board(board_id, solution):
    """
    Print one board.
    """
    return view_one_board(board_id, solution, PRINT_BOARD_VIEW, True)


@app.route("/other/pdf/<int:board_id>", defaults={"solution": False})
@app.route("/other/pdf/solutions/<int:board_id>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def pdf_specific_other_board(board_id, solution):
    """
    Get the PDF of one board.
    """
    return "Not supported (yet)"


@app.route("/other/view/custom", methods=["POST"])
@must_login(PERM_CREATE_BOARD)
def view_other_set():
    """
    Get the reslts of the "View set of boards" form, and redirect to the right location.
    """
    board_ids = [int(board_id) for board_id in request.form.iterkeys() if board_id.isdigit()]
    board_ids.sort()

    solution = "solution" in request.form

    return redirect(url_for("view_set_of_other_boards", board_ids=board_ids, solution=solution))


@app.route("/other/view/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/other/view/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def view_set_of_other_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, INSITE_BOARD_VIEW, True)


@app.route("/other/print/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/other/print/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_other_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, PRINT_BOARD_VIEW, True)


@app.route("/other/pdf/custom/<list:board_ids>", defaults={"solution": False})
@app.route("/other/pdf/solution/custom/<list:board_ids>", defaults={"solution": True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_other_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return "Not implemented (yet)"
