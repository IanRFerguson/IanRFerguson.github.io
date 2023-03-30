#!/bin/python3
import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials

from app import here

load_dotenv(os.path.join(here, ".env"))

##########


class BQHelper:
    """
    Simple wrapper to intake and process data to Google BigQuery
    """

    def __init__(self):
        self.client = bigquery.Client(credentials=self.credentials)

    @property
    def credentials(self) -> dict:
        """
        Reads credentials from production environment
        """

        raw = os.environ.get("GOOGLE_SERVICE_CREDS")
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        with open(raw) as incoming:
            loaded = json.load(incoming)

        return ServiceAccountCredentials(loaded, scopes=scopes)
