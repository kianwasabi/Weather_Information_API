import  math
import  requests
from    datetime import datetime

class Time(): 
    def __init__(self, timestamp , timezone):
        self.UNIXtimezone = timezone #unix, sec
        self.UNIXtimestamp, self.UTCdatetime = self._editTimewithTimezone(timestamp) # unix time edited with timezone returned as UTC TS & UNIX
        self.year, self.month, self.day, self.hour, self.minute, self.second = self._cropUTCdatetime() #simple time&date notation
    def _editTimewithTimezone(self, timestamp):
        ts_unedited = timestamp                     # unix timestamp in sec
        tz = self.UNIXtimezone                      # unix timezone in sec
        ts_edited = ts_unedited + tz                # edited unix timestamp in sec 
        dt = datetime.utcfromtimestamp(ts_edited)   # Construct a naive UTC datetime from a POSIX timestamp.
        return ts_edited, dt
    def _cropUTCdatetime(self):
        year = self.UTCdatetime.year
        month = self.UTCdatetime.month
        day = self.UTCdatetime.day
        hour = self.UTCdatetime.hour
        minute = self.UTCdatetime.minute
        second = self.UTCdatetime.second
        return year, month, day, hour, minute, second
    def getDate(self):
        d = "{:02d}".format(self.day)
        m = "{:02d}".format(self.month)
        y = "{:04d}".format(self.year)
        return f"{y}-{m}-{d}"
    def getTime(self):
        h = "{:02d}".format(self.hour)
        m = "{:02d}".format(self.minute)
        s = "{:02d}".format(self.second)
        return f"{h}:{m}:{s}"

class Location(Time): 
    def __init__(self,name,longitude, latitude, country, timestamp, timezone):
        Time.__init__(self, timestamp, timezone) 
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.country =  country

class Wind(Location):
    def __init__(self, wind_speed, wind_direction, name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self,name,longitude, latitude, country, timestamp, timezone)
        self.speed = wind_speed
        self.direction = wind_direction    
    def getDirectionPoint(self):
        if(self.direction>337.5):
            return 'North'
        if(self.direction>292.5):
            return 'North-West'
        if(self.direction>247.5):
            return 'West'
        if(self.direction>202.5):
            return 'South-West'
        if(self.direction>157.5):
            return 'South'
        if(self.direction>122.5):
            return 'South-East'
        if(self.direction>67.5):
            return 'East'
        if(self.direction>22.5):
            return 'Norht-East'
        return 'North'           

class Weather(Location): 
    def __init__(self,temperatur,min_temperatur,max_temperatur,feel_temperatur, weather_descr, cloudiness, visibility, name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, country, timestamp, timezone)
        self.current_temperatur = temperatur
        self.min_temperatur = min_temperatur
        self.max_temperatur = max_temperatur
        self.feel_temperatur = feel_temperatur
        self.weather_descr = weather_descr
        self.cloudiness = cloudiness
        self.visibility = visibility  

