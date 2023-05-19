#!/bin/python3
import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import logging

from app import here

load_dotenv(os.path.join(here, ".env"))
logging.basicConfig(level=logging.INFO)

##########


class BQHelper:
    """
    Simple wrapper to intake and process data to Google BigQuery
    """

    def __init__(self, dataset_id: str = "web", table_id: str = "miles"):
        # Production routing
        json_path_exists = os.path.exists(
            "/home/ianfergusonNYU/00_PACKETS/service.json"
        )

        creds_in_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        ###

        if not json_path_exists and creds_in_env:
            logging.info("Using environment variable for Google creds...")

            # Read in JSON data stored in .env
            self.__creds = service_account.Credentials.from_service_account_info(
                json.loads(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
            )

        elif json_path_exists:
            logging.info("Loading creds from PythonAnywhere...")

            # Read in JSON data stored in local file
            self.__creds = service_account.Credentials.from_service_account_file(
                "/home/ianfergusonNYU/00_PACKETS/service.json"
            )

        self.__creds = self.__creds.with_scopes(
            ["https://www.googleapis.com/auth/cloud-platform"]
        )

        ###

        self.client = bigquery.Client(project="ian-is-online", credentials=self.__creds)
        self.dataset = dataset_id
        self.table = table_id

    def credentials(self) -> dict:
        """Reads credentials from production environment"""

        raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        loaded = json.loads(raw)

        return ServiceAccountCredentials.from_json_keyfile_dict(loaded, scopes=scopes)

    def query(self, sql: str) -> None:
        """
        Wrapper for the bigquery.Client.query function

        Args
            sql: str
            Valid SQL to execute on BigQuery
        """

        query_job = self.client.query(sql)
        result = query_job.result()

        if result:
            return [x for x in result]

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

    def get_miles_this_month(self) -> float:
        """Queries all miles run in the current month"""

        base_query = f"""
        with base as (
            select
                extract(year from created) as year,
                extract(month from created) as month, 
                body
            from `ian-is-online.web.miles`
            where sent_from = '+17038190646'
            and safe_cast(body as float64) is not null
        )

        select sum(safe_cast(body as float64)) from base
        where year = extract(year from current_date())
        and month = extract(month from current_date())
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
