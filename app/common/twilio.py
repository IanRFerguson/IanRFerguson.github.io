#!/bin/python3
import os
import json
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import random
import logging

from app import here
from app.common.bigquery import BQHelper

load_dotenv(os.path.join(here, ".env"))
logging.basicConfig(level=logging.INFO)

##########

sid = os.environ.get("TWILIO_ACCOUNT_SID")
token = os.environ.get("TWILIO_AUTH_TOKEN")
my_number = os.environ.get("TWILIO_NUMBER")

client = Client(sid, token)
bq = BQHelper()


def receive_request(**kwargs):
    """
    This function is invoked in the /sms route. We will
    send a customized message to the user depending on the
    nature of the text
    """

    # Only respond to messages from Ian
    if kwargs["from_"] == "+17038190646":

        message_body = kwargs["body"].strip().lower()

        if message_body == "miles":
            outgoing_wrapper(message_type="miles")

        else:
            try:
                numeric_value = float(message_body)

            except:
                outgoing_wrapper()

    # Ingest all texts to BigQuery


def outgoing_wrapper(message_type: str = None):
    """Sends a message to Ian depending on the conditional"""

    comment = generate_nice_comment()

    if message_type == "initial":
        message_body = f"Respond to this text with your miles run today\n{comment}"

    elif message_type == "miles":
        all_miles = bq.get_all_miles(year=datetime.now().strftime("%Y"))
        message_body = f"You've run {all_miles} miles this year!\n{comment}"

    else:
        message_body = (
            "I don't have a good answer for that, but I hope you have a nice day!"
        )

    message = client.messages.create(
        body=message_body,
        from_=my_number,
        to="+17038190646",
    )


def generate_nice_comment() -> str:
    """Picks a nice thing to say at random"""

    pool = [
        "Keep up the good work!",
        "I'm proud of you big dog!",
        "You're the fucking man!",
    ]

    return random.choice(pool)
