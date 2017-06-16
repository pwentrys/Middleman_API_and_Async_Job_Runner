# --------------------------------------------------------------------------- #
#                                                                             #
#                           Core Imports                                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from datetime import timedelta

from flask import Flask

from sql.mysql import Connection as mysql

from config.configuration import config as _config
from config.strings import Strings as s
from routes import app_routes as setup_routes
from utils.toaster import Toaster

# --------------------------------------------------------------------------- #
#                                                                             #
#                       Default Configuration                                 #
#                                                                             #
# --------------------------------------------------------------------------- #

_app = Flask(
    __name__,
    static_url_path=s.empty,
    template_folder=s.templates,
    static_folder=s.static
)

_app._config = _config
_app.__name__ = _config.name
_app.config.from_object(__name__)

_app.config.update(
    SESSION_COOKIE_DOMAIN=_config.cookie.domain,
    SESSION_COOKIE_NAME=_config.cookie.name,
    DEBUG=_config.debug
)

_app.debug = _config.debug

_app.secret_key = _config.web.active.secret_key
_app.permanent_session_lifetime = timedelta(days=_config.web.active.lifetime)
_app.toaster = Toaster()
_app.sql = mysql(_config.sql.mysql, _app.toaster)

setup_routes(_app, _app.__name__)
