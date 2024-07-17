import os
from garminconnect import Garmin
import logging

def connect():
    print("Logging into Garmin API...")

    try:
        tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
        print(tokenstore)
        api = Garmin()
        api.login(tokenstore)
        print("Logged into Garmin API.")
        return api
    except Exception as e:
        logging.error(f"Couldn't log in to Garmin API: {e}")
        return None

def download(sports, start, end):
    pass

if __name__ == "__main__":
    print("Garmin API")
    connect()