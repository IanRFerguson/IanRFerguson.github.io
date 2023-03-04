from flask import render_template, redirect, url_for
from app.routes import bp

##########


@bp.route("/", methods=["GET", "POST"])
@bp.route("/home", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@bp.route("/acadmic_projects", methods=["GET"])
def academics():
    return render_template("academics.html")
