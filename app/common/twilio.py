#!/bin/python3
import os
import json
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import random
import logging
from time import sleep

from app import here
from app.common.bigquery import BQHelper
from app.food.helpers import process_food_items

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
        logging.info(message_body)

        try:
            k = float(message_body)
            can_parse = True
        except:
            can_parse = False

        if message_body == "miles":
            outgoing_wrapper(message_type="initial")

        elif "month" in message_body.lower():
            outgoing_wrapper(message_type="month")

        elif "food" in message_body.lower():
            process_food_items(message_body)

        elif can_parse:
            # Numeric representation of text body
            numeric_value = float(message_body)

            # All miles run in warehouse
            all_miles = (
                bq.get_all_miles(year=datetime.now().strftime("%Y")) + numeric_value
            )

            outgoing_wrapper(message_type="miles", all_miles=all_miles)

        else:
            outgoing_wrapper()

    # Ingest all texts to BigQuery
    payload = {
        "created": kwargs["time"],
        "sent_to": kwargs["to"],
        "sent_from": kwargs["from_"],
        "body": kwargs["body"],
    }

    bq.push_to_db(payload=payload)


def outgoing_wrapper(message_type: str = None, all_miles: float = None):
    """Sends a message to Ian depending on the conditional"""

    comment = generate_nice_comment()

    if message_type == "initial":
        message_body = f"Respond to this text with your miles run today\n\n{comment}"

    elif message_type == "miles":
        all_miles = round(all_miles, 2)
        message_body = f"You've run {all_miles} miles this year!\n\n{comment}"

    elif message_type == "month":
        bq = BQHelper()
        this_month = round(bq.get_miles_this_month(), 2)
        message_body = f"You've run {this_month} miles this month!\n\n{comment}"

    else:
        message_body = (
            "I don't have a good answer for that, but I hope you have a nice day!"
        )

    try:
        message = client.messages.create(
            body=message_body,
            from_=my_number,
            to="+17038190646",
        )

        return 0

    except Exception as e:
        logging.error(e)
        return 1


def generate_nice_comment() -> str:
    """Picks a nice thing to say at random"""

    pool = [
        "Keep up the good work!",
        "I'm proud of you big dog!",
        "You're the fucking man!",
        "I think you're amazing!",
        "You fucking rule",
        "Wow, you are cool and good!",
        "Fuck yes! Fuck! YES!",
        "You rule!",
        "Wow, look at you go!",
    ]

    return random.choice(pool)
