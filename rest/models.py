from cgi import print_exception
from dataclasses import fields
from unicodedata import name
from rest import db, ma 

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email_address, password):
        self.username = username
        self.email_address = email_address
        self.password = password

    def __repr__(self) -> str:
        return f'User({self.username}, {self.email_address})'

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email_address')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price, quantity) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity


    def __repr__(self) -> str:
        return f'Product({self.name},{self.price}, {self.quantity})'

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'price', 'quantity')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
        