from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from yandex_business_ai_landing.extensions import db

class LongOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    request = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    error = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('operations', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'request': self.request,
            'response': self.response,
            'error': self.error
        }