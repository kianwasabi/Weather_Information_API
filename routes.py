from flask import Flask,  make_response , request, jsonify
from flask_cors import CORS
from config import *
from packages.weather_Information import WeatherInfo
from collections import defaultdict

# create flask application 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# define routes

@app.route('/weatherinformation', methods=['GET'])
def weatherinformation():
    # Get query parameters/keys from url. If key doesn't exist, returns None (400 error).
    location = request.args.get("location", None)
    openweathermaps_api_key = request.args.get("openweathermaps_api_key", None)
    # Use weather information package to get the processed OpenWeatherMaps API content
    # in object "weatherdata", the raw API data in "api_data" (used in route /weatherinformation/oc) and the api error in "api_error".
    _ , weatherdata, api_error = WeatherInfo(city_name=location, user_api=openweathermaps_api_key)
    # Generate http response 
    # First, define defaultdict which itself contains a defaultdict of lists.                                                      
    payload = defaultdict(lambda: defaultdict(list))
    # Check if API call and processing was successful by checking if weatherdata points towards some data
    if(weatherdata is not None):
        #fill the response dict with data
        payload = {
            'location': {
                #Note: getattr(weatherdata,'UNIXtimestamp') instead of weatherdata.UNIXtimestamp
                'name'      : weatherdata.name,
                'country'   : weatherdata.country,
                'longitude' : weatherdata.longitude,
                'latitude'  : weatherdata.latitude,
                'time': {
                    'UNIX_Timestamp': weatherdata.UNIXtimestamp, 
                    'UNIX_Timezone': weatherdata.UNIXtimezone,
                    'UTC_Timestamp': weatherdata.UTCdatetime,
                    'simple_time' : weatherdata.getTime(),
                    'simple_date' : weatherdata.getDate()
                    },
                }, 
            'sun': {
                'azimuth': {
                    'deg'   : weatherdata.azimuth,
                    'point' : weatherdata.getAzimuthPoint()
                    },
                'elevation': {
                    'deg'   : weatherdata.elevation
                    },
                'rise' : {
                    'UNIX_Timestamp': weatherdata.sunrise.UNIXtimestamp,
                    # 'UNIX_Timezone': weatherdata.sunrise.UNIXtimezone,
                    # 'UTC_Timestamp': weatherdata.sunrise.UTCdatetime,
                    'simple_time' : weatherdata.sunrise.getTime(),
                    # 'simple_date' : weatherdata.sunrise.getDate(),
                    }, 
                'set' : {
                    'UNIX_Timestamp': weatherdata.sunset.UNIXtimestamp,
                    # 'UNIX_Timezone': weatherdata.sunset.UNIXtimezone,
                    # 'UTC_Timestamp': weatherdata.sunset.UTCdatetime,
                    'simple_time' : weatherdata.sunset.getTime(),
                    # 'simple_date' : weatherdata.sunset.getDate(),
                    }, 
                },
            'wind': {
                'speed'    : weatherdata.speed,
                'direction': {
                    'deg'   : weatherdata.direction,
                    'point' : weatherdata.getDirectionPoint()
                    },
                },
            'weather':  {
                'discription': weatherdata.weather_descr,
                'visibility' : weatherdata.visibility,
                'cloudiness': weatherdata.cloudiness,
                'temperatur': {
                    'current': weatherdata.current_temperatur,
                    'max': weatherdata.max_temperatur,
                    'min': weatherdata.min_temperatur,
                    'feel': weatherdata.feel_temperatur
                    }
                }        
    }
    # Add API error code to response dict
    error_key_dict_add = {'OpenWeatherMap API':{'code': api_error}}
    payload.update(error_key_dict_add)
    # place dict in http respone 
    response = make_response(jsonify(payload))
    return response

@app.route('/weatherinformation/oc', methods=['GET'])
def weatherinformation2():
    location = request.args.get("location", None)
    openweathermaps_api_key = request.args.get("openweathermaps_api_key", None)
    # plane display of the original content provided by the OpenWeather APIs response
    api_data, _ , _ = WeatherInfo(city_name=location,user_api=openweathermaps_api_key) 
    response = make_response(jsonify(api_data))
    return response