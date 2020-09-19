from flask import Blueprint
from flask import request
from user_blueprint import validate
import time
import jwt
import json
import csv

restaurant = Blueprint("restaurant", __name__)

@restaurant.route("/create", methods=["POST"])
def create():
    headers = ["id","name","address"]
    with open("data/restaurants.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if any(int(i["name"]) == request.json["name"] for i in l):
        return json.dumps({"result":"fail", "message":"restaurant already exists"})

    l.append({"id":request.json["id"], "name":request.json["name"], "address":request.json["address"]})

    with open("data/restaurants.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"successsfully created"})

@restaurant.route("/get", methods=["POST"])
def details():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    with open("data/restaurants.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    return json.dumps({"restaurants":l})    

@restaurant.route("/delete/<name>", methods=["DELETE"])
def delete(name):
    res = validate(request.json["auth_token"])
    if res is not None:
        return res    

    headers = ["id","name","address"]
    with open("data/restaurants.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if name not in [i["name"] for i in l]:
        return json.dumps({"message":"no such restaurant"})

    for i in l:
        if name == i["name"]:
            l.remove(i)

    with open("data/restaurants.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)                

    return json.dumps({"result":"restaurant deleted successfully"})               
