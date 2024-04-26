from library import app
from library import socket_io
from library import connectIOserver     # connected! 
import sys,requests

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app)