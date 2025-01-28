from flask import Blueprint, request, jsonify
from Modelos import Categoria
from db import db
from utils import token_required

category_bp = Blueprint('categoria', __name__)

@category_bp.route('/getCategorias', methods=['GET'])
@token_required
def getCategorias(decoded):
    userId = decoded['user_id']
    categoriasGlobales = Categoria.query.filter_by(user_id=None).all()
    categoriasUnicas = Categoria.query.filter_by(user_id=userId).all()

    return jsonify({
        'categoriasGlobales': [categoria.to_dict() for categoria in categoriasGlobales],
        'categoriasUnicas': [categoria.to_dict() for categoria in categoriasUnicas]
    }), 200

@category_bp.route('/setCategoria', methods=['POST'])
@token_required
def setCategorias(decoded):
    data = request.json
    userId = decoded['user_id']
    nombreCategoriaNueva = data.get('nombre')
    esGlobal = data.get("es_global")
    categoria = Categoria(nombre=nombreCategoriaNueva, user_id=userId, es_global=esGlobal)

    if Categoria.query.filter_by(nombre=nombreCategoriaNueva).first():
        return jsonify({'messaje': 'Categoria already exists'}), 409
    
    try:
        db.session.add(categoria)
        db.session.commit()
        return jsonify({"message": "Categoria created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating categoria: {str(e)}"}), 500