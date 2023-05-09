from .class_def import CallOpenWeatherMapAPI, WeatherInformation

def WeatherInfo(city_name:str, user_api:str):
    '''
    Provides weather information for a location by 
    fetching content from the OpenWeatherMap API, 
    organizing the received data and 
    adding some internal computed information to it. 
    The original OpenWeatherMap API content, 
    the edited content helt in an object of class WeatherInformation
    as well as the status of the OpenWeatherMap API is returned.

    :param cityname: 
    - (str) Name of Location

    :param user_api: 
    - (str) API Key for openweathermaps.com 
    - see: https://openweathermap.org/appid for more information
    
    :return api_status: 
    - (int) API Status Code (200 = OK, ...)

    :return api_msg: 
    - (str) API Status Message 

    :return weatherinfo: 
    - (turpel) Objects of class WeatherInformation,
    - (None) If construct of class WeatherInformation failed.

    :return api_data: 
    - (tuple) Original content of OpenWeatherMaps API.
    - (None)  If connection to OpenWeatherMaps API and hence no information could be fatched.
    '''
    # First, construct an object "api_call" of class "CallOpenWeatherMapAPI" that holds 
    # all the OpenWeatherMaps API data before preprocessing in "api_data" 
    # and the API status & message. 
    api_call    = CallOpenWeatherMapAPI(city_name,user_api)
    api_data    = api_call.api_data
    api_msg     = api_call.api_msg
    api_status  = api_call.api_code
    # Second, define an local variable "weaterinfo" that points toward null. 
    weatherinfo =  None
    # Third, if no api error occurred (200 OK) and the OpenWeatherMap API responded with 
    # some usable data than extract and organize the recieved data. 
    if((api_status == 200) and api_data is not None):
        #Some data fields' availability, <gust> for instance, depends on whether 
        #it is provided by the requested location's weather station.
        #The following will return None if either key1 or key2 does not exist.
        latitude            = api_data.get('coord', {}).get('lat')                          #latitude
        longitude           = api_data.get('coord', {}).get('lon')                          #longitude
        country_code        = api_data.get('sys', {}).get('country')                        #country code
        timezone            = api_data.get('timezone')                                      #timezone offset in sec (unix, UTC)
        unix_location       = api_data.get('dt')                                            #timestamp (unix, UTC, epoch)
        unix_sunrise        = api_data.get('sys', {}).get('sunrise')                        #timestamp (unix, UTC, epoch)
        unix_sunset         = api_data.get('sys', {}).get('sunset')                         #timestamp (unix, UTC, epoch)
        visibility          = api_data.get('visibility')
        weather_description = api_data.get('weather',{})[0].get('description',{})
        temperatur          = api_data.get('main', {}).get('temp')                          #current temp in C (API call is metric)
        #temperatur          = round(((api_data.get('main', {}).get('temp'))-273.15),3      #current temp in F (API call is imperial)
        temperatur_min      = api_data.get('main', {}).get('temp_min')                      #min temp in C
        temperatur_max      = api_data.get('main', {}).get('temp_max')                      #min temp in C
        temperatur_feel     = api_data.get('main', {}).get('feels_like')                    #feels like temp in C
        humidity            = api_data.get('main', {}).get('humidity')                      #humidity in 
        pressure            = api_data.get('main', {}).get('pressure')                      #pressure in psi
        cloudiness          = api_data.get('clouds', {}).get('all')                         #cloudiness in %
        speed               = api_data.get('wind', {}).get('speed')                         #wind speed in km/h 
        direction           = api_data.get('wind', {}).get('deg')                           #wind direction in deg 
        gust                = api_data.get('wind', {}).get('gust')                          #wind gust in km/h
        quality_index       = api_data.get('list',{})[0].get('main',{}).get('aqi')
        CO_concentration    = api_data.get('list',{})[0].get('components',{}).get('co')
        NO_concentration    = api_data.get('list',{})[0].get('components',{}).get('no')
        NO2_concentration   = api_data.get('list',{})[0].get('components',{}).get('no2')
        O3_concentration    = api_data.get('list',{})[0].get('components',{}).get('o3')
        SO2_concentration   = api_data.get('list',{})[0].get('components',{}).get('so2')
        PM2_5_concentration = api_data.get('list',{})[0].get('components',{}).get('pm2_5')
        PM10_concentration  = api_data.get('list',{})[0].get('components',{}).get('pm10')
        NH3_concentration   = api_data.get('list',{})[0].get('components',{}).get('nh3')
        print(NH3_concentration)
        # Fourth, construct an object of class "WeatherInformation" with the extracted data. 
        # This object holds all the finalized weatherinformations. 
        weatherinfo = WeatherInformation(
            current_temperatur  = temperatur,
            min_temperatur      = temperatur_min,
            max_temperatur      = temperatur_max,
            feel_temperatur     = temperatur_feel,
            weather_descr       = weather_description,
            cloudiness          = cloudiness,
            visibility          = visibility,
            humidity            = humidity,
            pressure            = pressure,
            wind_speed          = speed,
            wind_direction      = direction,
            wind_gust           = gust,
            quality_index       = quality_index,
            CO_concentration    = CO_concentration,
            NO_concentration    = NO_concentration,
            NO2_concentration   = NO2_concentration, 
            O3_concentration    = O3_concentration,
            SO2_concentration   = SO2_concentration,
            PM2_5_concentration = PM2_5_concentration,
            PM10_concentration  = PM10_concentration,
            NH3_concentration   = NH3_concentration,
            name                = city_name,
            country             = country_code,
            longitude           = longitude,
            latitude            = latitude,
            timestamp_sunrise   = unix_sunrise,
            timestamp_sunset    = unix_sunset,
            timestamp           = unix_location,
            timezone            = timezone
            )
    del api_call   
    # Finally, return the original OpenWeatherMap API data in "api_data", 
    # the WeatherInformation object (that holds all needed information),
    # and the API status and message. 
    return api_data, weatherinfo, api_status, api_msg