from flask import Blueprint, request, jsonify
from utils import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/getUserData', methods=['GET'])
@token_required
def getUserData(decoded):
    return jsonify({
            'message': 'Token is valid',
            'user_data': decoded
        }), 200