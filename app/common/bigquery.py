#!/bin/python3
import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging
from time import sleep

from app import here

load_dotenv(os.path.join(here, ".env"))
logging.basicConfig(level=logging.INFO)

##########


class BQHelper:
    """
    Simple wrapper to intake and process data to Google BigQuery
    """

    def __init__(self, dataset_id: str = "web", table_id: str = "miles"):

        creds = json.loads(os.environ.get("GOOGLE_SERVICE_CREDS"))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds

        self.client = bigquery.Client()
        self.dataset = dataset_id
        self.table = table_id

    def credentials(self) -> dict:
        """Reads credentials from production environment"""

        raw = os.environ.get("GOOGLE_SERVICE_CREDS")
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        loaded = json.loads(raw)

        return ServiceAccountCredentials.from_json_keyfile_dict(loaded, scopes=scopes)

    def get_all_miles(self, year: int) -> float:
        """Queries all miles run for a given year"""

        base_query = f"""
        with base_query as (
            select 
                created,
                sent_to,
                sent_from,
                body
            from `ian-is-online.web.miles`
            where extract(year from created) = {year}
            and sent_from = '+17038190646'
            and safe_cast(body as float64) is not null
            )

            select sum(safe_cast(body as float64)) from base_query
        """

        result = self.client.query(base_query)
        result = [x[0] for x in result.result()]

        return float(result[0])

    def push_to_db(self, payload: list):
        """Writes a new row to BigQuery database"""

        table = self.client.get_table(
            self.client.dataset(self.dataset).table(self.table)
        )

        if type(payload) == dict:
            payload = [payload]

        errors = self.client.insert_rows(rows=payload, table=table)

        if len(errors) == 0:
            logging.info(f"Successfully logged {len(payload)} rows to warehouse")

        else:
            logging.error("FAILED TO UPLOAD")

            for e in errors:
                logging.error(e)
