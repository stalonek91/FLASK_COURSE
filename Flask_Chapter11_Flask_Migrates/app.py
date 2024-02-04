from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(40))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    total = db.Column(db.Integer)


def create_app():
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql11681644:A1f9w3ULIM@sql11.freemysqlhosting.net/sql11681644'

    db.init_app(app)
    migrate.init_app(app, db)

    
    return app
