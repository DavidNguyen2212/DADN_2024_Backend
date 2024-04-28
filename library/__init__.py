import eventlet
eventlet.monkey_patch()
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
socket_io = SocketIO(app, cors_allowed_origins="*")

@socket_io.on('connect')
def test_connect():
    print("socket connected")

mongo_client = PyMongo(app)
db = mongo_client.db

# from library import connectIOserver
# from Adafruit_IO import Client
from library.initIOserver import MQTTClient
import sys, os
import json
# from library import db
# from library import socket_io
# from flask_socketio import emit, send
from library.models.notificationModel import Notification
from library.models.roomModel import Room
from library.models.deviceModel import Device
import datetime, pytz
# import paho.mqtt.client as mqtt


tz = pytz.timezone('Asia/Ho_Chi_Minh')
AIO_FEED_ID = ['temp', 'humi', 'light', 'chandeliers', 'control-fan','ac', 'door']
AIO_USERNAME = os.environ.get("AIO_USERNAME")
AIO_KEY = os.environ.get("AIO_KEY")

def connected(client):
    print("Kết nối thành công...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def subscribe(client, userdata, mid, granted_qos):
    print("Subcribe thành công...")

def disconnected(client):
    print("Ngắt kết nối...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Nhận dữ liệu từ " + feed_id + ": " + payload)

    if feed_id == "temp":
        last_record = Room.collection.find_one({"id": 1}, sort=[('_id', -1)])
        new_record = Room(1, "livingroom", payload, last_record["humidity"], last_record["lux"], 
                               datetime.datetime.now(tz).isoformat()).to_dictFormat()
        Room.insert_room_record(new_record)
    elif feed_id == "humi": 
        last_record = Room.collection.find_one({"id": 1}, sort=[('_id', -1)])
        new_record = Room(1, "livingroom", last_record["temperature"], payload, last_record["lux"], 
                               datetime.datetime.now(tz).isoformat()).to_dictFormat()
        Room.insert_room_record(new_record)
    elif feed_id == "light": 
        last_record = Room.collection.find_one({"id": 1}, sort=[('_id', -1)])
        new_record = Room(1, "livingroom", last_record["temperature"], last_record["humidity"], payload, 
                               datetime.datetime.now(tz).isoformat()).to_dictFormat()
        Room.insert_room_record(new_record)
        
    elif feed_id == "chandeliers":
        last_record = Device.collection.find_one({"name": "chandeliers", "roomId": 1}, sort=[("_id", -1)])
        last_record["state"] = payload
        time = datetime.datetime.now(tz).isoformat()
        last_record["updated_at"] = time
        Device.collection.update_one({"_id": last_record["_id"]}, {"$set": last_record})

    elif feed_id == "control-fan":
        last_record = Device.collection.find_one({"name": "air_conditioner", "roomId": 1}, sort=[("_id", -1)])
        last_record["state"] = payload
        time = datetime.datetime.now(tz).isoformat()
        last_record["updated_at"] = time
        Device.collection.update_one({"_id": last_record["_id"]}, {"$set": last_record})

    elif feed_id == "ac":
        last_record = Device.collection.find_one({"name": "air_conditioner", "roomId": 1}, sort=[("_id", -1)])
        last_temp = last_record["current_temp"]
        last_record["current_temp"] = int(int(payload) / 100 * 40)
        time = datetime.datetime.now(tz).isoformat()
        last_record["updated_at"] = time
        Device.collection.update_one({"_id": last_record["_id"]}, {"$set": last_record})

        if last_record["state"] == "ON":
            if int(payload) / 100 * 40 < 20:
                newNotif = Notification("Nhắc nhở", 
                            f"Nhiệt độ đang dưới mức 20 độ", 
                            time, "điều hòa", "phòng khách", False).to_dictFormat()
                Notification.insert_notification(newNotif)
                socket_io.emit('Announce change', {"refetch": True})


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background() 
# try:
#     client.connect()
#     client.loop_background()  # Start the background loop for handling incoming messages
# except Exception as e:
#     print("Error:", e)
#     sys.exit(1)



from library.controllers import notificationsController
from library.controllers import authController
from library.controllers import refreshTokenController
from library.controllers import logoutController
from library.controllers import aiController
