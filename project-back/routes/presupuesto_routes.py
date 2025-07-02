from flask import Blueprint, request, jsonify
from Modelos import Categoria, Presupuesto, User
from db import db
from utils import token_required
from sqlalchemy.exc import SQLAlchemyError

presupuesto_bp = Blueprint('presupuesto', __name__)

@presupuesto_bp.route('/deletePresupuesto/<int:presupuestoId>', methods=['DELETE'])
@token_required
def deletePresupuesto(decoded, presupuestoId):
    try:
        userId = decoded['user_id']

        # Verificar si el presupuesto pertenece al usuario
        presupuesto = Presupuesto.query.filter_by(id=presupuestoId, user_id=userId).first()

        if not presupuesto:
            return jsonify({"error": "Presupuesto no encontrado o no pertenece al usuario"}), 404

        # Eliminar presupuesto
        db.session.delete(presupuesto)
        db.session.commit()

        return jsonify({"message": "Presupuesto eliminado exitosamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500


@presupuesto_bp.route('/setPresupuesto', methods=['POST'])
@token_required
def setPresupuesto(decoded):
    try:
        data = request.json
        userId = decoded['user_id']

        # Obtener usuario y validar existencia
        user = User.query.get_or_404(userId, description="Usuario no encontrado")

        # Obtener datos de entrada
        porcentaje = data.get('porcentaje')
        categoria_nombre = data.get('categoria')

        # Validar datos
        if porcentaje is None or not categoria_nombre:
            return jsonify({"error": "Porcentaje y categoría son obligatorios"}), 400

        # Obtener categoría
        categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
        if not categoria:
            return jsonify({"error": "Categoría no encontrada"}), 404

        # Calcular presupuesto inicial
        presupuestoInicial = user.saldo * (porcentaje / 100)

        # Buscar si ya existe un presupuesto para la categoría
        presupuesto = Presupuesto.query.filter_by(user_id=userId, categoria_id=categoria.id).first()

        if presupuesto:
            # Si existe, actualizarlo
            presupuesto.porcentaje = porcentaje
            presupuesto.presupuesto_inicial = presupuestoInicial
            presupuesto.presupuesto_restante = presupuestoInicial
            mensaje = "Presupuesto actualizado exitosamente"
        else:
            # Si no existe, crearlo
            presupuesto = Presupuesto(
                user_id=userId,
                categoria_id=categoria.id,
                porcentaje=porcentaje,
                presupuesto_inicial=presupuestoInicial,
                presupuesto_restante=presupuestoInicial
            )
            db.session.add(presupuesto)
            mensaje = "Presupuesto creado exitosamente"

        db.session.commit()

        return jsonify({
            "message": mensaje,
            "presupuesto": {
                "categoria": categoria.nombre,
                "porcentaje": presupuesto.porcentaje,
                "presupuesto_inicial": presupuesto.presupuesto_inicial,
                "presupuesto_restante": presupuesto.presupuesto_restante
            }
        }), 200 if presupuesto else 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500


@presupuesto_bp.route('/getPresupuestos', methods=['GET'])
@token_required
def getPresupuestos(decoded):
    userId = decoded['user_id']

    # Obtener usuario y validar existencia
    user = User.query.get_or_404(userId, description="Usuario no encontrado")

    # Consultar presupuestos junto con sus categorías
    presupuestos = db.session.query(
        Presupuesto.id,
        Presupuesto.porcentaje,
        Presupuesto.presupuesto_inicial,
        Presupuesto.presupuesto_restante,
        Categoria.nombre.label("categoria")
    ).join(Categoria, Presupuesto.categoria_id == Categoria.id).filter(
        Presupuesto.user_id == userId
    ).all()

    # Formatear la respuesta
    presupuesto_data = [{
        "id": p.id,
        "categoria": p.categoria,
        "porcentaje": p.porcentaje,
        "presupuesto_inicial": p.presupuesto_inicial,
        "presupuesto_restante": p.presupuesto_restante
    } for p in presupuestos]

    return jsonify({"presupuestos": presupuesto_data}), 200


@presupuesto_bp.route('/getPresupuesto', methods=['POST'])
@token_required
def getPresupuesto(decoded):
    userId = decoded['user_id']
    data = request.json

    # Validar que se haya enviado el ID del presupuesto
    presupuestoId = data.get('id')
    if not presupuestoId:
        return jsonify({"error": "El ID del presupuesto es obligatorio"}), 400

    # Buscar el presupuesto y su categoría en una sola consulta
    presupuesto = db.session.query(
        Presupuesto.id,
        Presupuesto.porcentaje,
        Presupuesto.presupuesto_inicial,
        Presupuesto.presupuesto_restante,
        Categoria.nombre.label("categoria")
    ).join(Categoria, Presupuesto.categoria_id == Categoria.id).filter(
        Presupuesto.user_id == userId,
        Presupuesto.id == presupuestoId
    ).first()

    if not presupuesto:
        return jsonify({"error": "Presupuesto no encontrado"}), 404

    # Formatear respuesta
    return jsonify({
        "id": presupuesto.id,
        "categoria": presupuesto.categoria,
        "porcentaje": presupuesto.porcentaje,
        "presupuesto_inicial": presupuesto.presupuesto_inicial,
        "presupuesto_restante": presupuesto.presupuesto_restante
    }), 200

@presupuesto_bp.route('/updatePresupuesto', methods=['POST'])
@token_required
def updatePresupuesto(decoded):
    data = request.json
    userId = decoded['user_id']

    # Validar que los campos requeridos estén en la solicitud
    presupuestoId = data.get('id')
    categoria_nombre = data.get('categoria')
    porcentaje = data.get('porcentaje')

    if not presupuestoId or not categoria_nombre or porcentaje is None:
        return jsonify({"error": "Todos los campos (id, categoria, porcentaje) son obligatorios"}), 400

    # Buscar el presupuesto del usuario
    presupuesto = Presupuesto.query.filter_by(user_id=userId, id=presupuestoId).first()
    if not presupuesto:
        return jsonify({"error": "Presupuesto no encontrado"}), 404

    # Buscar la categoría (ya sea global o del usuario)
    categoria = Categoria.query.filter(
        (Categoria.nombre == categoria_nombre) & 
        ((Categoria.es_global == True) | (Categoria.user_id == userId))
    ).first()

    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    # Actualizar el presupuesto
    presupuesto.categoria_id = categoria.id
    presupuesto.porcentaje = porcentaje

    # Obtener el usuario y calcular el presupuesto inicial
    user = User.query.get(userId)
    presupuesto_inicial = user.saldo * (porcentaje / 100)
    presupuesto.presupuesto_inicial = presupuesto_inicial
    presupuesto.presupuesto_restante = presupuesto_inicial

    # Guardar cambios
    db.session.commit()

    # Formatear la respuesta
    return jsonify({
        'id': presupuesto.id,
        'categoria': categoria.nombre,
        'porcentaje': presupuesto.porcentaje,
        'presupuesto_inicial': presupuesto.presupuesto_inicial,
        'presupuesto_restante': presupuesto.presupuesto_restante
    }), 200