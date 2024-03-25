from flask import render_template, request, jsonify
import datetime
import random
import pytz
from library import app
from library import db
from library.services import format
from library.models.notificationModel import Notification


# Create a time zone object for GMT+7
tz = pytz.timezone('Asia/Ho_Chi_Minh')

@app.route("/")
def get_all_notifications():
    return render_template("index.html")


@app.route("/get-all-notifications-by-day", methods=['GET'])
def get_all_notifs_by_day():
    day_to_get = request.args.get("day")
    print(day_to_get)
    notices = Notification.find_notifs_by_day(day_to_get)
    response = format.format_notifs(notices)

    return jsonify(response), 200


@app.route("/fake-insert-notifications", methods=['POST'])
def insert_into_notifications():
    res = {}
    type = random.choice(["Cảnh báo", "Nhắc nhở", "Thay đổi thành công", "Tai nạn xảy ra"])
    if type == "Tai nạn xảy ra":
        res = {
            "type": type,
            "content": "Tai nạn xảy ra",
            "place": "Tai nạn xảy ra",
            "created_at": datetime.datetime.now(tz).isoformat()
        }
    elif type == "Thay đổi thành công":
        res = {
            "type": type,
            "content": "Thay đổi thành công",
            "device": "Thay đổi thành công",
            "place": "Thay đổi thành công",
            "created_at": datetime.datetime.now(tz).isoformat()
        }
    elif type == "Nhắc nhở":
        res = {
            "type": type,
            "content": "Nhắc nhở",
            "created_at": datetime.datetime.now(tz).isoformat()
        }
    elif type == "Cảnh báo":
        res = {
            "type": type,
            "content": "Cảnh báo",
            "created_at": datetime.datetime.now(tz).isoformat()
        }
    
    db.notifications.insert_one(res)
    del res['_id']
    return jsonify(res), 200