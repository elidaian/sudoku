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


class User(object):
    """
    Represents a logged in user.
    """

    def __init__(self, id, username, display, permissions):
        """
        Initialize a user given its ID, username, display name and permissions.

        :param id: The user ID.
        :type id: int
        :param username: The username.
        :type username: str
        :param display: The user display (nickname).
        :type display: str
        :param permissions: Mask of permissions granted to the user.
        :type permissions: int
        """
        super(User, self).__init__()
        self.id = id
        self.username = username
        self.display = display or username
        self.permissions = UserPermission.parse_mask(permissions)

    def has_permission(self, permission):
        """
        Check if this user has a permission.

        :param permission: The permission to check on.
        :type permission: :class:`~users.UserPermission`
        :return: ``True`` iff this user has the requested permission.
        :rtype: bool
        """
        return permission in self.permissions

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

    def to_json(self):
        """
        :return: jsonable object with the same data as this user.
        :rtype: bool
        """
        return {'id': self.id,
                'username': self.username,
                'display': self.display,
                'permisions': UserPermission.get_mask(self.permissions)}

    @staticmethod
    def from_json(json):
        """
        Create a :class:`~users.User` object fom its representing json.

        :param json: The json data.
        :type json: dict
        :return: The corresponding :class:`~users.User` object.
        :rtype: :class:`~users.User`
        """
        return User(json['id'], json['username'], json['display'], json['permissions'])
