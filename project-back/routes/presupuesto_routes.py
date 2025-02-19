from flask import Blueprint, request, jsonify
from Modelos import Categoria, Presupuesto, User
from db import db
from utils import token_required

presupuesto_bp = Blueprint('presupuesto', __name__)

@presupuesto_bp.route('/deletePresupuesto/<int:presupuestoId>', methods=['DELETE'])
@token_required
def deletePresupuesto(decoded, presupuestoId):
    userId = decoded['user_id']

    # Obtener el usuario
    user = User.query.filter_by(id=userId).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verificar si ya existe un presupuesto para esa categoría y usuario
    presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, id=presupuestoId).first()

    if presupuesto_existente:
        db.session.delete(presupuesto_existente)
        db.session.commit()
        return jsonify({"message": "Presupuesto eliminado exitosamente"}), 200

    return jsonify({"message": "Presupuesto no encontrado"}), 404


@presupuesto_bp.route('/setPresupuesto', methods=['POST'])
@token_required
def setPresupuesto(decoded):
    data = request.json
    userId = decoded['user_id']
    
    # Obtener el usuario
    user = User.query.filter_by(id=userId).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Obtener el porcentaje y la categoría
    porcentaje = data.get('porcentaje')
    categoria_nombre = data.get('categoria')
    
    # Validación de porcentaje y categoría
    if not porcentaje or not categoria_nombre:
        return jsonify({"message": "Porcentaje y categoría son obligatorios"}), 400
    
    # Obtener la categoría
    categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
    if not categoria:
        return jsonify({"message": "Categoría no encontrada"}), 404

    # Calcular el presupuesto inicial
    presupuestoInicial = user.saldo * (porcentaje / 100)
    
    # Verificar si ya existe un presupuesto para esa categoría y usuario
    presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, categoria_id=categoria.id).first()
    
    if presupuesto_existente:
        # Si ya existe, actualizarlo
        presupuesto_existente.porcentaje = porcentaje
        presupuesto_existente.presupuesto_inicial = presupuestoInicial
        presupuesto_existente.presupuesto_restante = presupuestoInicial
        db.session.commit()
        return jsonify({"message": "Presupuesto actualizado exitosamente"}), 200
    else:
        # Si no existe, crear uno nuevo
        presupuesto = Presupuesto(user_id=userId, categoria_id=categoria.id, porcentaje=porcentaje, presupuesto_inicial=presupuestoInicial, presupuesto_restante=presupuestoInicial)
        db.session.add(presupuesto)
        db.session.commit()
        return jsonify({"message": "Presupuesto creado exitosamente"}), 201

@presupuesto_bp.route('/getPresupuestos', methods=['GET'])
@token_required
def getPresupuestos(decoded):
    userId = decoded['user_id']
    
    # Obtener el usuario
    user = User.query.filter_by(id=userId).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Obtener los presupuestos del usuario
    presupuestos = Presupuesto.query.filter_by(user_id=userId).all()
    # if not presupuestos:
    #     return jsonify({"message": "No presupuestos found for this user"}), 404
    
    # Crear la respuesta con los presupuestos
    presupuesto_data = []
    for presupuesto in presupuestos:
        categoria = Categoria.query.filter_by(id=presupuesto.categoria_id).first()
        if categoria:
            presupuesto_data.append({
                'id': presupuesto.id,
                'categoria': categoria.nombre,
                'porcentaje': presupuesto.porcentaje,
                'presupuesto_inicial': presupuesto.presupuesto_inicial,
                'presupuesto_restante': presupuesto.presupuesto_restante
            })
    
    return jsonify({
        'presupuestos': presupuesto_data
    }), 200

@presupuesto_bp.route('/getPresupuesto', methods=['POST'])
@token_required
def getPresupuesto(decoded):
    userId = decoded['user_id']
    data = request.json
    presupuestoId = data['id']
    
    # Obtener el presupuesto del usuario en base al id
    presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, id=presupuestoId).first()
    
    categoria = Categoria.query.filter_by(id=presupuesto_existente.categoria_id).first()

    return jsonify({
        'id': presupuesto_existente.id,
        'categoria': categoria.nombre,
        'porcentaje': presupuesto_existente.porcentaje,
        'presupuesto_inicial': presupuesto_existente.presupuesto_inicial,
        'presupuesto_restante': presupuesto_existente.presupuesto_restante
    }), 200

@presupuesto_bp.route('/updatePresupuesto', methods=['POST'])
@token_required
def updatePresupuesto(decoded):
    data = request.json
    presupuestoId = data['id']
    categoria_nombre = data['categoria']
    porcentaje = data['porcentaje']
    userId = decoded['user_id']

    # Obtener el presupuesto
    presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, id=presupuestoId).first()

    if presupuesto_existente:
        if categoria_nombre:
            # Buscar la categoría correspondiente (ya sea global o personalizada)
            categoria = Categoria.query.filter(
                (Categoria.nombre == categoria_nombre) & 
                ((Categoria.es_global == True) | (Categoria.user_id == decoded['user_id']))
            ).first()
            presupuesto_existente.categoria_id = categoria.id
        if porcentaje:
            presupuesto_existente.porcentaje = porcentaje
            # Obtener el usuario
            user = User.query.filter_by(id=userId).first()
            # Calcular el presupuesto inicial
            presupuestoInicial = user.saldo * (porcentaje / 100)
            presupuesto_existente.presupuesto_inicial = presupuestoInicial
            presupuesto_existente.presupuesto_restante = presupuestoInicial
    db.session.commit()
    presupuesto_data = []
    presupuesto_data.append({
        'id': presupuesto_existente.id,
        'categoria': categoria.nombre,
        'porcentaje': presupuesto_existente.porcentaje,
        'presupuesto_inicial': presupuesto_existente.presupuesto_inicial,
        'presupuesto_restante': presupuesto_existente.presupuesto_restante
    })

    return jsonify({
        'presupuestos': presupuesto_data
    }), 200
    