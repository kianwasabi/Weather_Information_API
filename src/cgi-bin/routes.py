import dependencies
from flask import Flask,  make_response , request, jsonify
from flask_cors import CORS
from packages.weather_Information import WeatherInfo
from collections import defaultdict

# create flask application 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# define routes
@app.route('/current', methods=['GET'])
def weatherinformation():

    # Get query parameters/keys from url.
    location = request.args.get("location", None)
    openweathermaps_api_key = request.args.get("openweathermaps_api_key", None)

    # Use the weather_information package to get data in the weatherdata object 
    # and the api status.
    # The raw OpenWeatherMap API data does not find usage in this route, call route '/current/openweathermaps' instead.)
    _ , weatherdata, api_error_code, api_error_msg = WeatherInfo(city_name=location, user_api=openweathermaps_api_key)

    # Generate http response 
    #First, define defaultdict which itself contains a defaultdict of lists.
    #Needed if step 2 is skipped to store the API status in step 3.                                           
    payload = defaultdict(lambda: defaultdict(list))

    #Second, check if the API call was successful and the weatherdata object holds data.
    #If true, fill payload dict with data. 
    if(weatherdata is not None):
        payload = {
            'location': {
                'name'      : weatherdata.name,
                'country'   : weatherdata.country,
                'longitude' : weatherdata.longitude,
                'latitude'  : weatherdata.latitude,
                'time': {
                    'stamp_unix': weatherdata.UNIXtimestamp, 
                    'zone_unix': weatherdata.UNIXtimezone,
                    'stamp_utc': weatherdata.UTCdatetime,
                    'simple' : weatherdata.getTime(),
                    'dt' : weatherdata.getDate()
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
                    'stamp_unix': weatherdata.sunrise.UNIXtimestamp,
                    'zone_unix': weatherdata.sunrise.UNIXtimezone,
                    'stamp_utc': weatherdata.sunrise.UTCdatetime,
                    'simple' : weatherdata.sunrise.getTime(),
                    'dt' : weatherdata.sunrise.getDate(),
                    }, 
                'set' : {
                    'stamp_unix': weatherdata.sunset.UNIXtimestamp,
                    'zone_unix': weatherdata.sunset.UNIXtimezone,
                    'stamp_utc': weatherdata.sunset.UTCdatetime,
                    'simple' : weatherdata.sunset.getTime(),
                    'dt' : weatherdata.sunset.getDate(),
                    }, 
                #'uvi':"tbd"    
                },
            'wind': {
                'speed'    : weatherdata.speed,
                'direction': {
                    'deg'   : weatherdata.direction,
                    'point' : weatherdata.getDirectionPoint()
                    },
                'gust': weatherdata.gust
                },
            'weather':  {
                'pressure' : weatherdata.pressure, 
                'humidity': weatherdata.humidity,
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
    
    # Third, add API status to payload dict. 
    error_key_dict_add = {
        'api':{
            'code': api_error_code,
            'msg': api_error_msg
            }
        }
    payload.update(error_key_dict_add)  

    # Finally, place payload dict in http response.  
    response = make_response(jsonify(payload))
    return response

@app.route('/current/openweathermaps', methods=['GET'])
def weatherinformation_oc():
    location = request.args.get("location", None)
    openweathermaps_api_key = request.args.get("openweathermaps_api_key", None)
    # plane display of the original content provided by the OpenWeatherMap API's response. 
    api_data, _ , _ , _ = WeatherInfo(city_name=location,user_api=openweathermaps_api_key) 
    response = make_response(jsonify(api_data))
    return response