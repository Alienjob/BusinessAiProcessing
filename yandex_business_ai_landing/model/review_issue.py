from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from yandex_business_ai_landing.extensions import db


class ReviewIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('review_issues', lazy=True))
    status = db.Column(db.String(50), nullable=False, default='draft')

    review_id = db.Column(db.String(50), nullable=True)
    review_author = db.Column(db.String(50), nullable=True)
    review_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    review_rate = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)

    company_story = db.Column(db.Text, nullable=False)
    company_response = db.Column(db.Text, nullable=True)
