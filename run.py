from routes import *
from config import *

def main(): 
    app.run(hostIP, port, debug=True)
    try: 
        app.run(hostIP, port, debug=True)
        print("🫡 Server started")
    except Exception as err:
        print (f"Starting Server failed - Error: {err}")

if __name__ == '__main__':
    main()
