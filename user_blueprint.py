from flask import Blueprint
from flask import request
import jwt
import time
import csv
import json

user = Blueprint("user", __name__)

def validate(auth_token):
    data = jwt.decode(auth_token, "imperium")

    if not data["expire"] >= time.time():
        return json.dumps({"message":"token expired"})



@user.route("/register", methods=["POST"])
def register():

    with open("data/users.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    for i in l:
        if i["id"] == str(request.json["id"]) or i["email"] == request.json["email"]:
            return json.dumps({"registration":"Failed", "message":"user already present"})

    l.append({"id":request.json["id"], "name":request.json["name"],"email":request.json["email"], "gender":request.json["gender"],"password":request.json["password"], "contact_number":request.json["contact_number"], "address":request.json["address"]})

    headers = ["id","name","email","gender","password","contact_number","address"]
    with open("data/users.csv", 'w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"registration":"Successful"})

@user.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    with open("data/users.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    found = False
    for i in l:
        if i["email"] == email and i["password"] == password:
            found = True
            break

    if not found:
        return json.dumps({"login":"Failed", "message":"invalid credentials"})

    payload = {'email': email, 'message': 'logged_in', 'expire': time.time()+1000}
    key = "imperium"

    encode_jwt = jwt.encode(payload, key)
    return json.dumps({"login":"Successful", "auth_token":encode_jwt.decode()})

@user.route("/modify", methods=["PATCH"])
def modify():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res
    
    headers = ["id","name","email","gender","password","contact_number","address"]
    decoded = jwt.decode(request.json["auth_token"], key="imperium")

    with open("data/users.csv", 'r') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    for i in l:
        if i["email"] == decoded["email"]:
            i["password"] = request.json["new_password"]

    with open("data/users.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)

    return json.dumps({"result":"user modified successfully"})

@user.route("/delete/<name>", methods=["DELETE"])
def delete(name):
    res = validate(request.json["auth_token"])
    if res is not None:
        return res

    headers = ["id","name","email","gender","password","contact_number","address"]
    with open("data/users.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    if name not in [i["name"] for i in l]:
        return json.dumps({"message":"no such user"})

    for i in l:
        if name == i["name"]:
            l.remove(i)

    with open("data/users.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(l)                

    return json.dumps({"result":"user deleted successfully"})  

@user.route("/get", methods=["GET"])
def user_details():
    res = validate(request.json["auth_token"])
    if res is not None:
        return res
    
    with open("data/users.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        l = list(reader)

    return json.dumps({"users":l})