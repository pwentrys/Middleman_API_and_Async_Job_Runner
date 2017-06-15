from pprint import pprint

from flask import Flask
from flask import render_template, redirect
from flask_cors import cross_origin

from config.credentials import UKEY
from config.strings import Strings as s
from config.templates import Templates
from utils.flask_extensions import add_url_vars, add_url_vars_html

t = Templates(__file__)


def app_routes(app, appname):
    assert isinstance(app, Flask)
    app.t = t

    # ---------------------------------------------------------------------------- #
    #                                                                              #
    #                           Landing Page                                       #
    #                                                                              #
    # ---------------------------------------------------------------------------- #
    @app.route(s.slash)
    @cross_origin()
    def index():
        return """
            Testy test
        """
    add_url_vars(app, s.index, index)

    @cross_origin()
    def toast():
        app.toaster.toast_args({})
        return """
            Testy test
        """
    add_url_vars(app, 'toast', toast)

    @cross_origin()
    def toast_message(message):
        app.toaster.toast_args({'msg': message})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:message>', toast_message)

    @cross_origin()
    def toast_title_message(title, message):
        app.toaster.toast_args({'title': title, 'msg': message})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:title>/<string:message>', toast_title_message)

    @cross_origin()
    def toast_title_message_duration(title, message, duration):
        app.toaster.toast_args({'title': title, 'msg': message, 'duration': duration})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:title>/<string:message>/<int:duration>', toast_title_message_duration)
