import argparse
import datetime
import logging
import os

from garminconnect import Garmin

from database.write import write_vo2max

SPORTS = ["cycling", "running"]


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cred",
        "-c",
        default=False,
        help="Use credentials over env variable",
    )
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
            if sport not in sports:
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


def connect(use_cred=False):
    logging.info("Logging into Garmin API...")

    try:
        if use_cred:
            print("Use credentials")
            email = os.getenv("GARMIN_EMAIL")
            password = os.getenv("GARMIN_PASSWORD")
            print(email)
            api = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
        else:
            print("Use tokenstore")
            tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
            print(tokenstore)
            api = Garmin()
            api.login(tokenstore)

        logging.info("Logged into Garmin API.")
        print("Logged in")
        return api
    except Exception as e:
        logging.error(f"Couldn't log in to Garmin API: {e}")
        return None


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
        else:
            key = sport
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
        except Exception as e:
            logging.warning(f"Couldn't extract VO2Max and date for {sport}. {e}")


def download(args, verbose=False):

    sports, current, end = convert_args(args)
    api = connect(args.cred)

    if api is None:
        return

    # Main loop
    vo2_max = {}
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
