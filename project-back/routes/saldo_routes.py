from flask import Blueprint, request, jsonify
from Modelos import User
from db import db
from utils import token_required

saldo_bp = Blueprint('saldo', __name__)

@saldo_bp.route('/setSaldo', methods=['POST'])
@token_required
def setSaldo(decoded):
    data = request.json
    userId = decoded['user_id']

    user = User.query.filter_by(id=userId).first_or_404()

    # Actualizar saldo con el valor validado
    user.saldo = float(data['saldo'])
    db.session.commit()

    return jsonify({
        "message": "Saldo actualizado",
        "saldo": user.saldo
    }), 200

@saldo_bp.route('/getSaldo', methods=['GET'])
@token_required
def getSaldo(decoded):
    userId = decoded['user_id']
    
    # Obtener usuario, si no existe, devuelve 404 automáticamente
    user = User.query.filter_by(id=userId).first_or_404()

    return jsonify({
        "saldo": float(user.saldo)  # Aseguramos que el saldo se devuelve en formato numérico
    }), 200

