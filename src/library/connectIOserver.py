from Adafruit_IO import MQTTClient
import sys
import json
from library import db
from library.services.format import format_lvroom
from library import socket_io
from flask_socketio import emit, send
from library.models.notificationModel import Notification
import datetime, pytz

tz = pytz.timezone('Asia/Ho_Chi_Minh')
AIO_FEED_ID = ['livingroom']
AIO_USERNAME = 'david_nguyen7603'
AIO_KEY = 'aio_rUVY94t2nKtEgGtMwIsEySHRTacA'

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
    # print(type(payload))
    payload_to_dict = json.loads(payload)
    if feed_id == "livingroom":
        last_record = db["livingroom"].find_one(sort=[('_id', -1)])
        db["livingroom"].insert_one(payload_to_dict)
        changed_field = handleFindChange(db, "livingroom", payload_to_dict, last_record)
        print(changed_field)
        if changed_field is not None:
            if changed_field != "tempAC":
                newNotif = Notification("Thay đổi thành công", 
                    "Bạn đã thay đổi thành công trạng thái thiết bị", 
                    datetime.datetime.now(tz).isoformat(), str(changed_field), "phòng khách").to_dictFormat()
                Notification.insert_notification(newNotif)
                socket_io.emit('Announce change', {"refetch": True})



def handleFindChange(dbs, collection, new_record, last_record):
    if last_record is None:
        return None  
    for key in new_record.keys():
        if key not in ["temperature", "humidity", "lux", "updated_at", "_id"]:
            if new_record[key] != last_record.get(key):
                return key
    return None  




client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

try:
    client.connect()
    client.loop_background()  # Start the background loop for handling incoming messages
except Exception as e:
    print("Error:", e)
    sys.exit(1)