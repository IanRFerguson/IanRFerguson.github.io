from datetime import datetime
import logging

from app.common.bigquery import BQHelper

logging.basicConfig(level=logging.INFO)

##########


def process_food_items(body: str) -> None:
    """
    This helper performs the following operations:

    * Removes FOOD from the incoming string
    * Split into a list (sep on comma)
    * Iteratively add to BigQuery
    """

    body = body.lower().replace("food", "")

    item_list = [x for x in body.split(",")]
    logging.info(f"Identified {len(item_list)} food items...")

    bq = BQHelper(table_id="food")

    payload = [[datetime.now(), x.upper()] for x in item_list]

    bq.push_to_db(payload=payload)


def read_manifest(date_string=None, log_sql: bool = False) -> list:
    """
    Reads food data from BigQuery, cleans it, and returns
    a dictionary
    """

    base = """
    with base as (
    select
        food_item,
        extract(year from created) as year,
        format("%02d", extract(month from created)) as month,
        format("%02d", extract(day from created)) as day
    from web.food
    )

    select
    (year || '-' || month || '-' || day) as date_stamp,
    upper(food_item) as food_item,
    count(*) as count
    from base
    """

    if date_string:
        base += f" where (year || '-' || month || '-' || day) = '{date_string}'"

    base += " group by 1,2 order by 3 desc"

    if log_sql:
        logging.info("SQL call to BigQuery...")
        logging.info(base)

    ###

    bq = BQHelper(table_id="food")
    response = bq.query(sql=base)

    container = {"day": [], "food": [], "count": []}

    for r in response:
        container["day"].append(r["date_stamp"])
        container["food"].append(r["food_item"])
        container["count"].append(r["count"])

    return container


def get_all_diary_entries() -> list:
    """
    Queries BigQuery to determine the unique days
    that food has been logged
    """

    base = """
    with base as (
        select
            food_item,
            extract(year from created) as year,
            format("%02d", extract(month from created)) as month,
            format("%02d", extract(day from created)) as day
        from web.food
        order by created desc
    )

    select distinct
    (year || '-' || month || '-' || day) as date_stamp
    from base
    """

    bq = BQHelper(table_id="food")
    response = bq.query(sql=base)

    container = []

    for r in response:
        container.append(r["date_stamp"])

    return container
