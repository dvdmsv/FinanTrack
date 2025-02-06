from flask import Blueprint, request, jsonify
from db import db
from Modelos import PagoRecurrente
from datetime import datetime

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/agregarPagoRecurrente', methods=['POST'])
def agregar_pago_recurrente():
    data = request.json
    nuevo_pago = PagoRecurrente(
        user_id=data["user_id"],
        categoria_id=data["categoria_id"],
        cantidad=data["cantidad"],
        concepto=data["concepto"],
        tipo=data["tipo"],
        frecuencia=data["frecuencia"],
        siguiente_pago=datetime.strptime(data["siguiente_pago"], '%Y-%m-%d')
    )
    
    db.session.add(nuevo_pago)
    db.session.commit()
    
    return jsonify({"message": "Pago recurrente agregado correctamente."}), 201
