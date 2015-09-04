import os

from flask.app import Flask

from sudoku.server.converters import BooleanConverter, IntegersListConverter

__author__ = "Eli Daian <elidaian@gmail.com>"

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("sudoku.cfg", silent=True)
app.url_map.converters["bool"] = BooleanConverter
app.url_map.converters["list"] = IntegersListConverter

if not os.path.isfile(app.config["DATABASE"]):
    app.config["DATABASE"] = os.path.join(app.instance_path, app.config["DATABASE"])

# Import the modules that contain the pages
import sudoku.server.login
import sudoku.server.manage_users
import sudoku.server.my_boards
import sudoku.server.other_users_boards
