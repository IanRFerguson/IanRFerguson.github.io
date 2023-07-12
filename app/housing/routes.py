from flask import render_template, redirect, url_for
import logging

from app.housing import bp
from app.housing.helpers import get_rendered_map, isolate_values, build_map

logging.basicConfig(level=logging.INFO)

##########


@bp.route("/", methods=["GET", "POST"])
def index():
    """
    Main landing page for the housing routes
    """

    return render_template("housing/index.html")


@bp.route("/global_map", methods=["GET"])
def global_map():
    return render_template("housing/map__global.html")


@bp.route("/render/<year>", methods=["GET", "POST"])
def year(year: str):
    """
    Template route for each housing entry
    """

    packet = isolate_values(year=year)
    map_path = get_rendered_map()

    return render_template("housing/render.html", packet=packet, map_path=map_path)


@bp.route("/build_map", methods=["GET", "POST"])
def create_map_from_scratch():
    logging.info("Creating global map from scratch...")
    build_map()

    return redirect(url_for("main.index"))
