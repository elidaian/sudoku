from argparse import ArgumentParser
from getpass import getuser, getpass

from edsudoku.server import app

from edsudoku.server.database import Base, engine, commit
from edsudoku.server.users import User, UserPermission

__author__ = 'Eli Daian <elidaian@gmail.com>'


def _parse_args():
    """
    Parse command line arguments.

    :return: The parsed arguments.
    :rtype: :class:`argparse.Namespace`
    """

    parser = ArgumentParser(description='Initialize an empty DB')
    parser.add_argument('-u', '--user',
                        default=getuser(),
                        metavar='USERNAME',
                        dest='user',
                        help='Root user name')
    parser.add_argument('-p', '--password',
                        default=None,
                        metavar='PASSWORD',
                        dest='password',
                        help='Root user password')
    return parser.parse_args()


def main():
    """
    Main entry point for this script.
    """
    args = _parse_args()

    user = args.user
    password = args.password or getpass()

    print 'Initializing DB...'
    Base.metadata.create_all(bind=engine)
    with app.app_context():
        User.new_user(user, password, UserPermission.PERMISSIONS).add()
        commit()
    print 'Done!'


if __name__ == '__main__':
    main()
