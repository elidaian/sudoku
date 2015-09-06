from flask.globals import request, session, g
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from edsudoku.exceptions import ErrorWithMessage
from edsudoku.generator import generate
from edsudoku.server import db, app
from edsudoku.server.misc import must_login
from edsudoku.server.users import PERM_CREATE_BOARD, User
from edsudoku.server.view_boards import view_one_board, INSITE_BOARD_VIEW, PRINT_BOARD_VIEW, view_many_boards, \
    PDF_BOARD_VIEW

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.route('/create_board', methods=['GET', 'POST'])
@must_login(PERM_CREATE_BOARD)
def create_board():
    """
    Create a new board or some new boards.

    * If this page is requested with a GET method, the board generation form is returned.
    * If this page is requested with a POST method, a board generation form is processed, and new board/s is/are
        generated. Later a board generation form is returned, with a message that new boards were generated, with a
        link to the newly generated board/s.

    :return: As explained above.
    :rtype: flask.Response
    """
    just_created = False
    if request.method == 'POST':
        try:
            board_type = request.form['type']
            if board_type == 'regular':
                width = 3
                height = 3
            elif board_type == 'dodeka':
                width = 4
                height = 3
            elif board_type == 'custom':
                width = int(request.form['width'])
                height = int(request.form['height'])
            else:
                raise ErrorWithMessage('Invalid board type')
            count = int(request.form['count'])

            boards = [generate(width, height) for i in xrange(count)]
            board_ids = [db.insert_board(g.db, session['user'], board)
                         for board in boards]
            g.db.commit()
            session['last_boards'] = board_ids
            if len(board_ids) == 1:
                flash('Created one board', 'success')
            else:
                flash('Created %d boards' % len(board_ids), 'success')
            just_created = True
        except ErrorWithMessage as e:
            flash(e.message, 'danger')
        except (KeyError, ValueError):
            flash('Invalid request data', 'danger')
        except:
            if app.debug:
                raise
            flash('Internal server error', 'danger')
    user = User.get_by_id(session['user'])
    return render_template('create_board.html', just_created=just_created,
                           user=user)


@app.route('/view/list', defaults={'many': False})
@app.route('/view/list/<bool:many>')
@must_login(PERM_CREATE_BOARD)
def list_boards(many):
    """
    List the available user boards.

    :param many: ``True`` iff multiple boards can be selected.
    :type many: bool
    :return: A list of the users boards.
    :rtype: flask.Response
    """

    boards = db.list_user_boards(g.db, session['user'])
    user = User.get_by_id(session['user'])
    return render_template('list_boards.html', boards=boards, many=many, root=False, user=user)


@app.route('/view/last')
@must_login(PERM_CREATE_BOARD)
def view_last_boards():
    """
    View the last created boards.

    Actually, this function redirects to :func:`~edsudoku.server.my_boards.view_set_of_boards` in such way that the last
    generated board/s will be viewd.

    :return: A redirection.
    :rtype: flask.Response
    """
    if 'last_boards' not in session:
        flash('You have not created any board in this session', 'info')
        return redirect(url_for('view_board'))
    return redirect(url_for('view_set_of_boards', board_ids=session['last_boards'], solution=False))


@app.route('/view')
@must_login(PERM_CREATE_BOARD)
def view_board():
    """
    :return: A page that asks you if you want to select a single board or multiple boards.
    :rtype: flask.Response
    """
    if 'board_id' in request.args:
        is_solution = bool(request.args.get('solution', False))
        return redirect(url_for('view_specific_board', board_id=request.args['board_id'], solution=is_solution))

    return redirect(url_for("list_boards", many=True))


@app.route('/view/<int:board_id>', defaults={'solution': False})
@app.route('/view/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def view_specific_board(board_id, solution):
    """
    View one board.

    The board will be displayed inside the website, i.e. the website menus and themes will be displayed with the board.

    :note: This board **must** be owned by the logged in user.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A page containing the board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, INSITE_BOARD_VIEW, False)


@app.route('/print/<int:board_id>', defaults={'solution': False})
@app.route('/print/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_specific_board(board_id, solution):
    """
    Print one board.

    This board will be displayed in a clean page that is dedicated for printing, i.e. the website menus and themes will
    not be shown in this page.

    :note: This board **must** be owned by the logged in user.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A page containing the board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, PRINT_BOARD_VIEW, False)


@app.route('/pdf/<int:board_id>', defaults={'solution': False})
@app.route('/pdf/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_specific_board(board_id, solution):
    """
    Get the PDF of one board.

    :note: This board **must** be owned by the logged in user.

    :param board_id: The board ID to view.
    :type board_id: int
    :param solution: ``True`` iff the solution is requested.
    :type solution: bool
    :return: A PDF containing the requested board.
    :rtype: flask.Response
    """
    return view_one_board(board_id, solution, PDF_BOARD_VIEW, False)


@app.route('/view/custom', methods=['POST'])
@must_login(PERM_CREATE_BOARD)
def view_set():
    """
    Process the results of the 'View set of boards' form (see :func:`~edsudoku.server.my_boards.list_boards`), and
    redirect to the right location (:func:`~edsudoku.server.my_boards.view_set_of_boards`).

    :return: A redirection.
    :rtype: flask.Response
    """
    board_ids = [int(board_id) for board_id in request.form.iterkeys() if board_id.isdigit()]
    board_ids.sort()

    solution = 'solution' in request.form

    return redirect(url_for('view_set_of_boards', board_ids=board_ids, solution=solution))


@app.route('/view/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/view/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def view_set_of_boards(board_ids, solution):
    """
    View multiple boards.

    The boards will be displayed inside the website, i.e. the website menus and themes will be displayed with the
    boards.

    :note: These boards **must** be owned by the logged in user.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A page containing the boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, INSITE_BOARD_VIEW, False)


@app.route('/print/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/print/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_boards(board_ids, solution):
    """
    Print multiple boards.

    This boards will be displayed in a clean page that is dedicated for printing, i.e. the website menus and themes will
    not be shown in this page.

    :note: These boards **must** be owned by the logged in user.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A page containing the boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, PRINT_BOARD_VIEW, False)


@app.route('/pdf/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/pdf/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_boards(board_ids, solution):
    """
    Get the PDF of multiple boards.

    :note: These boards **must** be owned by the logged in user.

    :param board_ids: The board IDs to view.
    :type board_ids: list of ints
    :param solution: ``True`` iff the solutions are requested.
    :type solution: bool
    :return: A PDF containing the requested boards.
    :rtype: flask.Response
    """
    return view_many_boards(board_ids, solution, PDF_BOARD_VIEW, False)
