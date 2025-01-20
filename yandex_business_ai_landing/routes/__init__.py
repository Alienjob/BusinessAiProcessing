# routes/__init__.py

from .auth_routes import auth_routes
from .post_routes import post_routes
from .file_routes import file_routes
from .personal_cabinet_routes import personal_cabinet_routes
from .home_routes import home_routes
from yandex_business_ai_landing.api.api_routes import api_routes
from yandex_business_ai_landing.api.auth import auth
from .user_prompts_routes import user_prompts_routes
from .review_routes import review_routes

def register_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(post_routes)
    app.register_blueprint(file_routes)
    app.register_blueprint(personal_cabinet_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(api_routes)
    app.register_blueprint(auth)
    app.register_blueprint(user_prompts_routes)
    app.register_blueprint(review_routes)