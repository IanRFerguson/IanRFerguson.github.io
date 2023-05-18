from datetime import datetime
from app.common.bigquery import BQHelper

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

    # Loop through these and write to Bigquery
