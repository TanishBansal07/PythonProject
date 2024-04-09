from flask import Blueprint, jsonify, request, redirect, url_for
from db import db
from models import Customer, Products,Order, ProductOrder

# Create a Blueprint for the customers API
api_products_bp = Blueprint("api_products", __name__)


@api_products_bp.route("/", methods=["POST"])
def add_product():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        return "Invalid Request", 400
    name = data["name"]
    price = data["price"]
    if not isinstance(name, str) or not isinstance(price, (int, float)):
        return "Invalid Request", 400
    product = Products(name=name, price=price)
    db.session.add(product)
    db.session.commit()
    return "", 201


@api_products_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    prodcut = db.get_or_404(Products, id)
    if "name" not in data and "price" not in data:
        return "Invalid Request", 400
    if "name" in data:
        name = data["name"]
        if not isinstance(name, str):
            return "invalid Request", 400
        prodcut.name = name
    if "price" in data:
        price = data["price"]
        if not isinstance(price, (int, float)):
            return "Invalid Request", 400
        prodcut.price = price
    db.session.commit()
    return "", 201


@api_products_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    data = request.get_json()
    product = db.get_or_404(Products, id)
    print(product)
    db.session.delete(product)
    db.session.commit()
    return "", 204
