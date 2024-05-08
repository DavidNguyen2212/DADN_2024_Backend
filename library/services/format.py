import datetime, pytz, re
import requests
import json
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

def handleRegex(reg: str):
    # Sử dụng regex để tìm và thay thế tất cả các ký tự số trong chuỗi thành một khoảng trắng
    num = re.search(r'\d+', reg)
    noNumReg = re.sub(r'\d+', '', reg)
    if num:
        number = int(num.group()) 
        return number, noNumReg 
    else:
        return None, noNumReg
    
def get_Goldprice():
    api_url = 'http://api.btmc.vn/api/BTMCAPI/getpricebtmc?key=3kd8ub1llcg9t45hnoh8hmn7t5kc2v'  # Thay thế URL này bằng URL thực tế của API Python

    # Gửi yêu cầu GET tới API Python
    response = requests.get(api_url)

    # Trả về kết quả từ API Python
    if response.status_code == 200:
        data = response.json()["DataList"]["Data"]
        text_response = "Giá vàng hôm nay như sau: "
        for i in range(3):
            name = data[i][f"@n_{i+1}"]
            kara = data[i][f"@k_{i+1}"]
            inprice = data[i][f"@pb_{i+1}"]
            outprice = data[i][f"@ps_{i+1}"]
            input_time = data[i][f"@d_{i+1}"]
            text_response = text_response + name + ", hàm lượng kara: " + kara + ", giá mua vào: " + inprice + ", giá bán ra: "+ outprice + ", cập nhật lúc: " + input_time + ". " 

        return text_response
