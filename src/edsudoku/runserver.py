"""
Entry point for running the server as a standalone server.
"""

from edsudoku.server import app

__author__ = 'Eli Daian <elidaian@gmail.com>'

if __name__ == '__main__':
    app.run(debug=True)