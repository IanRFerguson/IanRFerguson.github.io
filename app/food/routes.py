from flask import render_template, redirect, request
from app.food import bp

###########


@bp.route("/", methods=["GET"])
def fd_landing():
    return render_template("food_diary.index.html")
