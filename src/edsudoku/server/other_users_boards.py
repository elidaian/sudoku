from flask.globals import g, session, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from edsudoku.server import db, app
from edsudoku.server.misc import must_login
from edsudoku.server.users import PERM_SHOW_OTHER_USER_BOARDS, PERM_CREATE_BOARD, User
from edsudoku.server.view_boards import view_one_board, INSITE_BOARD_VIEW, PRINT_BOARD_VIEW, view_many_boards, \
    PDF_BOARD_VIEW

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.route('/other/list', defaults={'many': False})
@app.route('/other/list/<bool:many>')
@must_login(PERM_SHOW_OTHER_USER_BOARDS)
def list_other_boards(many):
    """
    List the boards of all users.

    :param many: ``True`` iff multiple boards can be selected.
    :type many: bool
    :return: A list of boards.
    :rtype: flask.Response
    """
    boards = db.list_all_boards(g.db)
    user = User.get_by_id(session['user'])
    return render_template('list_boards.html', boards=boards, many=many, root=True, user=user)


@app.route('/other/view')
@must_login(PERM_CREATE_BOARD)
def view_other_board():
    """
    :return: A page that asks you if you want to select a single board or multiple boards. If a ``board_id`` argument is
        given in the request, the user will be redirected to
        :func:`~edsudoku.server.other_users_boards.view_specific_other_board`.
    :rtype: flask.Response
    """
    if 'board_id' in request.args:
        is_solution = bool(request.args.get('solution', False))
        return redirect(url_for('view_specific_other_board', board_id=request.args['board_id'], solution=is_solution))

    return redirect(url_for("list_other_boards", many=True))


@app.route('/other/view/<int:board_id>', defaults={'solution': False})
@app.route('/other/view/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def view_specific_other_board(board_id, solution):
    """
    View one board.

    The board will be displayed inside the website, i.e. the website menus and themes will be displayed with the board.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A page containing the board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, INSITE_BOARD_VIEW, True)


@app.route('/other/print/<int:board_id>', defaults={'solution': False})
@app.route('/other/print/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_specific_other_board(board_id, solution):
    """
    Print one board.

    This board will be displayed in a clean page that is dedicated for printing, i.e. the website menus and themes will
    not be shown in this page.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A page containing the board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, PRINT_BOARD_VIEW, True)


@app.route('/other/pdf/<int:board_id>', defaults={'solution': False})
@app.route('/other/pdf/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_specific_other_board(board_id, solution):
    """
    Get the PDF of one board.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A PDF containing the requested board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, PDF_BOARD_VIEW, True)


@app.route('/other/view/custom', methods=['POST'])
@must_login(PERM_CREATE_BOARD)
def view_other_set():
    """
    Process the results of the 'View set of boards' form (see :func:`~edsudoku.server.my_boards.list_boards`), and
    redirect to the right location (:func:`~edsudoku.server.other_users_boards.view_set_of_other_boards`).

    :return: A redirection.
    :rtype: flask.Response
    """
    board_ids = [int(board_id) for board_id in request.form.iterkeys() if board_id.isdigit()]
    board_ids.sort()

    solution = 'solution' in request.form

    return redirect(url_for('view_set_of_other_boards', board_ids=board_ids, solution=solution))


@app.route('/other/view/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/other/view/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def view_set_of_other_boards(board_ids, solution):
    """
    View multiple boards.

    The boards will be displayed inside the website, i.e. the website menus and themes will be displayed with the
    boards.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A page containing the boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, INSITE_BOARD_VIEW, True)


@app.route('/other/print/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/other/print/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_other_boards(board_ids, solution):
    """
    Print multiple boards.

    This boards will be displayed in a clean page that is dedicated for printing, i.e. the website menus and themes will
    not be shown in this page.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A page containing the boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, PRINT_BOARD_VIEW, True)


@app.route('/other/pdf/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/other/pdf/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_other_boards(board_ids, solution):
    """
    Get the PDF of multiple boards.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A PDF containing the requested boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, PDF_BOARD_VIEW, True)
