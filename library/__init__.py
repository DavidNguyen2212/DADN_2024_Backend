from flask import Flask, request, Blueprint
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import json

app = Flask(__name__)
app.config.from_pyfile("../config/config.py")
CORS(app, origins="https://dadn-2024-team-blue-whale.vercel.app", supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socket_io = SocketIO(app, cors_allowed_origins="https://dadn-2024-team-blue-whale.vercel.app")
mongo_client = PyMongo(app)
db = mongo_client.db

@socket_io.on('connect')
def test_connect():
    print("Socket-IO smarthome connected!")

from library.controllers import notificationsController
from library.controllers import authController
from library.controllers import refreshTokenController
from library.controllers import logoutController
from library.controllers import aiController