from library import app, socket_io
from library import connectIOserver

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, host="0.0.0.0", port=3017,log_output=True, allow_unsafe_werkzeug=True)