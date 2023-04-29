#!/bin/python3
from flask import Flask
import os
import logging

logging.basicConfig(level=logging.INFO)

##########

here = os.path.abspath(os.path.dirname(__file__))
logging.info(f"Path exists: {os.path.exists(os.path.join(here, '.env'))}")


def create_app():
    app = Flask(__name__)

    # Register blueprints
    from app.routes import bp as main_routes

    app.register_blueprint(main_routes)

    ### - Miles tracker
    from app.miles import bp as miles

    app.register_blueprint(miles, url_prefix="/miles")

    return app
