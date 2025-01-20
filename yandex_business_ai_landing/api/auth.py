from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from yandex_business_ai_landing.model import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401