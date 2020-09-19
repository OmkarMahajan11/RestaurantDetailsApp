from flask import Blueprint
from flask import request
from user_blueprint import validate
import time
import jwt
import json
import csv

dish = Blueprint("dish", __name__)

@dish.route("/create", methods=["POST"])
def create():
    headers = ["id","name","description","vegetarian"]
    with open("data/dishes.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if any(int(i["name"]) == request.json["name"] for i in l):
        return json.dumps({"result":"fail", "message":"dish already exists"})    

    l.append({"id":request.json["id"], "name":request.json["name"], "description":request.json["description"], "vegetarian":request.json["vegetarian"]})    

    with open("data/dishes.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"successsfully created"})

@dish.route("/get", methods=["POST"])
def dish_details():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res
    
    with open("data/dishes.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    return json.dumps({"dishes":l})

@dish.route("/delete/<name>", methods=["DELETE"])
def delete(name):
    res = validate(request.json["auth_token"])
    if res is not None:
        return res    

    headers = ["id","name","description","vegetarian"]
    with open("data/dishes.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)
    
    if name not in [i["name"] for i in l]:
        return json.dumps({"message":"no such dish"})

    for i in l:
        if name == i["name"]:
            l.remove(i)

    with open("data/dishes.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)                

    return json.dumps({"result":"dish deleted successfully"})        