import os
from dotenv import load_dotenv  # pip3 install python-dotenv

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
MONGO_URI = os.environ.get("DATABASE_URL")