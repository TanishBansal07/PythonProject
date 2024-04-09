from flask import Flask, render_template, jsonify, request, redirect, url_for
import csv
from db import db
from models import Customer, Products, Order, ProductOrder
from pathlib import Path
from routes import api_customers_bp , api_products_bp,api_order_bp,htmls_bp
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("./data").resolve()
db.init_app(app)
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")

app.register_blueprint(api_products_bp, url_prefix="/api/products")

app.register_blueprint(api_order_bp, url_prefix="/api/orders")
app.register_blueprint(htmls_bp, url_prefix="/")
if __name__ == "__main__":
    app.run(debug=True, port=8888)
