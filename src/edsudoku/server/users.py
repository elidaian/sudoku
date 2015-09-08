from hashlib import sha512
from os import urandom

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, BLOB

from edsudoku.server.database import Base

__author__ = 'Eli Daian <elidaian@gmail.com>'


class UserPermission(object):
    """
    Describes a permission for an operation for an user.
    """

    PERMISSIONS = []
    _curr_permission_bit = 1

    def __init__(self, name, description, is_default):
        """
        Construct a permission given its description.

        :param name: The permission name.
        :type name: str
        :param description: A brief description of this permission (will be displayed to the users).
        :type description: str
        :param is_default: Whether this permission is given by default to new users.
        :type is_default: bool
        """
        super(UserPermission, self).__init__()
        self.name = name
        self.description = description
        self.flag = UserPermission._curr_permission_bit
        self.is_default = is_default

        UserPermission.PERMISSIONS.append(self)
        UserPermission._curr_permission_bit <<= 1

    @staticmethod
    def get_mask(permissions):
        """
        :return: A mask containing the given permissions.
        :rtype: int
        """
        res = 0
        for permission in permissions:
            res |= permission.flag
        return res

    @staticmethod
    def parse_mask(mask):
        """
        :return: The permissions in the mask.
        :rtype: list of :class:`~users.UserPermission`-s
        """
        res = []
        for permission in UserPermission.PERMISSIONS:
            if permission.flag & mask:
                res.append(permission)
        return res

    def __eq__(self, other):
        """
        Checks the equality of this object to other object.

        :param other: The other permission to compare to.
        :type other: :class:`~users.UserPermission`
        :return: ``True`` iff this is the same permission as other.
        :rtype: bool
        """
        return self.flag == other.flag


# Define the permissions
PERM_CREATE_BOARD = UserPermission('CREATE_BOARD', 'Create boards', True)
""" Allow the user to create his/her own sudoku boards. """

PERM_MANAGE_USERS = UserPermission('MANAGE_USERS', 'Manage users', False)
""" Allow the user to manage the users in the server. """

PERM_SHOW_OTHER_USER_BOARDS = UserPermission('SHOW_OTHER_USERS_BOARDS',
                                             'Show other user\'s boards', False)
""" Allow the user to view the generated boards of other users. """


