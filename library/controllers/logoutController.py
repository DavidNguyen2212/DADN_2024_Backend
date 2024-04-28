from library import app, db, bcrypt
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import create_access_token,get_csrf_token, unset_refresh_cookies, unset_jwt_cookies, get_jwt_identity, create_refresh_token, jwt_required, set_refresh_cookies
import datetime

# FE nhớ thêm vào header là X-CSRF-TOKEN: get từ cookies để logout được
users = db["users"]
@app.route("/logout", methods=["DELETE"])
@jwt_required(refresh=True, locations=['headers', 'cookies'], verify_type=False) # ['headers', 'cookies']
def handleLogout():
    try:
        cookie = request.cookies
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


