from flask import render_template, request
import logging
from time import sleep
from datetime import datetime

from app.routes import bp
from app.common.twilio import receive_request

logging.basicConfig(level=logging.INFO)

##########


@bp.route("/", methods=["GET", "POST"])
@bp.route("/home", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@bp.route("/acadmic_projects", methods=["GET"])
def academics():
    return render_template("academics.html")


@bp.route("/sms", methods=["POST"])
def sms():
    """This endpoint will receive incoming SMS POST requests from Twilio"""

    # receive_request()
    sent_to = request.form["To"]
    sent_from = request.form["From"]
    sent_body = request.form["Body"]
    current_time = datetime.now()

    try:
        receive_request(to=sent_to, from_=sent_from, body=sent_body, time=current_time)
        return "Success"

    except Exception as e:
        logging.error(e)
        return "Failure"


@bp.route("/rebuild_twilio", methods=["GET", "POST"])
def rebuild_twilio():
    from app.dev.twilio_rebuild import main as rebuild

    # Trigger sync from Twilio to BigQuery
    rebuild()

    return "Success"
