import  math
import  requests
from    datetime import datetime
from    pvlib    import location

def deg2point(value):
    if(value>337.5):
        return 'North'
    if(value>292.5):
        return 'North-West'
    if(value>247.5):
        return 'West'
    if(value>202.5):
        return 'South-West'
    if(value>157.5):
        return 'South'
    if(value>122.5):
        return 'South-East'
    if(value>67.5):
        return 'East'
    if(value>22.5):
        return 'Norht-East'
    return 'North'

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
        return f"{d}.{m}.{y}"
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
        self.altitute = location.lookup_altitude(latitude, longitude)

class Air(Location): 
    def __init__(self, humidity, pressure, quality_index, 
                 CO_concentration, NO_concentration, NO2_concentration, O3_concentration, SO2_concentration, 
                 PM2_5_concentration, PM10_concentration, NH3_concentration,
                 name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self,name,longitude, latitude, country, timestamp, timezone)
        self.humidity = humidity
        self.pressure = pressure
        self.quality_index = quality_index
        self.CO_concentration = CO_concentration
        self.NO_concentration = NO_concentration
        self.NO2_concentration = NO2_concentration
        self.O3_concentration = O3_concentration
        self.SO2_concentration = SO2_concentration
        self.PM2_5_concentration = PM2_5_concentration
        self.PM10_concentration = PM10_concentration
        self.NH3_concentration = NH3_concentration

class Wind(Location):
    def __init__(self, wind_speed, wind_direction, wind_gust, 
                 name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self,name,longitude, latitude, country, timestamp, timezone)
        self.speed = wind_speed
        self.direction = wind_direction  
        self.gust = wind_gust  
    def getDirectionPoint(self):
        return deg2point(self.direction)         

class Weather(Location): 
    def __init__(self,temperatur,min_temperatur,max_temperatur,feel_temperatur, weather_descr, cloudiness, visibility, 
                name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, country, timestamp, timezone)
        self.current_temperatur = temperatur
        self.min_temperatur = min_temperatur
        self.max_temperatur = max_temperatur
        self.feel_temperatur = feel_temperatur
        self.weather_descr = weather_descr
        self.cloudiness = cloudiness
        self.visibility = visibility  

