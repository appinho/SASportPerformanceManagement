import os
from garminconnect import Garmin
import logging

def get_mfa():
    """Get MFA."""

    return input("MFA one-time code: ")

def connect(use_cred=True):
    print("Logging into Garmin API...")

    try:
        if use_cred:
            email  =os.getenv("GARMIN_EMAIL")
            password  =os.getenv("GARMIN_PASSWORD")
            print(email, password)
            api = Garmin(email=email, password=password, is_cn=False, prompt_mfa=get_mfa)
        else:
            tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
            api.login(tokenstore)
            api = Garmin()
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