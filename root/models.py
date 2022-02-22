from . import db
import datetime
from sqlalchemy.sql import func
from enum import Enum


# Foreign key sqlalchemy
#  Inheritance model sqlalchemy

class Role(Enum):
    admin = 'admin'
    doctor = 'doctor'
    finance = 'finance'


class Pays(Enum):
    cash = 'cash'
    card = 'card'
    cash_card = 'cash_card'


class BaseModel(db.Model):
    __tablename__ = 'base_model'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_creation = db.Column(db.DateTime(), default=datetime.datetime.today())


class BaseUser(BaseModel):
    __tablename__ = 'base_user'

    id = db.Column(db.Integer, db.ForeignKey('base_model.id'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    jmbg = db.Column(db.Integer, nullable=False, unique=True)  # Unique
    email = db.Column(db.String, unique=True)  # Unique
    address = db.Column(db.String)
    phone = db.Column(db.Integer, unique=True)  # Unique

    __mapper_args__ = {
        'polymorphic_identity': 'base_user',
    }


class User(BaseUser):
    _tablename__ = 'user'

    id = db.Column(db.Integer, db.ForeignKey('base_user.id'), primary_key=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(Role), default=Role.doctor)  # Enum polje


class Customers(BaseUser):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, db.ForeignKey('base_user.id'), primary_key=True)
    date_of_birth = db.Column(db.DateTime)
    personal_medical_history = db.Column(db.Text)
    family_medical_history = db.Column(db.Text)
    company_name = db.Column(db.Text)
    company_pib = db.Column(db.Integer)
    company_address = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'customers',
    }


class PriceList(BaseModel):
    __tablename__ = 'price_list'

    id = db.Column(db.Integer, db.ForeignKey('base_model.id'), primary_key=True)
    services = db.Column(db.String)
    medical_service = db.Column(db.String)
    price_of_service = db.Column(db.Integer)
    time_for_exam = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'price_list',
    }


class Review(BaseModel):
    __tablename__ = 'review'

    id = db.Column(db.Integer, db.ForeignKey('base_model.id'), primary_key=True)
    customers_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price_list_id = db.Column(db.Integer, db.ForeignKey('price_list.id'), nullable=False)
    price_of_service = db.Column(db.Integer)
    doctor_opinion = db.Column(db.Text)


class ReviewDocument(BaseModel):
    __tablename__ = 'review_document'

    id = db.Column(db.Integer, db.ForeignKey('base_model.id'), primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'review_document',

    }


class Payments(BaseModel):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, db.ForeignKey('base_model.id'), primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    customers_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price_list_id = db.Column(db.Integer, db.ForeignKey('price_list.id'), nullable=False)
    price_of_service = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean)
    payment_made = db.Column (db.Enum(Pays), default=Pays.card)# Enum cash, card or cash_card
