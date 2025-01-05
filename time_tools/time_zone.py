
import datetime
import pytz


# Function to return current time for a given city
def get_city_time(city):
    # Get timezone from dictionary
    tz = pytz.timezone(city)
    # Localize current datetime to city timezone
    now = datetime.datetime.now(tz)
    # Return the current time
    return now
    # return now.strftime("%H:%M:%S - %H:%M")


