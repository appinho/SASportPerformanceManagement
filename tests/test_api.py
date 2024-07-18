from data_feed.garmin_api import connect


def test_import():
    try:
        from garminconnect import Garmin

        _ = Garmin()
        print("GarminConnect imported successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


test_import()


def test_api_connection():

    try:
        api = connect()
    except Exception as err:
        print(f"Error connecting to Garmin API: {err}")
        assert False
    assert api is not None


test_api_connection()