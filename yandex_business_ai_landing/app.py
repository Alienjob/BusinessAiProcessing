# app.py

import os
from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from yandex_business_ai_landing.extensions import db, login_manager, init_extensions
from yandex_business_ai_landing.routes import register_routes
from yandex_business_ai_landing.model import User

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'ThisIsASecretKey'
    app.config['JWT_SECRET_KEY'] = 'ThisIsASecretJWTKey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 100 * 1024 * 1024
    app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/photos'
    app.config['UPLOADS_DEFAULT_URL'] = '/_uploads/'
    app.config['UPLOADS_AUTOSERVE'] = True

    # Initialize Extensions
    init_extensions(app)
    CORS(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    register_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0')
