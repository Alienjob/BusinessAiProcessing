from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from yandex_business_ai_landing.extensions import db


class UserPrompts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_prompt = db.Column(db.Text, nullable=True)
    describe_picture_prompt = db.Column(db.Text, nullable=True)
    write_article_prompt = db.Column(db.Text, nullable=True)
    write_issue_response_prompt = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('prompts', lazy=True))
    