from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from yandex_business_ai_landing.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    company_description = db.Column(db.Text, nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
