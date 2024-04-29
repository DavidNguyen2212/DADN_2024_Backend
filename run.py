from library import app, socket_io

if __name__ == "__main__":
    # app.run(debug=True, use_debugger=True, use_reloader=False) 
    socket_io.run(app, host="0.0.0.0", port=5007, allow_unsafe_werkzeug=True)