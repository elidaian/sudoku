from flask.globals import session, g
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from edsudoku.server import db

__author__ = 'Eli Daian <elidaian@gmail.com>'

INSITE_BOARD_VIEW = 0
PRINT_BOARD_VIEW = 1


def view_one_board(board_id, solution, mode, root):
    """
    View a single board.
    """
    if root:
        board = db.get_board(g.db, board_id)
    else:
        board = db.get_user_board(g.db, board_id, session['user'])

    if board is None:
        flash('Board not found', 'warning')
        return redirect(url_for('main_page'))

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session['user'])
        return render_template('view_board.html', many=False, board=board, board_id=board_id, is_solution=solution,
                               root=root, user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template('print_board.html', multi_board=False, board=board, board_id=board_id, is_solution=solution)
    else:
        flash('Invalid mode', 'warning')
        return redirect(url_for('main_page'))


def view_many_boards(board_ids, solution, mode, root):
    """
    View many boards.
    """
    if root:
        boards = [(db.get_board(g.db, board_id), board_id) for board_id in board_ids]
    else:
        boards = [(db.get_user_board(g.db, board_id, session['user']), board_id)
                  for board_id in board_ids]

    if mode == INSITE_BOARD_VIEW:
        user = db.get_user(g.db, session['user'])
        return render_template('view_board.html', many=True, boards=boards, board_ids=board_ids, is_solution=solution,
                               root=root, user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template('print_board.html', multi_board=True, boards=boards, is_solution=solution)
    else:
        flash('Invalid mode', 'warning')
        return redirect(url_for('main_page'))
