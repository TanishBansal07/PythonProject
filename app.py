from flask import Flask, render_template,jsonify
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

if __name__ == "__main__":
    app.run(debug=True,port=8888)