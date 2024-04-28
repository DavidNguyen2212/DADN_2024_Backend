from library import app, db, bcrypt
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import create_access_token,get_csrf_token, unset_refresh_cookies, unset_jwt_cookies, get_jwt_identity, create_refresh_token, jwt_required, set_refresh_cookies,verify_jwt_in_request
import datetime

# FE nhớ thêm vào header là X-CSRF-TOKEN: get từ cookies để logout được

# Lệnh phía trên. Không khả dụng. Verify bằng tay 
users = db["users"]
@app.route("/logout", methods=["DELETE"])
@jwt_required(refresh=True, locations=['headers', 'cookies'], verify_type=False) # ['headers', 'cookies']
def handleLogout():
    try:
        # cookie = request.cookies
        # csrf_refresh_token = request.cookies.get('csrf_refresh_token')

        # if not csrf_refresh_token:
        #     return jsonify({"Error": "Cookie 'csrf_refresh_token' không tồn tại trong request."}), 401
        
        # print(csrf_refresh_token)
        identity = get_jwt_identity()

        if identity is None:
            response = make_response(jsonify({"Notice": "Không tìm thấy thông tin xác thực, nhưng JWT cookies đã được xóa"}))
            unset_refresh_cookies(response)
            return response, 403

        user_found = users.find_one({"username": identity})

        if user_found is None:
            return jsonify({"Error": "Người dùng không tồn tại!"}), 404

        # Xóa refresh token của User trong database
        users.update_one({"_id": user_found["_id"]}, {"$unset": {"refresh_token": ""}})
        response = make_response(jsonify({"Success": "Đăng xuất thành công"}))
        unset_refresh_cookies(response)
        return response, 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


