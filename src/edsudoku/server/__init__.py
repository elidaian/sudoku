import os

from flask.app import Flask

from edsudoku.server.converters import BooleanConverter, IntegersListConverter

__author__ = 'Eli Daian <elidaian@gmail.com>'

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('sudoku.cfg', silent=True)
app.url_map.converters['bool'] = BooleanConverter
app.url_map.converters['list'] = IntegersListConverter

if not os.path.isfile(app.config['DATABASE']):
    app.config['DATABASE'] = os.path.join(app.instance_path, app.config['DATABASE'])

# Import the modules that contain the pages
import edsudoku.server.login
import edsudoku.server.manage_users
import edsudoku.server.misc
import edsudoku.server.my_boards
import edsudoku.server.other_users_boards
