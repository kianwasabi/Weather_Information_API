from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

ts = 1679568890 # timestamp sunrise in sec unix utc
tz = -4*60*60 # timezone in sec unix utc
e = ts + tz # 
time = datetime.utcfromtimestamp(e)

timezone_at = TimezoneFinder().timezone_at(lng=-74.006,lat=40.7143)
tz = pytz.timezone(timezone_at)
dt = datetime.now(tz)
unix_timestamp = int(dt.timestamp()) # Convert the datetime object to a Unix timestamp

#SOLL: Timestamp: SEC & timetone: SEC


# utc_dt = datetime.utcfromtimestamp(ts)
# # If you want to get an aware datetime object for UTC timezone:


# aware_utc_dt = utc_dt.replace(tzinfo=pytz.utc)
# # To convert it to some other timezone:
# tz = pytz.timezone('America/Montreal')
# dt = aware_utc_dt.astimezone(tz)
# # To convert the timestamp to an aware datetime object in the given timezone directly:
# dt = datetime.fromtimestamp(ts, tz)


