import csv
from app import app
from db import db
from models import Customer, Products, Order, ProductOrder
import random
from sqlalchemy.sql import functions as func

def create_tables():
    with app.app_context():
        db.create_all()


def drop_tables():
    with app.app_context():
        db.drop_all()


def costumer_table():
    with app.app_context():
        with open("./data/customers.csv", "r", newline="") as f:
            data = csv.DictReader(f)
            for i in data:
                customer = Customer(name=i["name"], phone=i["phone"],balance= random.randint(1, 1000))
                db.session.add(customer)
            db.session.commit()


def product_table():
    with app.app_context():
        with open("./data/products.csv", "r", newline="") as f:
            data = csv.DictReader(f)
            for i in data:
                product = Products(name=i["name"], price=i["price"],available= random.randint(1, 100))
                db.session.add(product)
            db.session.commit()


if __name__ == "__main__":
    drop_tables()
    create_tables()
    costumer_table()
    product_table()
# seeding orders and product orders with random data
    with app.app_context():
        for i in range(10):
            statement = db.select(Customer).order_by(func.random()).limit(1)
            customer = db.session.execute(statement).scalar()
            order = Order(customer = customer)
            db.session.add(order)           
            product_statement = db.select(Products).order_by(func.random()).limit(1)
            product = db.session.execute(product_statement).scalar()
            random_quantity = random.randint(1, 100)
            product_order = ProductOrder(order = order, product = product, quantity = random_quantity)
            db.session.add(product_order)
            product_statement = db.select(Products).order_by(func.random()).limit(1)

            product = db.session.execute(product_statement).scalar()
            random_quantity = random.randint(10, 20)
            product_order = ProductOrder(order = order, product = product, quantity = random_quantity) 
            db.session.add(product_order)

        db.session.commit()


    print("Database seeded")