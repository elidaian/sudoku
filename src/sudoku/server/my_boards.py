from flask.globals import request, session, g
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from sudoku.exceptions import ErrorWithMessage
from sudoku.generator import generate
from sudoku.server import db, app
from sudoku.server.misc import must_login
from sudoku.server.users import PERM_CREATE_BOARD
from sudoku.server.view_boards import view_one_board, INSITE_BOARD_VIEW, PRINT_BOARD_VIEW, view_many_boards

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.route('/create_board', methods=['GET', 'POST'])
@must_login(PERM_CREATE_BOARD)
def create_board():
    """
    Create a new board or some new boards.
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
    user = db.get_user(g.db, session['user'])
    return render_template('create_board.html', just_created=just_created,
                           user=user)


@app.route('/view/list', defaults={'many': False})
@app.route('/view/list/<bool:many>')
@must_login(PERM_CREATE_BOARD)
def list_boards(many):
    """
    List the available user boards.
    """

    boards = db.list_user_boards(g.db, session['user'])
    user = db.get_user(g.db, session['user'])
    return render_template('view_board.html', boards=boards, function='list_many' if many else 'list',
                           root=False, user=user)


@app.route('/view/last')
@must_login(PERM_CREATE_BOARD)
def view_last_boards():
    """
    View the last created boards.
    """
    if 'last_boards' not in session:
        flash('You have not created any board in this session', 'info')
        return redirect(url_for('view_board'))
    return redirect(url_for('view_set_of_boards', board_ids=session['last_boards'], solution=False))


@app.route('/view')
@must_login(PERM_CREATE_BOARD)
def view_board():
    """
    View a board.
    """
    if 'board_id' in request.args:
        is_solution = bool(request.args.get('solution', False))
        return redirect(url_for('view_specific_board', board_id=request.args['board_id'], solution=is_solution))

    user = db.get_user(g.db, session['user'])
    return render_template('view_board.html', function='main', root=False, user=user)


@app.route('/view/<int:board_id>', defaults={'solution': False})
@app.route('/view/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def view_specific_board(board_id, solution):
    """
    View one board insite.
    """
    return view_one_board(board_id, solution, INSITE_BOARD_VIEW, False)


@app.route('/print/<int:board_id>', defaults={'solution': False})
@app.route('/print/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_specific_board(board_id, solution):
    """
    Print one board.
    """
    return view_one_board(board_id, solution, PRINT_BOARD_VIEW, False)


@app.route('/pdf/<int:board_id>', defaults={'solution': False})
@app.route('/pdf/solutions/<int:board_id>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_specific_board(board_id, solution):
    """
    Get the PDF of one board.
    """
    return 'Not supported (yet)'


@app.route('/view/custom', methods=['POST'])
@must_login(PERM_CREATE_BOARD)
def view_set():
    """
    Get the reslts of the 'View set of boards' form, and redirect to the right location.
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
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, INSITE_BOARD_VIEW, False)


@app.route('/print/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/print/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def print_set_of_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return view_many_boards(board_ids, solution, PRINT_BOARD_VIEW, False)


@app.route('/pdf/custom/<list:board_ids>', defaults={'solution': False})
@app.route('/pdf/solution/custom/<list:board_ids>', defaults={'solution': True})
@must_login(PERM_CREATE_BOARD)
def pdf_set_of_boards(board_ids, solution):
    """
    View a set of boards insite.
    """
    return 'Not implemented (yet)'
