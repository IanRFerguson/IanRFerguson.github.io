#!/bin/python3
import os, pathlib
from time import sleep
from app import here
from app.new_york import bp
from app.new_york.helper.map import MapHandler
from app.new_york.helper.db import handle_request, init_db, read_db, update_rank
from pandas.io.sql import DatabaseError

from flask import (
    render_template,
    request,
    redirect,
    send_file,
    url_for,
    flash,
)


if not os.path.exists(os.path.join(here, "new_york", "nyc.db")):
    init_db(here=os.path.join(here, "new_york"))


##########


@bp.route("/", methods=["GET", "POST"])
def index():

    if not os.path.exists("./app/templates/hotspots.html"):
        dummy = open("./app/templates/hotspots.html", "w")
        dummy.close()

    return render_template("new_york/index.html")


@bp.route("/add_hotspot", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        venue_ = request.form["venue_name"]
        address_ = request.form["street_address"]
        city_ = request.form["city"]
        venue_type_ = request.form["venue_type"]
        submitted_by = request.form["submitted_by"]
        comments = request.form["comments"]

        address_string = f"{address_}, {city_}, NY"

        try:
            handle_request(
                address=address_string,
                label_=venue_,
                submitted_by=submitted_by,
                comments=comments,
                venue_type=venue_type_,
            )

        except Exception as e:
            flash(e)
            return redirect(url_for("new_york.index"))

        return render_template("new_york/success.html", address=address_string.upper())

    try:
        return render_template("new_york/add.html")

    except DatabaseError as e:
        flash(e)
        return redirect(url_for("new_york.index"))


@bp.route("/view_hotspots", methods=["GET", "POST"])
def view():
    data = read_db()

    try:
        return render_template("new_york/view.html", data=data.values.tolist())

    except DatabaseError as e:
        flash(e)
        return redirect(url_for("new_york.index"))


@bp.route("/upvote", methods=["GET", "POST"])
def upvote():
    data = read_db()

    feed = []

    for ix, label_ in enumerate(data["label"]):
        clean = f"{label_} - {data['address'][ix]}"
        feed.append(clean)

    if request.method == "POST":
        choice = request.form["upvote_choice"]

        choice = [x.strip() for x in choice.split("-")]

        print(f"{choice[0]}\t\t{choice[1]}")
        sleep(10)

        update_rank(choice[0], choice[1])

        flash(f"{choice[0]} updated!")

        return redirect(url_for("new_york.index"))

    try:
        return render_template("new_york/upvote.html", data=feed)

    except DatabaseError as e:
        flash(e)
        return redirect(url_for("new_york.index"))


@bp.route("/hotspots", methods=["GET", "POST"])
def hotspots():
    return render_template("new_york/hotspots.html")


@bp.route("/download_csv", methods=["GET", "POST"])
def download_csv():
    data = read_db()

    here = pathlib.Path(__file__).parent

    output_path = os.path.join(here, ".temp_cache")
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    data.to_csv(os.path.join(output_path, "NYC_WIFI_HOTSPOTS.csv"), index=False)

    return send_file(
        os.path.join(output_path, "NYC_WIFI_HOTSPOTS.csv"), as_attachment=True
    )
