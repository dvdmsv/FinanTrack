from flask import Blueprint, request, jsonify
from Modelos import Categoria, Presupuesto, User, Registro
from db import db
from sqlalchemy import func, text
import datetime
from utils import token_required

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/generarRegistro', methods=['POST'])
@token_required
def generarRegistro(decoded):
    
    data = request.json
    userId = decoded['user_id']

    categoria_nombre = data.get('categoria')
    cantidad = data.get('cantidad')
    concepto = data.get('concepto')
    tipo = data.get('tipo')

    # Buscar la categoría correspondiente (ya sea global o personalizada)
    categoria = Categoria.query.filter(
        (Categoria.nombre == categoria_nombre) & 
        ((Categoria.es_global == True) | (Categoria.user_id == userId))
    ).first()

    if not categoria:
        return jsonify({'error': 'Categoría no encontrada', 'info': request.json}), 400

    # Buscar el presupuesto del usuario para esa categoría (si existe)
    presupuesto = Presupuesto.query.filter_by(user_id=userId, categoria_id=categoria.id).first()

    # Si existe un presupuesto y el presupuesto restante es None, inicializarlo con el valor de presupuesto_inicial
    if presupuesto:
        if presupuesto.presupuesto_restante is None:
            presupuesto.presupuesto_restante = presupuesto.presupuesto_inicial

        # Verificar que el gasto no exceda el presupuesto restante
        if cantidad > presupuesto.presupuesto_restante:
            return jsonify({'error': 'La cantidad excede el presupuesto disponible'}), 400

        # Actualizar el presupuesto restante
        presupuesto.presupuesto_restante = presupuesto.presupuesto_restante - cantidad

    # Crear el registro de gasto (independientemente de si hay presupuesto o no)
    registro = Registro(
        user_id=userId,
        categoria_id=categoria.id,
        cantidad=cantidad,
        concepto=concepto,
        tipo=tipo,
        fecha=datetime.datetime.now()
    )

    try:
        # Actualizar el saldo del usuario
        user = User.query.filter_by(id=userId).first()
        if tipo == 'Gasto':
            user.saldo = user.saldo - cantidad
        if tipo == 'Ingreso': 
            user.saldo = user.saldo + cantidad
        # Guardar cambios en la base de datos
        db.session.add(registro)
        db.session.commit()

        return jsonify({
            'message': 'Registro creado exitosamente',
            'registro': {
                'id': registro.id,
                'categoria': categoria.nombre,
                'cantidad': registro.cantidad,  
                'fecha': registro.fecha,
                'concepto': registro.concepto
            },
            'nuevo_saldo': user.saldo,
            'presupuesto_restante': presupuesto.presupuesto_restante if presupuesto else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear el registro: {str(e)}'}), 500

@registro_bp.route('/getRegistrosUser', methods=['GET'])
@token_required
def getRegistrosUser(decoded):
    # Obtener el ID del usuario desde el token decodificado
    userId = decoded['user_id']
    
    # Obtener al usuario desde la base de datos
    user = User.query.filter_by(id=userId).first()
    
    # Verificar si el usuario existe
    if not user:
        return {'message': 'Usuario no encontrado'}, 404
    
    # Obtener los registros asociados al usuario
    # registros = Registro.query.filter_by(user_id=userId).all()
    registros = db.session.query(
        Registro.id,
        Registro.cantidad,
        Registro.concepto,
        Registro.tipo,
        Registro.fecha,
        Categoria.nombre.label('categoria')  # Añadimos el nombre de la categoría
    ).join(
        Categoria, Categoria.id == Registro.categoria_id  # Realizamos el JOIN entre Registro y Categoria
    ).filter(
        Registro.user_id == userId # Filtramos por el user_id
    ).all()
        
    # Convertir los registros a un formato que se pueda retornar
    registros_data = []
    for registro in registros:
        registros_data.append({
            'id': registro.id,
            'cantidad': registro.cantidad,
            'concepto': registro.concepto,
            'tipo': registro.tipo,
            'fecha': registro.fecha.strftime('%d-%m-%Y %H:%M'),
            'categoria': registro.categoria
        })
    
    # Retornar los registros en formato JSON
    return {'registros': registros_data}, 200

@registro_bp.route('/deleteRegistro/<int:registroId>', methods=['DELETE'])
@token_required
def deleteRegistro(decoded, registroId):
    userId = decoded['user_id']

    # Obtener el usuario
    user = User.query.filter_by(id=userId).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verificar si ya existe un presupuesto para esa categoría y usuario
    registro_existente = Registro.query.filter_by(user_id=userId, id=registroId).first()
    
    # Buscar el presupuesto del usuario para esa categoría (si existe)
    presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, categoria_id=registro_existente.categoria_id).first()

    if registro_existente:
        # Si el registro que se va a eliminar es un ingreso, se resta del saldo del usuario. Si es un gasto se suma al saldo del usuario
        if registro_existente.tipo == 'Ingreso':
            user.saldo = user.saldo - registro_existente.cantidad
        elif registro_existente.tipo == 'Gasto':
            user.saldo = user.saldo + registro_existente.cantidad

        if presupuesto_existente:
            presupuesto_existente.presupuesto_restante = presupuesto_existente.presupuesto_restante + registro_existente.cantidad

        db.session.delete(registro_existente)
        db.session.commit()
        return jsonify({"message": "Registro eliminado exitosamente"}), 200

    return jsonify({"message": "Registro no encontrado"}), 404

@registro_bp.route('/getRegistrosPorCategoria', methods=['GET'])
@token_required
def registros_por_categoria(decoded):
    user_id = decoded['user_id']

    # # Consulta con JOIN para traer datos de registros y presupuestos
    # results = db.session.query(
    #     Categoria.nombre.label('categoria'),
    #     db.func.sum(Registro.cantidad).label('total_cantidad'),
    #     Presupuesto.porcentaje,
    #     Presupuesto.presupuesto_inicial,
    #     Presupuesto.presupuesto_restante
    # ).join(Registro, Registro.categoria_id == Categoria.id)\
    #  .outerjoin(Presupuesto, Presupuesto.categoria_id == Categoria.id)\
    #  .filter(Registro.user_id == user_id)\
    #  .group_by(
    #      Categoria.nombre,
    #      Presupuesto.porcentaje,
    #      Presupuesto.presupuesto_inicial,
    #      Presupuesto.presupuesto_restante
    #  ).all()

    # Escribir una sentencia SQL literal con text()
    sql = text("""
        SELECT 
            r.user_id,
            r.categoria_id, 
            c.nombre AS categoria,  -- Se añade el nombre de la categoría
            SUM(r.cantidad) AS total_cantidad, 
            p.porcentaje, 
            p.presupuesto_inicial, 
            p.presupuesto_restante
        FROM 
            registros r
        LEFT JOIN 
            presupuestos p  -- Cambiamos a LEFT JOIN para incluir los registros sin presupuesto
        ON 
            r.categoria_id = p.categoria_id
            AND r.user_id = p.user_id  -- Aseguramos que el user_id también coincida en ambas tablas
        JOIN 
            categorias c  -- Se hace un JOIN con la tabla de categorías
        ON 
            r.categoria_id = c.id  -- Relacionamos la categoría con la tabla categorias
        WHERE 
            r.user_id = :user_id AND r.tipo = 'Gasto'
        GROUP BY 
            r.user_id,
            r.categoria_id,
            c.nombre,  -- Añadimos el nombre de la categoría en el GROUP BY
            p.porcentaje, 
            p.presupuesto_inicial, 
            p.presupuesto_restante;
        """)

    # Ejecutar la consulta con el valor de user_id
    results = db.session.execute(sql, {'user_id': user_id}).fetchall()

    # Convertir resultados a JSON
    response = {
        "categorias": []
    }

    for row in results:
        response["categorias"].append({
            "categoria": row.categoria,
            "total_cantidad": row.total_cantidad,
            "presupuesto": {
                "porcentaje": row.porcentaje,
                "presupuesto_inicial": row.presupuesto_inicial,
                "presupuesto_restante": row.presupuesto_restante
            } if row.porcentaje is not None else None
        })

    return jsonify(response), 200