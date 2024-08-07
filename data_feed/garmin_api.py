import argparse
import datetime
import logging
import os

import requests
from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError

from database.write import write_vo2max

SPORTS = ["cycling", "running"]


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sports",
        "-s",
        default=None,
        help=f"Comma-separated list of activity types. Can be: {SPORTS}",
    )
    parser.add_argument(
        "--init",
        "-i",
        default=None,
        help="Init date. July 1st",
    )
    parser.add_argument(
        "--end",
        "-e",
        default=None,
        help="End date. Default today",
    )
    return parser.parse_args()


def convert_args(args):
    if args.sports is None:
        sports = SPORTS
    else:
        sports = ",".join(args.sports)
        for sport in sports:
            print(sport, sport in sports)
            if sport not in SPORTS:
                raise TypeError(f"Unsupported sport: {sport}")

    if args.init is None:
        start = datetime.date(2024, 1, 1)
    else:
        start = datetime.datetime.strptime(args.init, "%Y-%m-%d").date()
    if args.end is None:
        end = datetime.date.today()
    else:
        end = datetime.datetime.strptime(args.end, "%Y-%m-%d").date()

    logging.info(f"Download for {sports} from {start} to {end}")
    return sports, start, end


def get_mfa():
    """Get MFA."""

    return input("MFA one-time code: ")


def connect():
    logging.info("Logging into Garmin API...")
    tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
    tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"

    try:
        print(
            f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            email = os.getenv("GARMIN_EMAIL") or None
            password = os.getenv("GARMIN_PASSWORD") or None
            if email is None:
                print("Please provide GARMIN_EMAIL")
                return None
            if password is None:
                print("Please provide GARMIN_PASSWORD")
                return None
            print(f"Login for {email}")
            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()
            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            print(
                f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)\n"
            )
            # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            print(
                f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
            )
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            logging.error(err)
            return None
    return garmin


def get_vo2_max(api, current_date, sports, vo2_max):

    current_iso = current_date.isoformat()
    print(current_iso)
    training_status = api.get_training_status(current_iso)

    if training_status is None:
        logging.warning(f"No training status for {current_date}")
        return
    if "mostRecentVO2Max" not in training_status:
        logging.warning(f"No 'mostRecentVO2Max' for {current_date} in training status")
        return
    most_recent_vo2_max = training_status["mostRecentVO2Max"]

    for sport in sports:
        if sport == "running":
            key = "generic"
            sport_id = 1
        else:
            key = sport
            sport_id = 2
        if key not in most_recent_vo2_max:
            print(f"No '{key}' for {current_date} in mostRecentVO2Max:")
            continue

        try:
            vo2_max_obj = most_recent_vo2_max[key]
            vo2_max_date = datetime.datetime.strptime(
                vo2_max_obj["calendarDate"], "%Y-%m-%d"
            ).date()
            vo2_max_value = vo2_max_obj["vo2MaxPreciseValue"]
            if vo2_max_date == current_date:
                print(f"Updated VO2Max {vo2_max_value} at {vo2_max_date}")
                if sport not in vo2_max:
                    vo2_max[sport] = []
                vo2_max[sport].append({"date": vo2_max_date, "value": vo2_max_value})
                print(vo2_max)
                with open("insert_vo2max.sql", "a") as fh:
                    fh.write(
                        f"INSERT VO2Max (date, value, sport_id) VALUES ('{vo2_max_date}', {vo2_max_value}, {sport_id});\n"
                    )
        except Exception as e:
            logging.warning(f"Couldn't extract VO2Max and date for {sport}. {e}")


def download(args, verbose=False):

    sports, current, end = convert_args(args)
    api = connect()

    if api is None:
        return

    # Main loop
    vo2_max = {}
    if os.path.isfile("insert_vo2max.sql"):
        os.remove("insert_vo2max.sql")
    while current < end:
        if verbose:
            print(f"Process date: {current}")

        get_vo2_max(api, current, sports, vo2_max)
        current += datetime.timedelta(days=1)

    print(vo2_max)
    write_vo2max(vo2_max)


def main():
    args = get_arguments()
    download(args)


if __name__ == "__main__":
    logging.info("Garmin API")
    main()
