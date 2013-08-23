"""
util.py

 Created on: Aug 23 2013
     Author: eli
"""

class ErrorWithMessage(Exception):
    """
    This exception has a message to be passed to the viewer.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the object.
        """
        super(ErrorWithMessage, self).__init__(self, *args, **kwargs)
