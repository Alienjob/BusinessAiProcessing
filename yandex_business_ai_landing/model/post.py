from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from yandex_business_ai_landing.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(255), nullable=False)
    photo_description = db.Column(db.Text, nullable=True)
    post_content = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='draft')
    created_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    posting_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    user_file_id = db.Column(db.Integer, db.ForeignKey('user_file.id'), nullable=False)
    user_file = db.relationship('UserFile', backref=db.backref('posts', lazy=True))