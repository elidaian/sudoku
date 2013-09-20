"""
configure_server.py

 Created on: Sep 19 2013
     Author: eli
"""

import getpass
import optparse
import os

import db
from server import app

def init_db(root_user, root_password):
    """
    Initialize the application DB.
    """
    db.init_db(app, root_user, root_password)

def create_parser():
    """
    Create an argument parser.
    """
    parser = optparse.OptionParser(description="Initialize server DB with a root user")
    parser.add_option("-u", "--user",
                      default=os.environ.get("USER", None),
                      metavar="USERNAME",
                      dest="user",
                      help="Root user name")
    parser.add_option("-p", "--password",
                      default=os.environ.get("PASSWORD", None),
                      metavar="PASSWORD",
                      dest="password",
                      help="Root password (or - to read from tty)")
    return parser

def get_username_and_password(args):
    """
    Get the user name and password out of the arguments.
    """
    if args.user:
        user = args.user
    else:
        user = raw_input("What is the username? ")
    
    if args.password and args.password != "-":
        password = args.password
    else:
        password = getpass.getpass()
    
    return user, password

def main():
    """
    Main entry point.
    """
    args, _ = create_parser().parse_args()
    user, password = get_username_and_password(args)
    
    print "Initializing DB..."
    init_db(user, password)
    print "Done!"    

if __name__ == "__main__":
    main()
