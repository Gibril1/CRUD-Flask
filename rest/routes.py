from flask import request, jsonify
from rest import db, bcrypt, app
from rest.models import User, user_schema, users_schema, Products, product_schema, products_schema

import jwt
import datetime

# registration
@app.route('/register', methods=['POST'])
def register():
    response = {
        "data":{},
        "error_message": ""
    }

    username = request.json['username']
    email_address = request.json['email_address']
    password = request.json['password']

    if username == "" or email_address == "" or password == "":
        response["error_message"] = "Enter all fields"
        return response, 400

    # check if user is in database
    user = User.query.filter_by(email_address=email_address).first()
    if user:
        response["error_message"] = "User already exists"
        return response, 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email_address=email_address, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    user = user_schema.dump(user)
    response["data"] = user
    return response, 200

@app.route('/login', methods=["POST"])
def login():
    response = {
        
        "data": {},
        "error_message":""
    }

    email_address = request.json["email_address"]
    password = request.json["password"]

    if email_address == "" or password == "":
        response["error_message"] = "Please enter all fields"
        return response, 400
    
    user = User.query.filter_by(email_address=email_address).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({'user':user.username,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        user = user_schema.dump(user)
        response["data"]["auth_token"] = token
        response["data"]["users"]=user
        return response, 200
    else:
        response["error_message"] = "Invalid Credentials"

@app.route('/create', methods = ['POST'])
def create_product():
    response = {

        "data": {},
        "error_message": ""
    }

    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']

    if name == "" or price == "" or quantity == "":
        response["error_message"] = "Please enter all fields"
        return response, 200

        # entering data into the database
    product = Products(name=name, price=price, quantity=quantity)
    db.session.add(product)
    db.session.commit()

    product = product_schema.dump(product)
    response["data"] = product
    return response, 200

@app.route('/update/<int:id>', methods=['PUT'])
def update_product(id):
    response = {

        "data": {},
        "error_message": {}
    }
    product = Products.query.filter_by(id=id).first()
    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']

    product.name = name
    product.price = price
    product.quantity = quantity

    db.session.commit()

    product = product_schema.dump(product)
    response["data"] = product
    return response, 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    response = {

        "data": {},
        "error_message": {}
    }
    product = Products.query.filter_by(id=id).first()
    
    
    db.session.delete(product)
    db.session.commit()

    
    response["data"] = product.id
    return response, 200


    
