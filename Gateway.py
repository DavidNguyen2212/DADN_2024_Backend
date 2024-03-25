import sys
import random
import time
import datetime
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
import pymongo as mongo
import json
import pytz

# Tạo đối tượng múi giờ cho GMT+7
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Tạo thời gian hiện tại theo múi giờ GMT+7
current_time = datetime.datetime.now(tz)
# Connect to mongoDB
client = mongo.MongoClient('mongodb://localhost:27017')
db = client['smart_home']
lvroom_collection = db["livingroom"]


AIO_FEED_ID = ['livingroom']
AIO_USERNAME = 'david_nguyen7603'
AIO_KEY = 'aio_oTlw384YUp83sRxOSHHSbfVce4tp'

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
    print("Nhận dữ liệu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    comPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            comPort =  (splitPort[0])
    return comPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[1] == "TEMP":
            client.publish("bbc-temp", splitData[2])
        if splitData[1] == "HUMI":
            client.publish("bbc-humi", splitData[2])
    except:
        pass

def readSerial():
    bytestoread = ser.inWaiting()
    if bytestoread > 0:
        global mess
        mess = mess + ser.read(bytestoread).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end+1])
            if end == len(mess):
                mess = ""
            else:
                mess = mess[end+1:]

def lorem_ipsum():
    value = {
            "automode": False,
            "temp": random.randint(25, 35), "humidity": random.randint(25, 35), "lux": 600,
            "light": {
                "chandeliers": "on",
                "light1": "on",
                "light2": "on"
            },
            "air_conditioner": {
                "state": "on",
                "current_temp": random.randint(20, 30),
            },
            "updated_at": current_time.isoformat()
        }
    return value

# Create an MQTT Client object
# Press on MQTTClient, visit its .py source, replace initialize MQTT Client stmt by:
# self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
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

# The script will continue running in the background to handle MQTT messages
try:
    while True:
        # if isMicrobitConnected:
        #     readSerial()
        # time.sleep(1)
        fake_value = lorem_ipsum()
        time.sleep(1)
        client.publish("livingroom", json.dumps(fake_value))
        lvroom_collection.insert_one(fake_value)
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting...")
    print("Exited!")
    sys.exit(0)