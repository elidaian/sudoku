#!/usr/bin/python

"""
generate_secret_key.py

 Created on: Sep 19 2013
     Author: eli
"""

import optparse
import os

try:
    from server import app
except ImportError:
    from sudoku_server import app

SECRET_KEY_FILE = app.config["SECRET_KEY_FILE"]

def init_db(root_user, root_password):
    """
    Initialize the application DB.
    """
    db.init_db(app, root_user, root_password)

def create_parser():
    """
    Create an argument parser.
    """
    parser = optparse.OptionParser(description="Initialize oldserver secret key")
    parser.add_option("-l", "--length",
                      default=128,
                      metavar="LENGTH`",
                      dest="length",
                      type=int,
                      help="Length of the secret key (in bytes)")
    return parser

def main():
    """
    Main entry point.
    """
    args, _ = create_parser().parse_args()
    
    print "Generating a secret key with %d bytes..." % args.length
    with open(SECRET_KEY_FILE, "wb") as f:
        f.write(os.urandom(args.length))
    print "Done!"    

if __name__ == "__main__":
    main()

