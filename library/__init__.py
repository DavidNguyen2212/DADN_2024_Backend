import eventlet
eventlet.monkey_patch()
from flask import Flask, request, Blueprint
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cookies import Cookies
from flask_mqtt import Mqtt
import json

mqtt_connected = False 
app = Flask(__name__)
app.config.from_pyfile("../config/config.py")
CORS(app, origins="*", supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socket_io = SocketIO(app, cors_allowed_origins="*")
mqtt = Mqtt(app)

@socket_io.on('connect')
def test_connect():
    print("Socket IO from smart_home_BackEnd connected")

mongo_client = PyMongo(app)
db = mongo_client.db

AIO_FEED_ID = ['temp', 'humi', 'light', 'chandeliers', 'control-fan','ac']

from library.connectIOserver import create_Client
client = create_Client()
client.loop_background()
# from library import connectIOserver
from library.controllers import notificationsController
from library.controllers import authController
from library.controllers import refreshTokenController
from library.controllers import logoutController
from library.controllers import aiController