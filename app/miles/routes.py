#!/bin/python3
from flask import render_template
from app.miles import bp

##########


@bp.route("/", methods=["GET", "POST"])
def index():
    return "Hello World"
