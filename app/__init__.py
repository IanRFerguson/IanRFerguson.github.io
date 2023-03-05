#!/bin/python3
from flask import Flask
import os

##########

here = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)

    # Register blueprints
    from app.routes import bp as main_routes

    app.register_blueprint(main_routes)

    ### - Miles tracker
    from app.miles import bp as miles

    app.register_blueprint(miles, url_prefix="/miles")

    ### - New York WiFi
    from app.new_york import bp as new_york

    app.register_blueprint(new_york, url_prefix="/new_york")

    return app
