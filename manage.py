import csv
from app import app
from db import db
import models
def create_tables():
    with app.app_context():
        db.create_all()
def drop_tables():
    with app.app_context():
        db.drop_all()
def costumer_table():
    with app.app_context():
        with open("./data/customers.csv","r",newline="") as f:
            data = csv.DictReader(f)
            for i in data:
                customer = models.Customer(name = i["name"],phone = i["phone"])
                db.session.add(customer)
            db.session.commit()
def product_table():
    with app.app_context():
        with open("./data/products.csv","r",newline="") as f:
            data = csv.DictReader(f)
            for i in data:
                product = models.Products(name = i["name"],price = i["price"])
                db.session.add(product)
            db.session.commit()
if __name__ == "__main__":
    drop_tables()
    create_tables()
    costumer_table()
    product_table()