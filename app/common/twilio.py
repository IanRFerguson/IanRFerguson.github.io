#!/bin/python3
import os
import json
import twilio
from dotenv import load_dotenv

from app import here

load_dotenv(os.path.join(here, ".env"))

##########


class TwilioHelper:
    """
    Simple wrapper to manage incoming messages
    """

    def __init__(self):
        pass
