from flask.globals import g, session, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from sudoku.server import db, app
from sudoku.server.misc import must_login
from sudoku.server.users import PERM_MANAGE_USERS, UserPermission

__author__ = "Eli Daian <elidaian@gmail.com>"


@app.route("/register", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def register_user():
    """
    Register a new user account.
    """
    user = db.get_user(g.db, session["user"])

    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        password2 = request.form.get("password2", None)

        if not username:
            flash("Username cannot be empty", "danger")
            return redirect(url_for("register_user"))
        if not password:
            flash("Password cannot be empty", "warning")
            return redirect(url_for("register_user"))
        if password != password2:
            flash("Passwords do not match", "warning")
            return redirect(url_for("register_user"))

        display = request.form.get("display", None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]
        message, status = db.register_user(g.db, username, password, display, permissions)
        flash(message, "success" if status else "danger")

    return render_template("register.html", user=user, permissions=UserPermission.PERMISSIONS)


@app.route("/manage")
@must_login(PERM_MANAGE_USERS)
def manage_users():
    """
    Manage the other users.
    """
    users = db.list_users(g.db)
    user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="main", users=users, user=user)


@app.route("/manage/<int:user_id>", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def edit_user(user_id):
    """
    Edit a user.
    """
    user = db.get_user(g.db, session["user"])

    if request.method == "POST":
        password = request.form.get("password", None)
        display = request.form.get("display", None)
        permissions = [permission for permission in UserPermission.PERMISSIONS
                       if request.form.get(permission.name, None) == str(permission.flag)]

        if password:
            password2 = request.form.get("password2", None)

            if password != password2:
                flash("Passwords mismatch", "warning")
                return redirect(url_for("edit_user", user_id=user_id))

            db.edit_user_with_password(g.db, user_id, password, display, permissions)
        else:
            db.edit_user_without_password(g.db, user_id, display, permissions)

        flash("User updated successfully", "success")
        return redirect(url_for("manage_users"))

    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    edited_user, num_boards = user_details

    return render_template("manage.html", function="edit", user=user, user_id=user_id, edited_user=edited_user,
                           num_boards=num_boards, permissions=UserPermission.PERMISSIONS)


@app.route("/manage/delete/<int:user_id>", methods=["GET", "POST"])
@must_login(PERM_MANAGE_USERS)
def delete_user(user_id):
    """
    Delete a user.
    """
    user_details = db.get_user_details(g.db, user_id)
    if not user_details:
        flash("User not found", "danger")
        return redirect(url_for("manage_users"))
    user_to_delete, num_boards = user_details

    if request.method == "POST":
        user_id2 = int(request.form.get("user_id", -1))
        approved = bool(request.form.get("approved", False))

        if approved and user_id == user_id2:
            db.delete_user(g.db, user_id)
            flash("User %s has been deleted successfully" % user_to_delete.display, "success")
        else:
            flash("User not deleted", "warning")
        return redirect(url_for("manage_users"))

    user = db.get_user(g.db, session["user"])
    return render_template("manage.html", function="delete", user=user, user_to_delete=user_to_delete,
                           num_boards=num_boards, user_id=user_id)
