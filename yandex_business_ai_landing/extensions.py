# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_executor import Executor
from flask_migrate import Migrate

# Initialize Extensions
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
executor = Executor()
photos = UploadSet('photos', IMAGES)

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    executor.init_app(app)
    configure_uploads(app, photos)
    Migrate(app, db)