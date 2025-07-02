from flask import Blueprint, request, jsonify
from Modelos import Categoria, User
from sqlalchemy.exc import SQLAlchemyError
from db import db
from utils import token_required

category_bp = Blueprint('categoria', __name__)

@category_bp.route('/getCategorias', methods=['GET'])
@token_required
def getCategorias(decoded):
    try:
        user_id = decoded.get('user_id')

        if not user_id:
            return jsonify({'message': 'Usuario no válido', 'status': 'error'}), 403

        # Obtener categorías globales y únicas del usuario
        categorias_globales = Categoria.query.filter_by(user_id=None).all()
        categorias_unicas = Categoria.query.filter_by(user_id=user_id, es_global=False).all()

        return jsonify({
            'categoriasGlobales': [categoria.to_dict() for categoria in categorias_globales],
            'categoriasUnicas': [categoria.to_dict() for categoria in categorias_unicas]
        }), 200

    except SQLAlchemyError as e:
        return jsonify({'message': 'Error al obtener categorías', 'status': 'error', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Error en el servidor', 'status': 'error', 'error': str(e)}), 500

@category_bp.route('/getCategoriasUnicas', methods=['GET'])
@token_required
def get_categorias_unicas(decoded):
    try:
        user_id = decoded.get('user_id')

        if not user_id:
            return jsonify({'message': 'Usuario no válido', 'status': 'error'}), 403

        # Obtener las categorías únicas del usuario
        categorias_unicas = Categoria.query.filter_by(user_id=user_id).all()

        return jsonify({
            'categoriasUnicas': [categoria.to_dict() for categoria in categorias_unicas]
        }), 200

    except SQLAlchemyError as e:
        return jsonify({'message': 'Error al obtener categorías únicas', 'status': 'error', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Error interno del servidor', 'status': 'error', 'error': str(e)}), 500

@category_bp.route('/deleteCategoria/<int:categoriaId>', methods=['DELETE'])
@token_required
def delete_categoria(decoded, categoriaId):
    try:
        user_id = decoded.get('user_id')

        # Buscar la categoría y verificar que pertenece al usuario
        categoria = Categoria.query.filter_by(id=categoriaId, user_id=user_id).first()

        if not categoria:
            return jsonify({"message": "Categoría no encontrada o no pertenece al usuario", "status": "error"}), 404

        # Eliminar la categoría
        db.session.delete(categoria)
        db.session.commit()

        return jsonify({"message": "Categoría eliminada exitosamente", "status": "success"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Revertir cambios si ocurre un error
        return jsonify({"message": "Error al eliminar la categoría", "status": "error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Error interno del servidor", "status": "error", "error": str(e)}), 500

@category_bp.route('/setCategoria', methods=['POST'])
@token_required
def set_categoria(decoded):
    try:
        data = request.get_json()

        # Validar que los datos requeridos estén presentes
        if not data or 'nombre' not in data or 'es_global' not in data:
            return jsonify({"message": "Datos incompletos", "status": "error"}), 400

        user_id = decoded.get('user_id')
        nombre_categoria = data['nombre'].strip()
        es_global = bool(data['es_global'])  # Convertir a booleano

        # Verificar si la categoría ya existe para evitar duplicados
        if Categoria.query.filter_by(nombre=nombre_categoria, user_id=user_id, es_global=es_global).first():
            return jsonify({"message": "La categoría ya existe", "status": "error"}), 409

        # Crear nueva categoría
        nueva_categoria = Categoria(nombre=nombre_categoria, user_id=user_id, es_global=es_global)
        db.session.add(nueva_categoria)
        db.session.commit()

        return jsonify({
            "message": "Categoría creada exitosamente",
            "status": "success",
            "categoria_id": nueva_categoria.id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()  # Revertir cambios en caso de error
        return jsonify({"message": "Error al crear la categoría", "status": "error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Error interno del servidor", "status": "error", "error": str(e)}), 500