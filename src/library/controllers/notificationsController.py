from flask import render_template, request, jsonify
import datetime
import random
import pytz
from library import app
from library import db
from library.services import format
from library.models.notificationModel import Notification
from bson import ObjectId
from flask_jwt_extended import jwt_required

# Create a time zone object for GMT+7
tz = pytz.timezone('Asia/Ho_Chi_Minh')

@app.route("/")
def get_all_notifications():
    return render_template("index.html")


@app.route("/get-all-notifications-by-day", methods=['GET'])
@jwt_required()
def get_all_notifs_by_day():
    day_to_get = request.args.get("day")
    notices = Notification.find_notifs_by_day(day_to_get)
    response = format.format_notifs(notices)

    return jsonify(response), 200

@app.route("/get-unread-notifs-amount", methods=['GET'])
def get_unread_notifs_amount():
    start_point = datetime.datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end_point = datetime.datetime.now(tz).isoformat()
    
    # Searching
    notif_num = Notification.collection.count_documents(
        {
        "created_at": {
        "$gte": start_point,
        "$lte": end_point
        }, 
        "isRead": False
    }) 
    
    return jsonify({"newNotifsToday": notif_num}), 200

@app.route("/check-all-notifs/<string:checked_day>", methods=['PUT'])
def mark_all_notifs(checked_day):
    notices = Notification.find_notifs_by_day(checked_day)
    print(checked_day)
    for notice in notices:
        if notice["isRead"] == False:
            notice["isRead"] = True
            Notification.collection.replace_one({"_id": notice["_id"]}, notice)  

    return jsonify({"Successful": "All Notifications marked as read."}), 200
    
@app.route("/mark-as-read/<string:_id>", methods=['PUT'])
def mark_notif_as_read(_id):
    # Turn _id to ObjectId of Mongo to work on it
    _id = ObjectId(_id)

    result = Notification.collection.update_one({"_id": _id}, {"$set": {"isRead": True}})  
    if result.modified_count > 0:
        return jsonify({"Successful": "Notification marked as read."}), 200
    else:
        return jsonify({"Error": "Notification not found."}), 404

@app.route("/fake-insert-notifications", methods=['POST'])
def insert_into_notifications():
    res = {}
    type = random.choice(["Cảnh báo", "Nhắc nhở", "Thay đổi thành công", "Tai nạn xảy ra"])
    if type == "Tai nạn xảy ra":
        res = {
            "type": type,
            "content": "Tai nạn xảy ra",
            "place": "Tai nạn xảy ra",
            "created_at": datetime.datetime.now(tz).isoformat(),
            "isRead": False
        }
    elif type == "Thay đổi thành công":
        res = {
            "type": type,
            "content": "Thay đổi thành công",
            "device": "Thay đổi thành công",
            "place": "Thay đổi thành công",
            "created_at": datetime.datetime.now(tz).isoformat(),
            "isRead": False
        }
    elif type == "Nhắc nhở":
        res = {
            "type": type,
            "content": "Nhắc nhở",
            "created_at": datetime.datetime.now(tz).isoformat(),
            "isRead": False
        }
    elif type == "Cảnh báo":
        res = {
            "type": type,
            "content": "Cảnh báo",
            "created_at": datetime.datetime.now(tz).isoformat(),
            "isRead": False
        }
    Notification.insert_notification(res)
    del res['_id']
    return jsonify(res), 200