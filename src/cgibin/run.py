# !! For LOCAL WSGI server usage !!
# NOTES: Do not use app.run() & print() in production.
# Moreover app.run() is fine to use in production as long as it is contained 
# in an if __name__ == '__main__': block. This is because most 
# production http servers do not execute this block. 
# Therefore, run.py & config.py are only meant for development on a local machine.  
# !! The flask application is executed in production with the routes.py file. 
from routes import *
import socket

def main(): 
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)
    port = 8080
    try: 
        app.run(hostIP, port, debug=True)
    except Exception as err:
        print (f"Starting Server failed - Error: {err}")

if __name__ == '__main__':
    main()
