from flask import request, jsonify
from functools import wraps
import secrets
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Expired token'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 400

        return f(decoded, *args, **kwargs)
    return decorated_function
