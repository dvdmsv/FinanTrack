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
    categoria_nombre = data.get('categoria')

    # Buscar la categoría correspondiente (ya sea global o personalizada)
    categoria = Categoria.query.filter(
        (Categoria.nombre == categoria_nombre) & 
        ((Categoria.es_global == True) | (Categoria.user_id == decoded['user_id']))
    ).first()
    
    nuevo_pago = PagoRecurrente(
        user_id=decoded['user_id'],
        categoria_id=categoria.id,
        cantidad=data["cantidad"],
        concepto=data["concepto"],
        tipo=data["tipo"],
        frecuencia=data["frecuencia"],
        intervalo=data["intervalo"],
        siguiente_pago=datetime.strptime(data["fecha"], '%Y-%m-%d')
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
        PagoRecurrente.intervalo,
        PagoRecurrente.siguiente_pago,
        PagoRecurrente.cantidad,
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
            'intervalo': pago.intervalo,
            'siguiente_pago': pago.siguiente_pago.strftime('%d-%m-%Y %H:%M'),
            'estado': pago.estado,
            'categoria': pago.categoria,
            'cantidad': pago.cantidad
        })
    # Retornar los registros en formato JSON
    return {'pagos': pagos_data}, 200

@pago_bp.route('/getPagoRecurrente/<int:pagoRecurrenteId>', methods=['GET'])
@token_required
def getPagoRecurrente(decoded, pagoRecurrenteId):
    userId = decoded['user_id']

    # Buscar el pago recurrente del usuario
    pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()

    if not pago_recurrente:
        return jsonify({'error': 'Pago recurrente no encontrado'}), 404

    # Obtener la categoría asociada
    categoria = Categoria.query.filter_by(id=pago_recurrente.categoria_id).first()
    categoria_nombre = categoria.nombre if categoria else 'Sin categoría'

    return jsonify({
        'id': pago_recurrente.id,
        'concepto': pago_recurrente.concepto,
        'tipo': pago_recurrente.tipo,
        'frecuencia': pago_recurrente.frecuencia,
        'intervalo': pago_recurrente.intervalo,
        'siguiente_pago': pago_recurrente.siguiente_pago.strftime('%Y-%m-%d'),
        'estado': pago_recurrente.estado,
        'categoria': categoria_nombre,
        'cantidad': pago_recurrente.cantidad
    }), 200


@pago_bp.route('/updatePagoRecurrente', methods=['POST'])
@token_required
def updatePagoRecurrente(decoded):
    userId = decoded['user_id']
    data = request.json

    pagoRecurrenteId=data['id']
    categoria_nombre=data['categoria']
    cantidad=data["cantidad"]
    concepto=data["concepto"]
    tipo=data["tipo"]
    frecuencia=data["frecuencia"]
    intervalo=data["intervalo"]
    siguiente_pago=datetime.strptime(data["siguiente_pago"], '%Y-%m-%d')
    estado=data["estado"]


    pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()

    if pago_recurrente:
        if categoria_nombre:
            # Buscar la categoría correspondiente (ya sea global o personalizada)
            categoria = Categoria.query.filter(
                (Categoria.nombre == categoria_nombre) & 
                ((Categoria.es_global == True) | (Categoria.user_id == decoded['user_id']))
            ).first()
            pago_recurrente.categoria_id = categoria.id
        if cantidad:
            pago_recurrente.cantidad = cantidad
        if concepto:
            pago_recurrente.concepto = concepto
        if tipo:
            pago_recurrente.tipo = tipo
        if frecuencia:
            pago_recurrente.frecuencia = frecuencia
        if intervalo:
            pago_recurrente.intervalo = intervalo
        if siguiente_pago:
            pago_recurrente.siguiente_pago = siguiente_pago
        if estado:
            pago_recurrente.estado = estado
        db.session.commit()

    return jsonify({
        'id': pago_recurrente.id,
        'concepto': pago_recurrente.concepto,
        'tipo': pago_recurrente.tipo,
        'frecuencia': pago_recurrente.frecuencia,
        'intervalo': pago_recurrente.intervalo,
        'siguiente_pago': pago_recurrente.siguiente_pago.strftime('%d-%m-%Y %H:%M'),
        'estado': pago_recurrente.estado,
        'categoria': categoria.nombre,
        'cantidad': pago_recurrente.cantidad
        }), 200

@pago_bp.route('/modificarEstadoPagoRecurrente', methods=['PATCH'])
@token_required
def modificarEstadoPagoRecurrente(decoded):
    userId = decoded['user_id']
    data = request.json
    pagoRecurrenteId = data['pagoRecurrenteId']
    estado = data['estado']

    # Buscar el pago recurrente
    pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()
    
    if pago_recurrente:
        pago_recurrente.estado = estado
        db.session.commit()
        return jsonify({"message": "Pago recurrente actualizado exitosamente"}), 200
    
    return jsonify({"error": "Pago recurrente no encontrado"}), 404


@pago_bp.route('/eliminarPagoRecurrente/<int:pagoRecurrenteId>', methods=['DELETE'])
@token_required
def eliminarPagoRecurrente(decoded, pagoRecurrenteId):
    userId = decoded['user_id']

    pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()

    if pago_recurrente:
        db.session.delete(pago_recurrente)
        db.session.commit()
        return jsonify({"message": "Pago recurrente eliminado exitosamente"}), 200

@pago_bp.route('/forzar-pagos', methods=['GET'])
@token_required
def forzar_pagos(decoded):
    procesar_pagos_recurrentes()  # Llamamos manualmente la función
    return jsonify({"message": "Pagos recurrentes procesados manualmente"}), 200
