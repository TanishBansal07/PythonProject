from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from db import db
from models import Customer, Products, Order, ProductOrder

# Create a Blueprint for the customers API
api_order_bp = Blueprint("api_orders", __name__)


@api_order_bp.route("", methods=["POST"])
def add_order():
    data = request.get_json()
    if "customer_id" not in data:
        return "Invalid Request", 400
    customer_id = data["customer_id"]
    customer = db.get_or_404(Customer, customer_id)
    order = Order(customer=customer)
    db.session.add(order)
    for i in data["items"]:
        product_name = i["name"]
        statement = db.select(Products).where(Products.name == product_name)
        product = db.session.execute(statement).scalar()
        if product is None:
            # skip this product
            continue
        product = db.get_or_404(Products, product.id)

        quantity = i["quantity"]
        product_order = ProductOrder(order=order, product=product, quantity=quantity)
        db.session.add(product_order)

    db.session.commit()
    return "", 201


@api_order_bp.route("/<int:id>/delete", methods=["POST"])
def delete_order(id):
    order = db.get_or_404(Order, id)
    if order.processed is not None:
        return redirect(url_for("html.orders"))
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("html.orders"))


@api_order_bp.route("/<int:id>", methods=["PUT", "POST"])
def process_order(id):
    data = request.form.to_dict()
    print(data)
    order = db.get_or_404(Order, id)
    process = True
    if process:
        if "strategy" not in data:
            print("herejjj")
            strategy = "adjust"
        else:
            strategy = data["strategy"]
            print(strategy)
        print(strategy)
        if strategy not in ["adjust", "reject", "ignore"]:
            return "Invalid Request", 400
        if not order.process(strategy):
            return "Invalid Request", 400

    return redirect(url_for("html.orders"))
