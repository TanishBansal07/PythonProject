from flask import Flask, render_template,jsonify,request,redirect, url_for   
import csv
from db import db
from models import Customer,Products
from pathlib import Path 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("./data").resolve()
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html",name = "Tanish",my_list = ["Home","Customers","Products","Orders"])
@app.route("/customers")
def customers_info():
    statement = db.select(Customer)
    records= db.session.execute(statement)
    results = records.scalars()
    return render_template("customers.html",customers=results)
@app.route("/products")
def products_info():
    statement = db.select(Products)
    records= db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html",products= results)
@app.route("/api/customers",methods=["POST"])
def customers_json():
    # ! This method uses the form in my html so not as per the project instructions
    data = request.form.to_dict()
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for("customers_info"))
@app.route("/api/customers/<int:id>",methods = ["PUT"])
def update_balance(id):
    data = request.get_json()
    customer = db.get_or_404(Customer,id)
    if "balance" not in data:
        return "Invalid Request",405
    balance = data["balance"]
    if not isinstance(balance,(int,float)):
        return "Invalid Request",405
    customer.balance = balance
    db.session.commit()
    return "",204
@app.route("/api/customers/<int:id>",methods =["DELETE"])
def delete_customer(id):
    customer = db.get_or_404(Customer,id)
    db.session.delete(customer)
    db.session.commit()
    return "",204
@app.route("/api/products", methods = ["POST"])
def add_product():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        return "Invalid Request", 400
    name = data["name"]
    price = data["price"]
    if not isinstance(name,str) or not isinstance(price,(int,float)):
        return "Invalid Request" , 400
    product = Products(name=name,price=price)
    db.session.add(product)
    db.session.commit()
    return "",201
@app.route("/api/products/<int:id>", methods = ["PUT"])
def update_product(id):
    data = request.get_json()
    prodcut = db.get_or_404(Products,id)
    if "name" not in data and "price" not in data:
        return "Invalid Request", 400
    if "name" in data:
        name = data["name"]
        if not isinstance(name,str):
            return "invalid Request",400
        prodcut.name = name
    if "price" in data:
        price = data["price"]
        if not isinstance(price,(int,float)):
            return "Invalid Request" , 400
        prodcut.price = price
    db.session.commit()
    return "",201 
@app.route("/api/products/<int:id>", methods = ["DELETE"])
def delete_product(id):
    data = request.get_json()
    product = db.get_or_404(Products,id)
    print(product)
    db.session.delete(product)
    db.session.commit()
    return "",204
if __name__ == "__main__":
    app.run(debug=True,port=8888) 