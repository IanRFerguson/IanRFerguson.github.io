from flask import Blueprint

bp = Blueprint("food", __name__)

from app.food import routes
