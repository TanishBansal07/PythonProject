from flask import Blueprint, jsonify, request, redirect, url_for
from db import db
from models import Customer
# Create a Blueprint for the customers API
api_customers_bp = Blueprint("api_customers", __name__)
@api_customers_bp.route("/", methods=["GET"])
def get_customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return jsonify([cust.to_json() for cust in results])
@api_customers_bp.route("/<int:id>", methods=["PUT"])
def update_balance(id):
    data = request.get_json()
    customer = db.get_or_404(Customer, id)
    if "balance" not in data:
        return "Invalid Request", 405
    balance = data["balance"]
    if not isinstance(balance, (int, float)):
        return "Invalid Request", 405
    customer.balance = balance
    db.session.commit()
    return "", 204
@api_customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.get_or_404(Customer, id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204
@api_customers_bp.route("/api/customers", methods=["POST"])
def customers_json():
    # ! This method uses the form in my html so not as per the project instructions
    data = request.form.to_dict()
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for("html.customers_info"))