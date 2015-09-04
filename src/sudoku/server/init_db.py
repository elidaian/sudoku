from argparse import ArgumentParser
from getpass import getuser, getpass

from sudoku.server import app
from sudoku.server.db import init_db

__author__ = "Eli Daian <elidaian@gmail.com>"


def _parse_args():
    """
    Parse command line arguments.
    :return: The parsed arguments.
    :rtype: :class:`argparse.Namespace`
    """

    parser = ArgumentParser(description="Initialize an empty DB")
    parser.add_argument("-u", "--user",
                        default=getuser(),
                        metavar="USERNAME",
                        dest="user",
                        help="Root user name")
    parser.add_argument("-p", "--password",
                        default=None,
                        metavar="PASSWORD",
                        dest="password",
                        help="Root user password")
    return parser.parse_args()


def main():
    """
    Main entry point for this script.
    """
    args = _parse_args()

    user = args.user
    password = args.password or getpass()

    print "Initializing DB..."
    init_db(app, user, password)
    print "Done!"


if __name__ == '__main__':
    main()
