from library import app, db, bcrypt
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required, set_refresh_cookies
import datetime

users = db["users"]
@app.route("/register", methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    if users.find_one({"username": username}) is not None:
        return jsonify({"Error": "Tên người dùng đã tồn tại. Hãy thử tên khác."}), 400
    
    # Hashed password
    hashed_pwd = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
    users.insert_one({
        "username": username, "password": hashed_pwd
    })

    return jsonify({'Message': 'Đăng ký thành công'}), 201

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")

    user_found = users.find_one({"username": username})
    if user_found is None:
        return jsonify({"Error": "Tài khoản không tồn tại!"}), 401
    elif bcrypt.check_password_hash(user_found["password"], data.get("password")):
        # Kiểm tra xem người dùng đã đăng nhập trước đó chưa
        if user_found.get("refresh_token") is not None:
            return jsonify({"Error":"Bạn hiện đã đăng nhập!"}), 403 
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=10))
        refresh_token = create_refresh_token(identity=username, expires_delta=datetime.timedelta(days=1))
        print("refresh token: ", refresh_token)

        # Thêm trường refresh token của người dùng trong cơ sở dữ liệu
        users.update_one({"_id": user_found["_id"]}, {"$set": {"refresh_token": refresh_token}})
        response = make_response(jsonify({"access_token": access_token}))
        response.set_cookie('abcid', 'Hello', domain="dadn-2024-team-blue-whale-1h2hw9qrf.vercel.app", secure=True, samesite='None', max_age=63072000)
        set_refresh_cookies(response, refresh_token, max_age=24*60*60*1000)
        # print(jsonify(response))
        return response, 200
    else:
        return jsonify({"Error": "Bạn đã nhập sai mật khẩu!"}), 401
    
