# --------------------------------------------------------------------------- #
#                                                                             #
#                           Core Imports                                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from datetime import timedelta

from flask import Flask

from sql.mysql import Connection as sql

from config.configuration import config as c
from config.strings import Strings as s
from routes import app_routes as setup_routes
from utils.toaster import Toaster

# --------------------------------------------------------------------------- #
#                                                                             #
#                       Default Configuration                                 #
#                                                                             #
# --------------------------------------------------------------------------- #


def run():
    app = Flask(
        __name__,
        static_url_path=s.empty,
        template_folder=s.templates,
        static_folder=s.static
    )

    app.authinfo = c
    app.__name__ = c.name
    app.config.from_object(__name__)

    app.config.update(
        SESSION_COOKIE_DOMAIN=c.cookie.domain,
        SESSION_COOKIE_NAME=c.cookie.name,
        DEBUG=c.debug
    )

    app.debug = c.debug

    app.secret_key = c.web.active.secret_key
    app.permanent_session_lifetime = timedelta(days=c.web.active.lifetime)
    app.toaster = Toaster()
    app.sql = sql(c.sql.mysql, app.toaster)

    setup_routes(app, app.__name__)
    return app
