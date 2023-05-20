from flask import render_template, redirect, request
from datetime import datetime
from app.food import bp
from app.food.helpers import get_all_diary_entries, read_manifest

###########


@bp.route("/", methods=["GET"])
def fd_landing():
    entries = get_all_diary_entries()
    return render_template("food_diary/index.html", entries=entries)


@bp.route("/day/<date_stamp>", methods=["GET"])
def log(date_stamp: str):
    """
    About
    """

    items = read_manifest(date_string=date_stamp, log_sql=False)
    clean_day = datetime.strptime(date_stamp, "%Y-%m-%d").strftime("%A %B %d, %Y")
    food = items["food"]
    counts = items["count"]

    return render_template(
        "food_diary/entry.html", items=zip(food, counts), clean_day=clean_day
    )


@bp.route("/viewAllLogs", methods=["GET"])
def log_all_days():
    """
    About
    """

    items = read_manifest(log_sql=True)
    clean_day = "every damn day"
    food = items["food"]
    counts = items["count"]

    return render_template(
        "food_diary/entry.html", items=zip(food, counts), clean_day=clean_day
    )
