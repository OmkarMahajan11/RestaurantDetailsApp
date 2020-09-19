from flask import Blueprint
from flask import request
from user_blueprint import validate
import time
import jwt
import json
import csv

booking = Blueprint("booking", __name__)

@booking.route("/create", methods=["POST"])
def create():
    headers = ["id","user_id","dish_id","restaurant_id","ordered_at"]
    with open("data/booking.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    l.append({"id":request.json["id"], "user_id":request.json["user_id"], "restaurant_id":request.json["restaurant_id"], "ordered_at":request.json["ordered_at"]})  

    with open("data/booking.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"successsfully created"})
