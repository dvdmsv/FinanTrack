from flask import Blueprint, request, jsonify
from Modelos import User
from db import db
from utils import token_required
from flask_bcrypt import Bcrypt
import jwt
import datetime
from config import Config

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, Config.SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': 'Login exitoso',
            'userId': user.id,
            'token': token
        }), 200
    return jsonify({'message': 'Credenciales incorrectas', 'status': 'error'}), 401

@auth_bp.route('/registro', methods=['POST', 'OPTIONS'])
def registro():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight check passed'}), 200

    data = request.json
    username = data.get('username')
    password = data.get('password')
    saldo = data.get('saldo')

    if not username or not password:
        return jsonify({'messaje': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'messaje': 'Username already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password, saldo=saldo)

    try:
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, Config.SECRET_KEY, algorithm='HS256')

        return jsonify({
            'messaje': 'User registered successfully',
            'token': token
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 500
    
@auth_bp.route('/validToken', methods=['GET', 'OPTIONS'])
@token_required
def validToken(decoded):
    return jsonify({"message": "Token valid"}), 200