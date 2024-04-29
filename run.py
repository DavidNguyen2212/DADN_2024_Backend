from library import app, socket_io

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, allow_unsafe_werkzeug=True)