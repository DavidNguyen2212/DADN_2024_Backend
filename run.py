from library import app

this_app = app
if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=False) 
#     socket_io.run(app, port=os.environ.get("PORT"), log_output=True, debug=False)