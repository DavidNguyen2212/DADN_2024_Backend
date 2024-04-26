# import eventlet
# eventlet.monkey_patch()
from flask import Flask, request, Blueprint
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cookies import Cookies

mqtt_connected = False 
app = Flask(__name__)
app.config.from_pyfile("../config/config.py")
CORS(app, origins="*", supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cookies = Cookies(app=app)
socket_io = SocketIO(app, cors_allowed_origins="*")

@socket_io.on('message')
def handle_message(message):
    print('OK!, client rep: ' + message )
mongo_client = PyMongo(app)
db = mongo_client.db

from library.controllers import notificationsController
from library.controllers import authController
from library.controllers import refreshTokenController
from library.controllers import logoutController
from library.controllers import aiController
