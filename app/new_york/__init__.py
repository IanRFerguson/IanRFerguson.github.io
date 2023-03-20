from flask import Blueprint

bp = Blueprint("new_york", __name__)

from app.new_york import routes
