#!/bin/python3
import pandas as pd
from app.common.bigquery import BQHelper
from app.common.twilio import client

##########


def build_response_dict() -> dict:
    """
    Queries Twilio API for historical view
    of SMS I/O
    """

    # Container to append into
    container = []

    # Loop through all Twilio message objects
    # and add to container
    for response in client.messages.list():
        container.append(
            {
                "created": response.day_created,
                "sent_to": response.to,
                "sent_from": response.from_,
                "body": response.body,
            }
        )

    return container


def build_clean_df(incoming: dict) -> list:
    """
    Converts response dictionary to Pandas DataFrame
    for easy cleaning
    """

    df = pd.DataFrame(incoming)

    # Add boolean filters
    df["is_food_log"] = df["body"].apply(lambda x: "FOOD" in x.upper())
    df["is_from_ian"] = df["sent_from"].apply(lambda x: x == "+17038190646")

    # Filter unwanted data
    rdf = (
        df[(df["is_food_log"] == False) & (df["is_from_ian"] == True)]
        .sort_values(by="created")
        .reset_index(drop=True)
    )

    # Limit to relevant columns
    rdf = rdf.loc[:, ["created", "sent_to", "sent_from", "body"]]

    # Return list of dictionaries with complete key:value pairs
    return rdf.to_dict("records")


def write_to_bigquery(incoming: list) -> None:
    """
    Writes cleaned list of responses to BigQuery
    using helper functions
    """

    bq = BQHelper()
    bq.push_to_db(payload=incoming)


def main():
    # Get dictionary of responses
    responses = build_response_dict()

    # Clean up and filter responses
    clean_list = build_clean_df(incoming=responses)

    # Push clean list to BigQuery
    write_to_bigquery(incoming=clean_list)


#####

if __name__ == "__main__":
    main()
