from flask import Blueprint

bp = Blueprint("global", __name__)

from app.housing import routes
