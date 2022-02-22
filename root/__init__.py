from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "Clinic1.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dwounufuhf83dwndhi8t666'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:myPassword@localhost:5432/Clinic1"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import BaseUser, User, Pricelist, Customers, Reviewdocument, Payments
    create_database(app)

    return app


def create_database(app):

        db.create_all(app=app)
        print('Created Database!')
