from .class_def import CallOpenWeatherMapAPI, WeatherInformation

def WeatherInfo(city_name:str, user_api:str):
    '''
    Generates weatherinformation for "XYZ"
    :param cityname: (str) City Name
    :param user_api: (str) API Key for openweathermaps.com
    :return: (str) API Error Code
             (None) if no error occured Error Code is
    :return: (turpel) objects of class WeatherInformation,
             (None) if construct of class WeatherInformation failed.
    '''
    # First, construct an object "api_call" of class "CallOpenWeatherMapAPI" that holds 
    # all the API content before preprocessing from OpenWeatherMaps in "api_data" 
    # and the API error code in "api_error". 
    api_call = CallOpenWeatherMapAPI(city_name,user_api)
    api_data = api_call.api_data
    api_error = api_call.error_code
    # Second, define an local variable "weaterinfo" that points toward null. 
    weatherinfo =  None
    # Third, if no api error occurred and the OpenWeatherMap API responded with 
    # some usable data than extract, organize, and start pre-processing the recieved content as you wish. 
    if(api_error is None and api_data is not None):
        # location & sun 
        latitude            = api_data['coord']['lat']    #lat
        longitude           = api_data['coord']['lon']    #long 
        country_code        = api_data['sys']['country']  #Country codes, see OpenWeatherMaps Doc
        timezone            = api_data['timezone']        #timezone in seconds (unix, UTC)
        unix_location       = api_data['dt']              #timestamp in seconds (unix, UTC)
        unix_sunrise        = api_data['sys']['sunrise']  #timestamp in seconds (unix, UTC)
        unix_sunset         = api_data['sys']['sunset']   #timestamp in seconds (unix, UTC)
        #weather
        temperatur          = api_data['main']['temp'] #api call metric, if imperial use: round(((api_data['main']['temp'])-273.15),3
        temperatur_min      = api_data['main']['temp_min']
        temperatur_max      = api_data['main']['temp_max']
        temperatur_feel     = api_data['main']['feels_like']
        weather_description = api_data['weather'][0]['description']
        humidity            = api_data['main']['humidity']
        #wind
        cloudiness          = api_data['clouds']['all']
        visibility          = api_data['visibility']
        wind_speed          = api_data['wind']['speed']
        wind_direction      = api_data['wind']['deg']
        # Fourth, construct an object of class "WeatherInformation" that 
        # holds all the finalized weatherinformations. 
        weatherinfo = WeatherInformation(
            current_temperatur=temperatur,
            min_temperatur=temperatur_min,
            max_temperatur=temperatur_max,
            feel_temperatur=temperatur_feel,
            weather_descr=weather_description,
            cloudiness=cloudiness,
            visibility=visibility,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            name=city_name,
            country=country_code,
            longitude=longitude,
            latitude=latitude,
            timestamp_sunrise=unix_sunrise,
            timestamp_sunset=unix_sunset,
            timestamp=unix_location,
            timezone=timezone)
    # Finally, return the original OpenWeatherMap API data (if needed), 
    # the WeatherInformation object (that holds all needed information),
    # and the OpenWeatherMaps API error code. 
    return api_data, weatherinfo, api_error