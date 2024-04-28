from library import app
from library import client
# from library import socket_io
# from library import connectIOserver     # connected! 
import sys,requests
import os


# client.connect()
# print("Here")
# client.loop_background()  

client.connect()
print("Here on conect")
complete_client = client
client.loop_background()  # Start the background loop for handling incoming messages
this_app = app
# if __name__ == "__main__":
#     # app.run(debug=True, use_debugger=True, use_reloader=False) 
#     socket_io.run(app, port=os.environ.get("PORT"), log_output=True, debug=False)