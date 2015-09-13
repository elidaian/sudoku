from flask.globals import session, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from edsudoku.server import app
from edsudoku.server.database import commit
from edsudoku.server.misc import must_login
from edsudoku.server.users import PERM_MANAGE_USERS, UserPermission, User

__author__ = 'Eli Daian <elidaian@gmail.com>'


@app.route('/register', methods=['GET', 'POST'])
@must_login(PERM_MANAGE_USERS)
def register_user():
    """
    Register a new user account.

    * If this page was requested with a GET method, the new user registration form will be shown.
    * If this page was requested with a POST method, a registration form is processed.

    In any case, a registration form is returned.

    :return: The registration form.
    :rtype: flask.Response
    """
    user = User.get_by_id(session['user'])

    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        password2 = request.form.get('password2', None)

        if not username:
            flash('Username cannot be empty', 'danger')
            return redirect(url_for('register_user'))
        if not password:
            flash('Password cannot be empty', 'warning')
            return redirect(url_for('register_user'))
        if password != password2:
            flash('Passwords do not match', 'warning')
            return redirect(url_for('register_user'))

        display = request.form.get('display', None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]

        try:
            User.new_user(username, password, permissions, display).add()
            commit()
        except:
            flash('Unable to register %s' % username, 'danger')
        else:
            flash('User %s successfully created!' % username, 'success')

    return render_template('register.html', user=user, permissions=UserPermission.PERMISSIONS)


@app.route('/manage')
@must_login(PERM_MANAGE_USERS)
def manage_users():
    """
    Manage the other users.

    This page lists the available users, with buttons to edit and remove the users.

    :return: The page.
    :rtype: flask.Response
    """
    users = User.query().all()
    user = User.get_by_id(session['user'])
    return render_template('list_users.html', users=users, user=user)


@app.route('/manage/<int:user_id>', methods=['GET', 'POST'])
@must_login(PERM_MANAGE_USERS)
def edit_user(user_id):
    """
    Edit a user.

    * If this page was requested with GET method, the user editing form is displayed.
    * If this page was requested with a POST method, a user editing is processed.

      * If the form was processed successfully, the user is redirected to the management page
        (see :func:`~edsudoku.server.manage_users.manage_users`).
      * Otherwise, the form is returned with an error explanation.

    :param user_id: The user ID to edit.
    :type user_id: int
    :return: As explained above.
    :rtype: flask.Response
    """
    user = User.get_by_id(session['user'])

    edited_user = User.get_by_id(user_id)
    if not edited_user:
        flash('User not found', 'danger')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        password = request.form.get('password', None)
        display = request.form.get('display', None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]

        if password:
            if password != request.form.get('password2', None):
                flash('Passwords mismatch', 'warning')
                return redirect(url_for('edit_user', user_id=user_id))
            edit_user.set_password(password)

        edited_user.display = display
        edited_user.set_permissions(permissions)

        commit()

        flash('User updated successfully', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user, edited_user=edited_user,
                           permissions=UserPermission.PERMISSIONS)


@app.route('/manage/delete/<int:user_id>', methods=['GET', 'POST'])
@must_login(PERM_MANAGE_USERS)
def delete_user(user_id):
    """
    Delete a user.

    This page can be requested in both GET and POST methods:

    * If this page was requested with GET method, a form that confirms that this user should be removed is returned.
    * If this page was requested with POST method, the validation form is checked. If it is validated successfully.
        Later (even if the user was not deleted) the user is redirected to the management page (see
        :meth:`~edsudoku.server.manage_users.manage_users`).

    :param user_id: The user ID to be deleted.
    :type user_id: int
    :return: As explained above.
    :rtype: flask.Response
    """
    user_to_delete = User.get_by_id(user_id)
    if not user_to_delete:
        flash('User not found', 'danger')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        user_id2 = int(request.form.get('user_id', -1))
        approved = bool(request.form.get('approved', False))

        if approved and user_id == user_id2:
            user_to_delete.delete()
            commit()
            flash('User %s has been deleted successfully' % user_to_delete.display, 'success')
        else:
            flash('User not deleted', 'warning')
        return redirect(url_for('manage_users'))

    user = User.get_by_id(session['user'])
    return render_template('delete_user.html', user=user, user_to_delete=user_to_delete)
