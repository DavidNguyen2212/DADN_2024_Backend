import eventlet.wsgi
from library import app, socket_io
from library import connectIOserver
import os
import eventlet

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    eventlet.wsgi.server(eventlet.listen(('', os.environ.get("PORT"))), app)
    # socket_io.run(app, host="0.0.0.0", port=os.environ.get("PORT"), allow_unsafe_werkzeug=True)