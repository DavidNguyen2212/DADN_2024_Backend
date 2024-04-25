import os
from dotenv import load_dotenv  # pip3 install python-dotenv
from gevent import monkey
monkey.patch_all()

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
MONGO_URI = os.environ.get("DATABASE_URL")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_COOKIE_SECURE = os.environ.get("JWT_COOKIE_SECURE")
JWT_COOKIE_SAMESITE = os.environ.get("JWT_COOKIE_SAMESITE")