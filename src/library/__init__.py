from flask import Flask, request, Blueprint
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS

mqtt_connected = False 
app = Flask(__name__)
app.config.from_pyfile("../config/config.py")
CORS(app)
socket_io = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@socket_io.on('message')
def handle_message(message):
    print('OK!, client rep: ' + message )
mongo_client = PyMongo(app)
db = mongo_client.db


# app.register_blueprint(lvrc.lvroom)
# from library import livingroomController
from library.controllers import notificationsController
from library.controllers import socketIOController
from library.controllers import livingroomController
