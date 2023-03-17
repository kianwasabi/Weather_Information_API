from routes import *
from config import *

def main(): 
    app.run(hostIP, port, debug=True)
    try: 
        app.run(hostIP, port, debug=True)
        print("🫡 Server started")
    except Exception as e:
        print (f"Starting Server failed - Error: {e}")

if __name__ == '__main__':
    main()
#http://127.0.0.1:8080/weatherinformation?location=Braunschweig&openweathermaps_api_key=4b8f1ddd0540ebd49a6b0ca7927e3534