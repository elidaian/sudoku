from flask.app import Flask

from edsudoku.server import default_config

from edsudoku.server.converters import BooleanConverter, IntegersListConverter

__author__ = 'Eli Daian <elidaian@gmail.com>'

# Create the WSGI application
app = Flask(__name__, instance_relative_config=True)

# Register custom converters
app.url_map.converters['bool'] = BooleanConverter
app.url_map.converters['list'] = IntegersListConverter

# Load application configuration:
# 1. Load the default configuration.
app.config.from_object(default_config)
# 2. Override with environmental supplied configuration
if not app.config.from_envvar('EDSUDOKU_CONF_FILE', silent=True):
    # Warn if not succeeded
    app.logger.warning('Could not load environment configuration, falling back to default')

# Import the modules that contain the pages
import edsudoku.server.login
import edsudoku.server.manage_users
import edsudoku.server.misc
import edsudoku.server.my_boards
import edsudoku.server.other_users_boards
