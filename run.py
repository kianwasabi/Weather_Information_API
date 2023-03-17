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
