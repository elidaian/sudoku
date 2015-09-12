from functools import wraps
from os.path import join, dirname

from flask.globals import session, request
from flask.helpers import url_for, flash, send_from_directory

from werkzeug.utils import redirect

from edsudoku.server import app
from edsudoku.server.database import db_session
from edsudoku.server.users import User

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.teardown_request
def close_db(exception):
    """
    Close the DB connection after any request.
    """
    db_session.remove()


def must_login(permission=None):
    """
    Wraps a page that requires a logged in viewer.

    :param permission: If given, the viewing user must have the given permission.
    :type permission: :class:`~edsudoku.server.users.UserPermissions`
    :return: A wrapped function with this check.
    :rtype: function
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login', next=request.url))
            elif permission is not None and not User.get_by_id(session['user']).has_permission(permission):
                flash('Permission denied', 'danger')
                return redirect(url_for('main_page'))
            else:
                return func(*args, **kwargs)

        return wrapped

    return wrapper


@app.route('/fonts/<path:filename>')
def get_font(filename):
    """
    Get a file from the fonts directory.

    :param filename: The filename.
    :type filename: str
    :return: The font file.
    :rtype: flask.Response
    """
    return send_from_directory(join(dirname(__file__), 'fonts'), filename)
