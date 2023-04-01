#!/bin/python3
import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging

from app import here

load_dotenv(os.path.join(here, ".env"))
logging.basicConfig(level=logging.INFO)

##########


class BQHelper:
    """
    Simple wrapper to intake and process data to Google BigQuery
    """

    def __init__(self):
        self.client = bigquery.Client(credentials=self.credentials)
        self.dataset = "web"
        self.table = "miles"

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

    def get_all_miles(year: int) -> float:
        """Queries all miles run for a given year"""

        pass

    def push_to_db(
        self,
        body: str,
        created_at: datetime,
        from_: str = "+17038190646",
        to: str = "+18043732715",
    ):
        """Writes a new row to BigQuery database"""

        table = self.client
