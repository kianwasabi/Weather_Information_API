from flask import Flask,  make_response , request, jsonify
from flask_cors import CORS
from config import *
from packages.weather_Information import WeatherInfo

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/weatherinformation', methods=['GET'])
def weatherinformation():
    # if key doesn't exist, returns None // 400 error
    location = request.args.get("location", None)
    openweathermaps_api_key = request.args.get("openweathermaps_api_key", None)
    # call weather information package
    weatherdata = WeatherInfo(city_name=location,user_api=openweathermaps_api_key)
    print(weatherdata)
    if (weatherdata):
    # generate http response 
        payload = {
            'location': {'name'     : weatherdata.getLocationName(), 
                        'longitude': weatherdata.getLongitude(),
                        'latitude' : weatherdata.getLatitude(),
                        'time'     : weatherdata.getTime()}, 
            'sun':      {'azimuth'  : weatherdata.getAzimuth(),
                        'elevation': weatherdata.getElevation(),
                        'rise'     : weatherdata.getTimeSunrise(), 
                        'set'      : weatherdata.getTimeSunset(),},
            'wind':     {'speed'    : weatherdata.getWindSpeed(),
                        'direction': weatherdata.getDirectionPoint(),
                        },
            'weather':  {'discription': weatherdata.getTemperatur(),
                        'visibility' : weatherdata.getVisibility(),
                        'cloudiness': weatherdata.getCloudiness(),
                        'temperatur': weatherdata.getTemperatur(),}
        }
    else: 
        payload = weatherdata
    response = make_response(jsonify(payload))
    return response
