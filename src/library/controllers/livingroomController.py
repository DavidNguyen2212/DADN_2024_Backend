from flask import render_template, request, redirect, flash, url_for
from flask import jsonify
import datetime
import random
import pytz
from library import app
from library import db
from library.services import format
from library.connectIOserver import client
import json


@app.route("/modify-livingroom-states", methods=['POST'])
def modify_livingroom_states():
    req_data = dict(request.json)
    req_params = []
    for key, value in req_data.items():
        req_params.append((key, value))
    print("Params: ", req_params)

    last_record = db.livingroom.find_one({}, {"_id": False})
    new_record = format.format_lvroom(req_params[0][0], req_params[0][1] , last_record)
    client.publish("livingroom", json.dumps(new_record))

    return jsonify(last_record), 200