class User(Base):
    """
    Represents a logged in user.

    :cvar id: The user ID in the DB.
    :type id: int
    :cvar username: The username.
    :type username: str
    :cvar _password: The password (as stored in the DB).
    :type _password: buffer
    :cvar _salt: The password salt.
    :type _salt: buffer
    :cvar _display: The user display, or ``None``.
    :type _display: str
    :cvar permissions_mask: The permissions mask of this user.
    :type permissions_mask: int
    :cvar boards: The list of this user's boards.
    :type boards: list of :class:`~edsudoku.server.boards.DBBoard`-s
    """

    HASH_SIZE = 64
    SALT_SIZE = 16

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    _password = Column(BLOB(HASH_SIZE), nullable=False)
    _salt = Column(BLOB(SALT_SIZE))
    _display = Column(String)
    permissions_mask = Column(Integer, nullable=False, default=0)

    @staticmethod
    def new_user(username, password, permissions, display=None):
        """
        Create a new user (and commit it).

        :param username: The username.
        :type username: str
        :param password: The user password.
        :type password: str
        :param permissions: The user permissions.
        :type permissions: list of :class:`~edsudoku.server.users.UserPermission`-s
        :param display: The user display, or ``None``.
        :type display: str
        :return: The new registered user.
        :rtype: :class:`~edsudoku.server.users.User`
        """
        user = User(username=username)
        user.set_password(password)
        user.add_permissions(permissions)
        user.display = display
        return user

    @hybrid_property
    def permissions(self):
        """
        :return: The list of permissions of this user, given its permissions mask.
        :rtype: list of :class:`~edsudoku.server.users.UserPermission`-s
        """
        return UserPermission.parse_mask(self.permissions_mask)

    @hybrid_property
    def display(self):
        """
        :return: The display of this user, if any, or the username.
        :rtype: str
        """
        return self._display or self.username

    @display.setter
    def display(self, new_display):
        """
        Set a new display for this user.

        :param new_display: The new display of this user.
        :type new_display: str
        """
        if new_display:
            self._display = new_display
        else:
            self._display = None

    @staticmethod
    def _hash_password(password, salt):
        """
        Hash a password with a salt to protect it.

        :param password: The password.
        :type password: str
        :param salt: The password salt, or ``None`` if no salt.
        :type salt: buffer
        :return: The hashed password.
        :rtype: buffer
        """
        return buffer(sha512(buffer(password.encode('ascii')) + (salt or '')).digest())

    @staticmethod
    def _generate_salt():
        """
        :return: A strong random salt, for salting passwords.
        :rtype: buffer
        """
        return buffer(urandom(User.SALT_SIZE))

    def check_password(self, password):
        """
        Check a password for authenticating the user.

        :param password: The password to check.
        :type password: str
        :return: ``True`` iff the password matches.
        :rtype: bool
        """
        return self._hash_password(password, self._salt) == self._password

    def set_password(self, new_password):
        """
        Set a new password for this user.

        :param new_password: The new user password.
        :type new_password: str
        """
        self._salt = self._generate_salt()
        self._password = self._hash_password(new_password, self._salt)

    def set_permissions(self, permissions):
        """
        Set a set of permissions to this user.
        The permissions that were not passed won't be given to this user.

        :param permissions: The permissions to set.
        :type permissions: list of :class:`~edsudoku.server.users.UserPermission`-s
        """
        self.permissions_mask = UserPermission.get_mask(permissions)

    def add_permission(self, permission):
        """
        Add a permission to this user.

        :param permission: The permission to add.
        :type permission: :class:`~edsudoku.server.users.UserPermission`
        """
        self.add_permissions([permission])

    def add_permissions(self, permissions):
        """
        Add some permissions to this user.

        :param permissions: The permissions to add.
        :type permissions: list of :class:`~edsudoku.server.users.UserPermission`-s
        """
        self.permissions_mask |= UserPermission.get_mask(permissions)

    def remove_permission(self, permission):
        """
        Remove a permission of this user.

        :param permission: The permission to remove.
        :type permission: :class:`~edsudoku.server.users.UserPermission`
        """
        self.remove_permissions([permission])

    def remove_permissions(self, permissions):
        """
        Remove some permissions of this user.

        :param permissions: The permissions to remove.
        :type permissions: list of :class:`~edsudoku.server.users.UserPermission`-s
        """
        self.permissions_mask &= ~UserPermission.get_mask(permissions)

    def has_permission(self, permission):
        """
        Check if this user has a permission.

        :param permission: The permission to check on.
        :type permission: :class:`~users.UserPermission`
        :return: ``True`` iff this user has the requested permission.
        :rtype: bool
        """
        return bool(self.permissions_mask & permission.flag)

    def allow_create_board(self):
        """
        :see: :data:`~edsudoku.server.users.PERM_CREATE_BOARD`

        :return: ``True`` iff this user is allowed to create boards.
        :rtype: bool
        """
        return self.has_permission(PERM_CREATE_BOARD)

    def allow_manage_users(self):
        """
        :see: :data:`~edsudoku.server.users.PERM_MANAGE_USERS`

        :return: ``True`` iff this user is allowed to manage other users.
        :rtype: bool
        """
        return self.has_permission(PERM_MANAGE_USERS)

    def allow_other_user_boards(self):
        """
        :see: :data:`~edsudoku.server.users.PERM_SHOW_OTHER_USER_BOARDS`

        :return: ``True`` iff this user is allowed to see other users boards.
        :rtype: bool
        """
        return self.has_permission(PERM_SHOW_OTHER_USER_BOARDS)
