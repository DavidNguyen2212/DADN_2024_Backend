from library import app, socket_io
from library import connectIOserver

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, allow_unsafe_werkzeug=True)