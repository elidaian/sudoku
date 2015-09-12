from flask.globals import session
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from edsudoku.server.boards import DBBoard
from edsudoku.server.pdf import render_pdf_template
from edsudoku.server.users import User

__author__ = 'Eli Daian <elidaian@gmail.com>'

# Board viewing modes

INSITE_BOARD_VIEW = 0
""" The board will be viewed inside the website. """

PRINT_BOARD_VIEW = 1
""" The board will be viewed in a printable format. """

PDF_BOARD_VIEW = 2
""" The board will be viewed as a PDF file. """


def view_one_board(board_id, solution, mode, root):
    """
    View a single board.
    """
    user = User.get_by_id(session['user'])
    board = DBBoard.get_by_id(board_id)

    if board is None or (board.user != user and not root):
        flash('Board not found', 'warning')
        return redirect(url_for('main_page'))

    if mode == INSITE_BOARD_VIEW:
        return render_template('view_board.html', many=False, board=board, board_id=board_id, is_solution=solution,
                               root=root, user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template('print_board.html', multi_board=False, board=board, board_id=board_id,
                               is_solution=solution)
    elif mode == PDF_BOARD_VIEW:
        filename = 'solution.pdf' if solution else 'board.pdf'
        return render_pdf_template('pdf_board.tex', filename, multi_board=False, board=board, board_id=board_id,
                                   is_solution=solution)
    else:
        flash('Invalid mode', 'warning')
        return redirect(url_for('main_page'))


def view_many_boards(board_ids, solution, mode, root):
    """
    View many boards.
    """
    user = User.get_by_id(session['user'])
    query = DBBoard.query().filter(DBBoard.id.in_(board_ids))
    if not root:
        query = query.filter_by(user=user)
    boards = query.all()

    if mode == INSITE_BOARD_VIEW:
        return render_template('view_board.html', many=True, boards=boards, board_ids=board_ids,
                               is_solution=solution, root=root, user=user)
    elif mode == PRINT_BOARD_VIEW:
        return render_template('print_board.html', multi_board=True, boards=boards, is_solution=solution)
    elif mode == PDF_BOARD_VIEW:
        filename = 'solution.pdf' if solution else 'board.pdf'
        return render_pdf_template('pdf_board.tex', filename, multi_board=True, boards=boards, is_solution=solution)
    else:
        flash('Invalid mode', 'warning')
        return redirect(url_for('main_page'))
