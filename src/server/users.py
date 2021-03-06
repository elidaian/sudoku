"""
users.py

 Created on: Aug 17 2013
     Author: eli
"""

class UserPermission(object):
    """
    Describes a permission for an operation for an user.
    """
    
    PERMISSIONS = []
    _curr_permission_bit = 1
    
    def __init__(self, name, description, is_default):
        """
        Construct a permission given its description.
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
        Returns a mask containing the given permissions.
        """
        res = 0
        for permission in permissions:
            res |= permission.flag
        return res
    
    @staticmethod
    def parse_mask(mask):
        """
        Return a list of permissions given the mask.
        """
        res = []
        for permission in UserPermission.PERMISSIONS:
            if permission.flag & mask:
                res.append(permission)
        return res
    
    def __eq__(self, other):
        """
        Checks the equality of this object to other object.
        """
        return self.flag == other.flag

def permissions_to_mask(permissions):
    """
    Create a mask of permissions given the permissions list.
    """
    res = 0
    for permission in permissions:
        res |= permission.flag
    return res

# Define the permissions
PERM_CREATE_BOARD = UserPermission("CREATE_BOARD", "Create boards", True)
PERM_MANAGE_USERS = UserPermission("MANAGE_USERS", "Manage users", False)
PERM_SHOW_OTHER_USER_BOARDS = UserPermission("SHOW_OTHER_USERS_BOARDS",
                                             "Show other user\'s boards", False)

class User(object):
    """
    Represents a logged in user.
    """
    
    def __init__(self, id, username, display, permissions):
        """
        Initialize a user given its ID, username, display name and permissions.
        """
        super(User, self).__init__()
        self.id = id
        self.username = username
        if not display:
            self.display = username
        else:
            self.display = display
        self.permissions = UserPermission.parse_mask(permissions)
    
    def has_permission(self, permission):
        """
        Returns True if this user has the requested permission.
        """
        return permission in self.permissions
    
    def allow_create_board(self):
        """
        Returns True if this user is allowed to create boards.
        """
        return self.has_permission(PERM_CREATE_BOARD)
    
    def allow_manage_users(self):
        """
        Returns True if this user is allowed to manage other users.
        """
        return self.has_permission(PERM_MANAGE_USERS)
    
    def allow_other_user_boards(self):
        """
        Returns True if this user is allowed to see other users boards.
        """
        return self.has_permission(PERM_SHOW_OTHER_USER_BOARDS)
    
    def to_json(self):
        """
        Returns a jsonable object with the same data as this user.
        """
        return {"id"        : self.id,
                "username"  : self.username,
                "display"   : self.display,
                "permisions": permissions_to_mask(self.permissions)}

def user_from_json(json):
    """
    Create a User object from its representing json.
    """
    return User(json["id"], json["username"], json["display"], json["permissions"])

