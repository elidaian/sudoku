from flask.globals import session, g, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from sudoku.server import db, app

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.route('/')
def main_page():
    """
    Webserver index page.

    :return: The main page.
    :rtype: flask.Response
    """
    if session.get('logged_in', False):
        user = db.get_user(g.db, session['user'])
    else:
        user = None
    return render_template('main_page.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Show the login page and handle login requests.

    :return: The login page.
    :rtype: flask.Response
    """
    if request.method == 'POST':
        try:
            username = request.form.get('username', None)
            password = request.form.get('password', None)

            if username is None or password is None:
                flash('Invalid data', 'danger')
                return redirect(url_for('login'))

            user = db.login(g.db, username, password)
            if user is None:
                flash('Invalid login credentials', 'danger')
            else:
                flash('You were logged in successfully!', 'success')
                session['logged_in'] = True
                session['user'] = user.id

                if request.args.get('next', None):
                    return redirect(request.args['next'])
                return redirect(url_for('main_page'))
        except KeyError:
            flash('Missing username or password', 'info')
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Log out and end the current session (if any).
    Later redirect to the main page (see :meth:`~sudoku.server.login.main_page`).

    :return: A redirection.
    :rtype: flask.Response
    """
    session.clear()
    session['logged_in'] = False
    return redirect(url_for('main_page'))
