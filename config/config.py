import os
from dotenv import load_dotenv  # pip3 install python-dotenv

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
MONGO_URI = os.environ.get("DATABASE_URL")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE")
# JWT_COOKIE_SAMESITE = os.environ.get("JWT_COOKIE_SAMESITE")
JWT_COOKIE_SAMESITE = 'None'
PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")
MQTT_BROKER_URL = 'io.adafruit.com'
MQTT_BROKER_PORT = 443
MQTT_USERNAME = os.environ.get("AIO_USERNAME")
MQTT_PASSWORD = os.environ.get("AIO_KEY")
