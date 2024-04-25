from library import app
from library import socket_io
from library import connectIOserver     # connected! 
import sys,requests

this_app = app
if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, allow_unsafe_werkzeug=True)
    # this_app = app
    # app.run(debug=False)