class Sun(Location):
    def __init__(self, timestamp_sunrise, timestamp_sunset, 
                 name, country, longitude, latitude, timestamp, timezone):
        Location.__init__(self, name, longitude, latitude, country ,timestamp, timezone)
        self.sunrise = Time(timestamp_sunrise, timezone)
        self.sunset = Time(timestamp_sunset, timezone)
        self.azimuth, self.elevation  = self._SunPosition()
    def _SunPosition(self):
        ''' 
        Calculate Azimuth and Elevation
        Source (modified): 
        https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777
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
        return deg2point(self.azimuth)

class WeatherInformation(Sun,Weather,Wind,Air):
    '''
    Construct Weather Information Object
    that holds the child classes Sun, Weather & Wind. 
    '''
    def __init__(self, timestamp_sunrise, timestamp_sunset, 
                 current_temperatur, min_temperatur, max_temperatur, feel_temperatur, 
                 weather_descr, cloudiness, visibility,
                 wind_speed, wind_direction, wind_gust,
                 humidity, pressure, quality_index, 
                 CO_concentration, NO_concentration, NO2_concentration, O3_concentration, SO2_concentration, 
                 PM2_5_concentration, PM10_concentration, NH3_concentration,
                 name, country, longitude, latitude, timestamp, timezone):
        Sun.__init__(self,timestamp_sunrise, timestamp_sunset, 
                     name, country, longitude, latitude, timestamp, timezone)
        Weather.__init__(self,current_temperatur, min_temperatur,max_temperatur,feel_temperatur, weather_descr, cloudiness, visibility,
                        name, country, longitude, latitude, timestamp, timezone)
        Wind.__init__(self,wind_speed, wind_direction, wind_gust,
                      name, country, longitude, latitude, timestamp, timezone)
        Air.__init__(self, humidity, pressure, quality_index, 
                    CO_concentration, NO_concentration, NO2_concentration, O3_concentration, SO2_concentration, 
                    PM2_5_concentration, PM10_concentration, NH3_concentration,
                    name, country, longitude, latitude, timestamp, timezone)       

class CallOpenWeatherMapAPI():
    '''
    Fetches & returns content from OpenWeatherMap API as well as the API status. 
    :return error_code: 
    - (int) 200 if no error occured,
    - ...
    :return api_data:
    - (tuple) if no API error occured
    - (None) if an API error occured 
    '''
    def __init__(self,city_name:str,user_api:str):
        self.city_name                  = city_name
        self.user_api                   = user_api
        self.units                      = "metric"                          # api is called with metric system by default
        self.api_data, self.api_code, self.api_msg  = self._callOpenWeahterMapsAPI()   # !PRODUCTION!
        #self.api_data, self.error_code  = self._callofflineAPI()           # !TESTING w/ API Emulator! 

    def _callofflineAPI(self):
        # For testing with OpenWeatherMaps Server Emulator, running locally. 
        # Use repository "API EMULATOR"!
        api_url = "http://127.0.0.1:8080/api/weatherinfomation/openweathermaps/emulator"
        response = requests.get(api_url)
        api_data = response.json()
        print(api_data)
        api_code = None
        api_msg = None
        return api_data, api_code, api_msg 
    
    def _callOpenWeahterMapsAPI(self):
        try: 
            # Try to connect to several OpenWeatherMaps API endpoints
            # First, the geocoding API endpoint to get lat. & long. for a location name
            api_url = "http://api.openweathermap.org/geo/1.0/direct"
            query_param_1 = "q="+self.city_name
            query_param_2 = "limit="+"1"
            query_param_3 = "appid="+self.user_api
            complete_api_link = api_url + "?" + query_param_1 + "&" + query_param_2 + "&" + query_param_3
            response = requests.get(complete_api_link)
            api_data = response.json()
            response.raise_for_status()
            lat = api_data[0]['lat']
            lon = api_data[0]['lon']
            # Second, the current weather endpoint to get current weatherinformation
            api_url = "https://api.openweathermap.org/data/2.5/weather"
            query_param_1 = "lat="+str(lat)
            query_param_2 = "lon="+str(lon)
            query_param_3 = "appid="+self.user_api
            query_param_4 = "units="+self.units
            complete_api_link = api_url + "?" + query_param_1 + "&" + query_param_2 + "&" + query_param_3 + "&" + query_param_4
            response = requests.get(complete_api_link)
            api_data = response.json()
            response.raise_for_status()
            # Third, the current air pollution endpoint
            api_url = "http://api.openweathermap.org/data/2.5/air_pollution"
            query_param_1 = "lat="+str(lat)
            query_param_2 = "lon="+str(lon)
            query_param_3 = "appid="+self.user_api
            complete_api_link = api_url + "?" + query_param_1 + "&" + query_param_2 + "&" + query_param_3
            response = requests.get(complete_api_link)
            api_data.update(response.json())
            response.raise_for_status()
            # Finally, set error code & msg if no error occurred
            api_code = 200
            api_msg = None
            return api_data, api_code, api_msg
        except requests.exceptions.HTTPError as err: 
            # Connection to weathermap endpoint succeeded but q-param were not accepted.
            api_code = int(api_data['cod'])
            api_msg = str("OpenWeatherMaps API Error:" + api_data['message'])
            # Set api_data to Null
            api_data = None
            return api_data, api_code, api_msg
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.ConnectTimeout) as err:
            # Connection to weathermap api failed or timed out. 
            # Set api_data to Null
            api_data = None
            # Set error code if Connection to OpenWeatherMaps API failed/timed out. 
            api_code = 408
            api_msg = "Connection to OpenWeatherMap API failed/timed out."
            return api_data, api_code, api_msg
        