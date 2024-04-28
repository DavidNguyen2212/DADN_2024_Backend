from library import app
from library import client
# from library import socket_io
# from library import connectIOserver     # connected! 
import sys,requests
import os
 

client.connect()
client.loop_background() 
this_app = app
# if __name__ == "__main__":
#     # app.run(debug=True, use_debugger=True, use_reloader=False) 
#     socket_io.run(app, port=os.environ.get("PORT"), log_output=True, debug=False)