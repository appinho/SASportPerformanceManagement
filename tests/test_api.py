from data_feed.garmin_api import connect

import logging

logging.basicConfig(level=logging.INFO)

def test_api_connection():

    try:
        api = connect()
    except Exception as err:
        logging.error(f"Error connecting to Garmin API: {err}")
        assert False
    assert api is not None

test_api_connection()