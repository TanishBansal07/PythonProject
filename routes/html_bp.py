from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from db import db
from models import Customer, Products, Order, ProductOrder
# Create a Blueprint for the customers API
htmls_bp = Blueprint("html", __name__)
@htmls_bp.route("/")
def home():
    return render_template(
        "home.html", name="Tanish", my_list=["Home", "Customers", "Products", "Orders"]
    )


@htmls_bp.route("/customers")
def customers_info():
    statement = db.select(Customer)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("customers.html", customers=results)


@htmls_bp.route("/customers/<int:id>", methods=["GET"])
def customer_info(id):
    customer = db.get_or_404(Customer, id)
    return render_template("customer.html", customer=customer)
@htmls_bp.route("/products")
def products_info():
    statement = db.select(Products)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products=results)
@htmls_bp.route("/orders", methods=["GET"])
def orders():
    statement = db.select(Order)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("orders.html", orders=results)
@htmls_bp.route("/orders/<int:id>", methods=["GET"])
def orders_info(id):
    order = db.get_or_404(Order, id)
    return render_template("order.html", order=order)