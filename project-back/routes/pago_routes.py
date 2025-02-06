from flask import Blueprint, request, jsonify
from utils import token_required
from db import db
from Modelos import Categoria, PagoRecurrente
from datetime import datetime
from scheduler import procesar_pagos_recurrentes

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/agregarPagoRecurrente', methods=['POST'])
@token_required
def agregar_pago_recurrente(decoded):
    data = request.json
    nuevo_pago = PagoRecurrente(
        user_id=decoded['user_id'],
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

@pago_bp.route('/getPagosRecurrentes', methods=['GET'])
@token_required
def getPagosRecurrentes(decoded):
    userId = decoded['user_id']

    pagos = db.session.query(
        PagoRecurrente.id,
        PagoRecurrente.user_id,
        PagoRecurrente.concepto,
        PagoRecurrente.tipo,
        PagoRecurrente.frecuencia,
        PagoRecurrente.siguiente_pago,
        PagoRecurrente.estado,
        Categoria.nombre.label("categoria")
    ).join(
        Categoria, Categoria.id == PagoRecurrente.categoria_id
    ).filter(
        PagoRecurrente.user_id == userId
    ).all()

    pagos_data = []
    for pago in pagos:
        pagos_data.append({
            'id': pago.id,
            'user_id': pago.user_id,
            'concepto': pago.concepto,
            'tipo': pago.tipo,
            'frecuencia': pago.frecuencia,
            'siguiente_pago': pago.siguiente_pago,
            'estado': pago.estado,
            'categoria': pago.categoria
        })
    # Retornar los registros en formato JSON
    return {'pagos': pagos_data}, 200

@pago_bp.route('/forzar-pagos', methods=['GET'])
@token_required
def forzar_pagos(decoded):
    procesar_pagos_recurrentes()  # Llamamos manualmente la función
    return jsonify({"message": "Pagos recurrentes procesados manualmente"}), 200
