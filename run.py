from library import app
from library import socket_io

this_app = app
if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, host="0.0.0.0", port=3107, allow_unsafe_werkzeug=True)