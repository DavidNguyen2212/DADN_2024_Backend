from library import socket_io
from library import db
from flask_socketio import send, emit
from flask import request

# @socket_io.on('connect')
# def connected():
#     print("Client is connected!")


# @socket_io.on('new_notifications')
# def supply_new_notifications():
#     emit('update-notification-list')

# @socket_io.on('disconnect')
# def disconnected():
#     print("Client is disconnected!")
#     emit("connect", {
#         "data": f"User id: {request.sid} has disconnected!"
#     })