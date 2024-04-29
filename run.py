from library import app, socket_io
from library import connectIOserver
import os

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, host="0.0.0.0", port=os.environ.get("PORT"), allow_unsafe_werkzeug=True)