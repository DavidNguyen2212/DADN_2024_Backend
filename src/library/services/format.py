import datetime, pytz
######
## Format function for the controllers
######
def format_notifs(notices: any):
    response = []
    unReadCount = 0
    for notice in notices:
        if notice["isRead"] == False:
            unReadCount = unReadCount + 1
        if notice["type"] == "Tai nạn xảy ra":
            res = {
                "type": notice["type"],
                "content": notice["content"],
                "place": notice["place"],
                "created_at": notice["created_at"],
                "isRead": notice["isRead"]
            }
            response += [res]
        elif notice["type"] == "Thay đổi thành công":
            res = {
                "type": notice["type"],
                "content": notice["content"],
                "device": notice["device"],
                "place": notice["place"],
                "created_at": notice["created_at"],
                "isRead": notice["isRead"]
            }
            response += [res]
        elif notice["type"] == "Nhắc nhở":
            res = {
                "type": notice["type"],
                "content": notice["content"],
                "created_at": notice["created_at"],
                "isRead": notice["isRead"]
            }
            response += [res]
        elif notice["type"] == "Cảnh báo":
            res = {
                "type": notice["type"],
                "content": notice["content"],
                "created_at": notice["created_at"],
                "isRead": notice["isRead"]
            }
            response += [res]
        res["_id"] = str(notice["_id"])
    response.insert(0, {"unReadCount": unReadCount})
    return response


tz = pytz.timezone('Asia/Ho_Chi_Minh')

def format_lvroom(field, value, last_record):
    new_record = {
        "automode": last_record["automode"],
        "temp": last_record["temp"], "humidity": last_record["humidity"], "lux": last_record["lux"],
        "chandeliers": last_record["chandeliers"],
        "light1": last_record["light1"],
        "light2": last_record["light2"],
        "AC": last_record["AC"],
        "tempAC": last_record["tempAC"],
        "updated_at": last_record["updated_at"]
    }
    # if field in ["automode", "temp", "humidity", "lux"]:
    #     new_record[field] = value
    # elif field in ["chandeliers", "light1", "light2"]:
    #     new_record["light"][field] = value
    # elif field in ["state", "current_temp"]:
    #     new_record["air_conditioner"][field] = value
    if field is not None and value is not None:
        new_record[field] = value
        new_record["updated_at"] = datetime.datetime.now(tz).isoformat()

    return new_record