class Sun(Location):
    def __init__(self, timestamp_sunrise, timestamp_sunset, name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, country ,timestamp, timezone)
        self.sunrise = Time(timestamp_sunrise, timezone)
        self.sunset = Time(timestamp_sunset, timezone)
        self.azimuth, self.elevation  = self._SunPosition()
    def getAzimuth(self):
        return self.azimuth
    def getElevation(self):
        return self.elevation
    def getSunPosition(self):
        return self.azimuth, self.elevation
    def _SunPosition(self):
        ''' 
        Calculate Azimuth and Elevation
        Source (modified): https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
        '''
        refraction = True
        year = self.year
        month = self.month
        day = self.day
        hour = self.hour
        minute = self.minute
        second = self.second
        timezone = self.UNIXtimezone/60/60
        longitude = self.longitude
        latitude = self.latitude 
        #inner function 
        def into_range(x, range_min, range_max):
            shiftedx = x - range_min
            delta = range_max - range_min
            return (((shiftedx % delta) + delta) % delta) + range_min
        rad, deg = math.radians, math.degrees
        sin, cos, tan = math.sin, math.cos, math.tan
        asin, atan2 = math.asin, math.atan2  
        rlat = rad(latitude)
        rlon = rad(longitude) 
        greenwichtime = hour - timezone + minute / 60 + second /3600
        daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day - 730531.5 + greenwichtime / 24)  
        mean_long = daynum * 0.01720279239 + 4.894967873  
        mean_anom = daynum * 0.01720197034 + 6.240040768  
        eclip_long = (
            mean_long
            + 0.03342305518 * sin(mean_anom)
            + 0.0003490658504 * sin(2 * mean_anom))
        obliquity = 0.4090877234 - 0.000000006981317008 * daynum  
        rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))  
        decl = asin(sin(obliquity) * sin(eclip_long))
        sidereal = 4.894961213 + 6.300388099 * daynum + rlon  
        hour_ang = sidereal - rasc  
        elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat)* cos(hour_ang))  
        azimuth = atan2(-cos(decl) * cos(rlat) * sin(hour_ang),sin(decl) - sin(rlat) * sin(elevation),)
        azimuth = into_range(deg(azimuth), 0, 360)
        elevation = into_range(deg(elevation), -180, 180)
        if refraction:
            targ = rad((elevation + (10.3 / (elevation + 5.11))))
            elevation += (1.02 / tan(targ)) / 60
        return round(azimuth, 2), round(elevation, 2)

    def getAzimuthPoint(self):
        if(self.azimuth>337.5):
            return 'North'
        if(self.azimuth>292.5):
            return 'North-West'
        if(self.azimuth>247.5):
            return 'West'
        if(self.azimuth>202.5):
            return 'South-West'
        if(self.azimuth>157.5):
            return 'South'
        if(self.azimuth>122.5):
            return 'South-East'
        if(self.azimuth>67.5):
            return 'East'
        if(self.azimuth>22.5):
            return 'Norht-East'
        return 'North'

class WeatherInformation(Sun,Weather,Wind):
    '''
    Construct Weather Information Object.
    '''
    def __init__(self, timestamp_sunrise, timestamp_sunset, current_temperatur, min_temperatur,max_temperatur,feel_temperatur, weather_descr, cloudiness, visibility, wind_speed, wind_direction, name, country, longitude, latitude, timestamp, timezone):
        Sun.__init__(self,timestamp_sunrise, timestamp_sunset, name, country, longitude, latitude, timestamp, timezone)
        Weather.__init__(self,current_temperatur, min_temperatur,max_temperatur,feel_temperatur, weather_descr, cloudiness, visibility, name, country, longitude, latitude, timestamp, timezone)
        Wind.__init__(self,wind_speed, wind_direction, name, country, longitude, latitude, timestamp, timezone)

class CallOpenWeatherMapAPI():
    '''
    error_code: 
    (None) if no error occured,
    (str) "API-Error: URL not accepted." if connection was successful but the URL was not accepted, 
    (str) "API-Error: Connection failed." if connection to failed. 
    api_data:
    (tuple) if no api error occured
    (None) if Connection failed & URL was not accepted. 
    '''
    def __init__(self,city_name:str,user_api:str):
        self.city_name                  = city_name
        self.user_api                   = user_api
        self.units                      = "metric" # api is called with metric system by default
        self.api_data, self.error_code  = self._callAPI()
    def _callAPI(self):
        try:
            # Try to connect to open weathermap api & get api response
            # Note: ?->beginn query param, &->append query param, %->wildcard/space
            api_url = "https://api.openweathermap.org/data/2.5/weather"
            query_param_1 = "q="+self.city_name
            query_param_2 = "appid="+self.user_api
            query_param_3 = "units="+self.units
            complete_api_link = api_url + "?" + query_param_1 + "&" + query_param_2 + "&" + query_param_3
            response = requests.get(complete_api_link)
            api_data = response.json()
            response.raise_for_status()
            # Set error code if no error occurred
            error_code = None
            return api_data, error_code
        except requests.exceptions.HTTPError as err: 
            # Connection to weathermap api successed 
            # BUT query parameters appended to the url were not accepted.
            # Set error code if query parametere were not accepted
            error_code = str(str(api_data['cod'])+": "+api_data['message'])
            # Set api_data to Null
            api_data = None
            return api_data, error_code
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.ConnectTimeout) as err:
            # Connection to weathermap api failed or timed out. 
            # Set api_data to Null
            api_data = None
            # Set error code if Connection to OpenWeatherMaps API failed/timed out. 
            error_code = "URL may be correct but connection to weathermap api failed/timed out."
            return api_data, error_code
        