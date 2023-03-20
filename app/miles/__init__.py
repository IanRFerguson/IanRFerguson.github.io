from flask import Blueprint

bp = Blueprint("miles", __name__)

from app.miles import routes
