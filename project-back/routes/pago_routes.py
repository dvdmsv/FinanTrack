from flask import Blueprint, request, jsonify
from utils import token_required
from db import db
from Modelos import Categoria, PagoRecurrente
from datetime import datetime
from scheduler import procesar_pagos_recurrentes
from sqlalchemy.exc import SQLAlchemyError

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/agregarPagoRecurrente', methods=['POST'])
@token_required
def agregar_pago_recurrente(decoded):
    try:
        data = request.get_json()

        # Validar que los datos requeridos estén presentes
        required_fields = ["categoria", "cantidad", "concepto", "tipo", "frecuencia", "intervalo", "fecha"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Datos incompletos", "status": "error"}), 400

        user_id = decoded['user_id']
        categoria_nombre = data["categoria"].strip()

        # Buscar la categoría correspondiente (ya sea global o personalizada)
        categoria = Categoria.query.filter(
            (Categoria.nombre == categoria_nombre) & 
            ((Categoria.es_global == True) | (Categoria.user_id == user_id))
        ).first()

        if not categoria:
            return jsonify({"message": "Categoría no encontrada", "status": "error"}), 404

        # Validar y convertir la fecha
        try:
            fecha_pago = datetime.strptime(data["fecha"], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Formato de fecha inválido. Use 'YYYY-MM-DD'", "status": "error"}), 400

        # Crear nuevo pago recurrente
        nuevo_pago = PagoRecurrente(
            user_id=user_id,
            categoria_id=categoria.id,
            cantidad=data["cantidad"],
            concepto=data["concepto"],
            tipo=data["tipo"],
            frecuencia=data["frecuencia"],
            intervalo=data["intervalo"],
            siguiente_pago=fecha_pago
        )

        db.session.add(nuevo_pago)
        db.session.commit()

        return jsonify({
            "message": "Pago recurrente agregado correctamente.",
            "status": "success",
            "pago_id": nuevo_pago.id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()  # Revertir cambios en caso de error en la BD
        return jsonify({"message": "Error al agregar el pago recurrente", "status": "error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Error interno del servidor", "status": "error", "error": str(e)}), 500

@pago_bp.route('/getPagosRecurrentes', methods=['GET'])
@token_required
def getPagosRecurrentes(decoded):
    try:
        user_id = decoded['user_id']

        # Obtener pagos recurrentes con la categoría asociada
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
            PagoRecurrente.user_id == user_id
        ).all()

        # Convertir los pagos en una lista de diccionarios
        pagos_data = [
            {
                'id': pago.id,
                'user_id': pago.user_id,
                'concepto': pago.concepto,
                'tipo': pago.tipo,
                'frecuencia': pago.frecuencia,
                'intervalo': pago.intervalo,
                'siguiente_pago': pago.siguiente_pago.strftime('%d-%m-%Y'),
                'estado': pago.estado,
                'categoria': pago.categoria,
                'cantidad': pago.cantidad
            }
            for pago in pagos
        ]

        return jsonify({
            "status": "success",
            "message": "Pagos recurrentes obtenidos correctamente.",
            "pagos": pagos_data
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "status": "error",
            "message": "Error al obtener los pagos recurrentes.",
            "error": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error interno del servidor.",
            "error": str(e)
        }), 500

@pago_bp.route('/getPagoRecurrente/<int:pagoRecurrenteId>', methods=['GET'])
@token_required
def getPagoRecurrente(decoded, pagoRecurrenteId):
    try:
        userId = decoded['user_id']

        # Consultar solo los campos necesarios usando with_entities()
        pago_recurrente = db.session.query(
            PagoRecurrente.id,
            PagoRecurrente.concepto,
            PagoRecurrente.tipo,
            PagoRecurrente.frecuencia,
            PagoRecurrente.intervalo,
            PagoRecurrente.siguiente_pago,
            PagoRecurrente.estado,
            PagoRecurrente.cantidad,
            Categoria.nombre.label("categoria")
        ).join(
            Categoria, Categoria.id == PagoRecurrente.categoria_id
        ).filter(
            PagoRecurrente.id == pagoRecurrenteId,
            PagoRecurrente.user_id == userId
        ).first()

        # Validar si el pago existe
        if not pago_recurrente:
            return jsonify({'error': 'Pago recurrente no encontrado'}), 404

        # Construir la respuesta JSON
        return jsonify({
            'id': pago_recurrente.id,
            'concepto': pago_recurrente.concepto,
            'tipo': pago_recurrente.tipo,
            'frecuencia': pago_recurrente.frecuencia,
            'intervalo': pago_recurrente.intervalo,
            'siguiente_pago': pago_recurrente.siguiente_pago.strftime('%Y-%m-%d'),
            'estado': pago_recurrente.estado,
            'categoria': pago_recurrente.categoria,
            'cantidad': pago_recurrente.cantidad
        }), 200

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Error al obtener el pago recurrente.",
            "message": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor.",
            "message": str(e)
        }), 500


@pago_bp.route('/updatePagoRecurrente', methods=['POST'])
@token_required
def updatePagoRecurrente(decoded):
    try:
        userId = decoded['user_id']
        data = request.json

        pagoRecurrenteId = data.get('id')
        if not pagoRecurrenteId:
            return jsonify({'error': 'ID del pago recurrente es requerido'}), 400

        # Buscar el pago recurrente
        pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()
        if not pago_recurrente:
            return jsonify({'error': 'Pago recurrente no encontrado'}), 404

        # Buscar la categoría solo si se proporciona
        categoria_nombre = data.get('categoria')
        if categoria_nombre:
            categoria = Categoria.query.filter(
                (Categoria.nombre == categoria_nombre) & 
                ((Categoria.es_global == True) | (Categoria.user_id == userId))
            ).first()
            if not categoria:
                return jsonify({'error': 'Categoría no encontrada'}), 404
            pago_recurrente.categoria_id = categoria.id
        else:
            categoria = Categoria.query.get(pago_recurrente.categoria_id)

        # Actualizar los valores solo si se proporcionan en la petición
        pago_recurrente.cantidad = data.get('cantidad', pago_recurrente.cantidad)
        pago_recurrente.concepto = data.get('concepto', pago_recurrente.concepto)
        pago_recurrente.tipo = data.get('tipo', pago_recurrente.tipo)
        pago_recurrente.frecuencia = data.get('frecuencia', pago_recurrente.frecuencia)
        pago_recurrente.intervalo = data.get('intervalo', pago_recurrente.intervalo)
        pago_recurrente.estado = data.get('estado', pago_recurrente.estado)

        # Convertir la fecha solo si se proporciona
        siguiente_pago = data.get('siguiente_pago')
        if siguiente_pago:
            try:
                pago_recurrente.siguiente_pago = datetime.strptime(siguiente_pago, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido, use YYYY-MM-DD'}), 400

        # Guardar cambios
        db.session.commit()

        return jsonify({
            'id': pago_recurrente.id,
            'concepto': pago_recurrente.concepto,
            'tipo': pago_recurrente.tipo,
            'frecuencia': pago_recurrente.frecuencia,
            'intervalo': pago_recurrente.intervalo,
            'siguiente_pago': pago_recurrente.siguiente_pago.strftime('%Y-%m-%d'),
            'estado': pago_recurrente.estado,
            'categoria': categoria.nombre,
            'cantidad': pago_recurrente.cantidad
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error en la base de datos', 'message': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Error interno del servidor', 'message': str(e)}), 500

@pago_bp.route('/modificarEstadoPagoRecurrente', methods=['PATCH'])
@token_required
def modificarEstadoPagoRecurrente(decoded):
    try:
        userId = decoded['user_id']
        data = request.json

        # Validar datos de entrada
        pagoRecurrenteId = data.get('pagoRecurrenteId')
        estado = data.get('estado')

        if pagoRecurrenteId is None or estado is None:
            return jsonify({"error": "pagoRecurrenteId y estado son requeridos"}), 400

        # Buscar el pago recurrente
        pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()

        if not pago_recurrente:
            return jsonify({"error": "Pago recurrente no encontrado"}), 404

        # Actualizar estado
        pago_recurrente.estado = estado
        db.session.commit()

        return jsonify({"message": "Pago recurrente actualizado exitosamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500


@pago_bp.route('/eliminarPagoRecurrente/<int:pagoRecurrenteId>', methods=['DELETE'])
@token_required
def eliminarPagoRecurrente(decoded, pagoRecurrenteId):
    try:
        userId = decoded['user_id']

        # Buscar el pago recurrente
        pago_recurrente = PagoRecurrente.query.filter_by(id=pagoRecurrenteId, user_id=userId).first()

        if not pago_recurrente:
            return jsonify({"error": "Pago recurrente no encontrado"}), 404

        # Eliminar el pago recurrente
        db.session.delete(pago_recurrente)
        db.session.commit()

        return jsonify({"message": "Pago recurrente eliminado exitosamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500

@pago_bp.route('/forzar-pagos', methods=['GET'])
@token_required
def forzar_pagos(decoded):
    procesar_pagos_recurrentes()  # Llamamos manualmente la función
    return jsonify({"message": "Pagos recurrentes procesados manualmente"}), 200
