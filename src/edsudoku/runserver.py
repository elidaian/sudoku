"""
Entry point for running the server as a standalone server.
"""

from edsudoku.server import app

__author__ = 'Eli Daian <elidaian@gmail.com>'


def main():
    """
    Main entry point for running the server as a standalone.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()
