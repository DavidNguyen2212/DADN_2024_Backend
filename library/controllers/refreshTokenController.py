from library import app, db, bcrypt
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required, set_refresh_cookies
import datetime

users = db["users"]
@app.route("/refresh", methods=["GET"])
@jwt_required(refresh=True, locations='cookies')
def handleRefreshToken():
    cookie = request.cookies
    if cookie.get("refresh_token_cookie") is None:
        return jsonify({"Error": "No refresh token there!"}), 401
    # refresh_token = cookie["refresh_token_cookie"]

    identity = get_jwt_identity()
    if identity is None:
        return jsonify({"Error": "Forbidden"}), 403
    # Tạo access token mới
    access_token = create_access_token(identity=identity, fresh=False)
    
    return jsonify(access_token=access_token)


