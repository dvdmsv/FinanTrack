from flask import Blueprint, request, jsonify
from Modelos import Categoria, Presupuesto, User, Registro
from db import db
from sqlalchemy import distinct, func, text, extract
import datetime
from utils import token_required

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/generarRegistro', methods=['POST'])
@token_required
def generarRegistro(decoded):
    data = request.json
    userId = decoded['user_id']

    # Obtener y validar los datos
    categoria_nombre = data.get('categoria')
    cantidad = data.get('cantidad')
    concepto = data.get('concepto')
    tipo = data.get('tipo')
    fecha = data.get('fecha')

    if not all([categoria_nombre, cantidad, concepto, tipo, fecha]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if tipo not in ['Gasto', 'Ingreso']:
        return jsonify({'error': 'Tipo de registro inválido (debe ser "Gasto" o "Ingreso")'}), 400

    if cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400

    # Buscar la categoría (global o personalizada)
    categoria = Categoria.query.filter(
        (Categoria.nombre == categoria_nombre) & 
        ((Categoria.es_global == True) | (Categoria.user_id == userId))
    ).first()

    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    # Buscar el presupuesto del usuario para esa categoría (si existe)
    presupuesto = Presupuesto.query.filter_by(user_id=userId, categoria_id=categoria.id).first()

    if presupuesto:
        # Inicializar el presupuesto restante si es None
        if presupuesto.presupuesto_restante is None:
            presupuesto.presupuesto_restante = presupuesto.presupuesto_inicial

        # Validar si el gasto supera el presupuesto restante
        if tipo == "Gasto" and cantidad > presupuesto.presupuesto_restante:
            return jsonify({'error': 'La cantidad excede el presupuesto disponible'}), 400

        # Actualizar el presupuesto restante si es un gasto
        if tipo == "Gasto":
            presupuesto.presupuesto_restante -= cantidad

    # Crear el registro de gasto o ingreso
    registro = Registro(
        user_id=userId,
        categoria_id=categoria.id,
        cantidad=cantidad,
        concepto=concepto,
        tipo=tipo,
        fecha=fecha
    )

    try:
        # Obtener y actualizar el saldo del usuario
        user = User.query.get(userId)
        if tipo == 'Gasto':
            user.saldo -= cantidad
        elif tipo == 'Ingreso':
            user.saldo += cantidad

        # Guardar en la base de datos
        db.session.add(registro)
        db.session.commit()

        return jsonify({
            'message': 'Registro creado exitosamente',
            'registro': {
                'id': registro.id,
                'categoria': categoria.nombre,
                'cantidad': registro.cantidad,
                'fecha': registro.fecha,
                'concepto': registro.concepto,
                'tipo': registro.tipo
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
    userId = decoded['user_id']
    
    try:
        # Obtener registros del usuario con JOIN a la categoría
        registros = db.session.query(
            Registro.id,
            Registro.cantidad,
            Registro.concepto,
            Registro.tipo,
            Registro.fecha,
            Categoria.nombre.label('categoria')
        ).join(
            Categoria, Categoria.id == Registro.categoria_id
        ).filter(
            Registro.user_id == userId
        ).order_by(
            Registro.fecha.desc()
        ).all()

        # Si no hay registros, retornar mensaje claro
        if not registros:
            return jsonify({'message': 'No hay registros para este usuario'}), 404

        # Convertir los registros a formato JSON
        registros_data = [{
            'id': reg.id,
            'cantidad': reg.cantidad,
            'concepto': reg.concepto,
            'tipo': reg.tipo,
            'fecha': reg.fecha.strftime('%d-%m-%Y'),
            'categoria': reg.categoria
        } for reg in registros]

        return jsonify({'registros': registros_data}), 200
    
    except Exception as e:
        return jsonify({'error': f'Error al obtener registros: {str(e)}'}), 500


@registro_bp.route('/deleteRegistro/<int:registroId>', methods=['DELETE'])
@token_required
def deleteRegistro(decoded, registroId):
    userId = decoded['user_id']

    try:
        # Verificar si el registro existe
        registro_existente = Registro.query.filter_by(user_id=userId, id=registroId).first()
        if not registro_existente:
            return jsonify({"message": "Registro no encontrado"}), 404

        # Obtener el usuario directamente
        user = User.query.get(userId)
        
        # Ajustar el saldo del usuario según el tipo de registro
        if registro_existente.tipo == 'Ingreso':
            user.saldo -= registro_existente.cantidad
        elif registro_existente.tipo == 'Gasto':
            user.saldo += registro_existente.cantidad

        # Buscar el presupuesto asociado a la categoría (si existe)
        presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, categoria_id=registro_existente.categoria_id).first()
        
        # Si el registro tiene un presupuesto, sumar la cantidad eliminada al presupuesto restante
        if presupuesto_existente:
            presupuesto_existente.presupuesto_restante += registro_existente.cantidad

        # Eliminar el registro
        db.session.delete(registro_existente)
        db.session.commit()

        return jsonify({
            "message": "Registro eliminado exitosamente",
            "nuevo_saldo": user.saldo,
            "presupuesto_restante": presupuesto_existente.presupuesto_restante if presupuesto_existente else None
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el registro: {str(e)}"}), 500


@registro_bp.route('/getRegistrosPorCategoria2/<int:anio>/<int:mes>', methods=['GET'])
@token_required
def registros_por_categoria2(decoded, anio, mes):
    user_id = decoded['user_id']

    try:
        # Sentencia SQL optimizada
        sql = text("""
            SELECT 
                r.categoria_id, 
                c.nombre AS categoria,  
                COALESCE(SUM(r.cantidad), 0) AS total_cantidad, 
                p.porcentaje, 
                p.presupuesto_inicial, 
                p.presupuesto_restante
            FROM 
                registros r
            JOIN 
                categorias c ON r.categoria_id = c.id  
            LEFT JOIN 
                presupuestos p ON r.categoria_id = p.categoria_id AND r.user_id = p.user_id
            WHERE 
                r.user_id = :user_id AND r.tipo = 'Gasto'
                AND (:anio = 0 OR EXTRACT(YEAR FROM r.fecha) = :anio)  
                AND (:mes = 0 OR EXTRACT(MONTH FROM r.fecha) = :mes)  
            GROUP BY 
                r.categoria_id, c.nombre, p.porcentaje, p.presupuesto_inicial, p.presupuesto_restante
            ORDER BY 
                total_cantidad DESC;
        """)

        # Ejecutar la consulta con parámetros seguros
        results = db.session.execute(sql, {'user_id': user_id, 'anio': anio, 'mes': mes}).fetchall()

        # Construcción eficiente del JSON
        response = {
            "categorias": [
                {
                    "categoria": row.categoria,
                    "total_cantidad": float(row.total_cantidad),  # Asegura formato JSON válido
                    "presupuesto": {
                        "porcentaje": row.porcentaje,
                        "presupuesto_inicial": float(row.presupuesto_inicial) if row.presupuesto_inicial else None,
                        "presupuesto_restante": float(row.presupuesto_restante) if row.presupuesto_restante else None
                    } if row.porcentaje is not None else None
                } for row in results
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al obtener registros: {str(e)}"}), 500


@registro_bp.route('/getRegistrosPorCategoria', methods=['GET'])
@token_required
def registros_por_categoria(decoded):
    user_id = decoded['user_id']

    try:
        # Consulta SQL optimizada
        sql = text("""
            SELECT 
                r.categoria_id, 
                c.nombre AS categoria,  
                COALESCE(SUM(r.cantidad), 0) AS total_cantidad, 
                p.porcentaje, 
                p.presupuesto_inicial, 
                p.presupuesto_restante
            FROM 
                registros r
            JOIN 
                categorias c ON r.categoria_id = c.id  
            LEFT JOIN 
                presupuestos p ON r.categoria_id = p.categoria_id AND r.user_id = p.user_id
            WHERE 
                r.user_id = :user_id AND r.tipo = 'Gasto'
            GROUP BY 
                r.categoria_id, c.nombre, p.porcentaje, p.presupuesto_inicial, p.presupuesto_restante
            ORDER BY 
                total_cantidad DESC;
        """)

        # Ejecutar la consulta
        results = db.session.execute(sql, {'user_id': user_id}).fetchall()

        # Construcción eficiente del JSON
        response = {
            "categorias": [
                {
                    "categoria": row.categoria,
                    "total_cantidad": float(row.total_cantidad),  # Asegura formato JSON válido
                    "presupuesto": {
                        "porcentaje": row.porcentaje,
                        "presupuesto_inicial": float(row.presupuesto_inicial) if row.presupuesto_inicial else None,
                        "presupuesto_restante": float(row.presupuesto_restante) if row.presupuesto_restante else None
                    } if row.porcentaje is not None else None
                } for row in results
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al obtener registros: {str(e)}"}), 500

@registro_bp.route('/filtrarRegistros/<int:anio>/<int:tipo>/<int:mes>', methods=['GET'])
@token_required
def filtrarRegistros(decoded, anio, tipo, mes):
    user_id = decoded['user_id']

    try:
        # Construcción de la consulta con filtros dinámicos
        query = db.session.query(
            Registro.id,
            Registro.cantidad,
            Registro.concepto,
            Registro.tipo,
            Registro.fecha,
            Categoria.nombre.label('categoria')
        ).join(
            Categoria, Categoria.id == Registro.categoria_id
        ).filter(
            Registro.user_id == user_id
        )

        # Aplicar filtros si son distintos de 0
        if anio > 0:
            query = query.filter(extract('year', Registro.fecha) == anio)

        if tipo == 1:  # 1 = Gastos, 2 = Ingresos, 0 = Todos
            query = query.filter(Registro.tipo == 'Gasto')
        elif tipo == 2:
            query = query.filter(Registro.tipo == 'Ingreso')

        if mes > 0:
            query = query.filter(extract('month', Registro.fecha) == mes)

        # Optimización en ordenación por fecha completa
        query = query.order_by(Registro.fecha.desc())

        registros = query.all()

        # Construcción eficiente del JSON
        registros_data = [
            {
                "id": r.id,
                "cantidad": float(r.cantidad),
                "concepto": r.concepto,
                "tipo": r.tipo,
                "fecha": r.fecha.strftime("%d-%m-%Y"),
                "categoria": r.categoria
            }
            for r in registros
        ]

        return jsonify({"registros": registros_data}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al filtrar registros: {str(e)}"}), 500

# Se obtiene una lista de los años en los que hay registros
@registro_bp.route('/getAniosRegistros', methods=['GET'])
@token_required
def getAniosRegistros(decoded):
    user_id = decoded['user_id']

    anios = db.session.query(
        distinct(extract('year', Registro.fecha)).label('anio')
    ).filter(
        Registro.user_id == user_id
    ).order_by('anio').all()

    # Extraer el valor correcto de la tupla
    registros_data = [{'anio': anio[0]} for anio in anios]

    return {'registros': registros_data}, 200

# Se obtiene una lista de los meses en los que hay registros
@registro_bp.route('/getMesesRegistros/<int:anio>', methods=['GET'])
@token_required
def getMesesRegistros(decoded, anio):
    user_id = decoded['user_id']

    # Crear la consulta base con el filtro por usuario
    query = db.session.query(
        distinct(extract('month', Registro.fecha)).label('mes')
    ).filter(
        Registro.user_id == user_id
    )

    # Aplicar el filtro por año, si el parámetro anio es mayor que 0
    if anio > 0:
        query = query.filter(extract('year', Registro.fecha) == anio)

    # Ejecutar la consulta
    meses = query.order_by('mes').all()

    # Extraer el valor correcto de la tupla
    registros_data = [{'mes': mes[0]} for mes in meses]

    return {'registros': registros_data}, 200


@registro_bp.route('/gastos-por-mes', methods=['POST'])
@token_required
def obtener_gastos_por_mes(decoded):
    data = request.json
    user_id = decoded['user_id']
    anio = data['anio']

    gastos_por_mes = (
        db.session.query(
            extract('month', Registro.fecha).label('mes'),
            func.sum(Registro.cantidad).label('total')
        )
        .filter(
            Registro.user_id == user_id,
            extract('year', Registro.fecha) == anio,
            Registro.tipo == 'Gasto'  # Solo filtrar gastos
        )
        .group_by('mes')
        .order_by('mes')
        .all()
    )

    # Convertir resultado a una lista de diccionarios con formato {"mes": mes, "gasto": gasto}
    resultado = {"gastoPorMes": [{"mes": mes, "gasto": total} for mes, total in gastos_por_mes]}

    return jsonify(resultado)


@registro_bp.route('/getRegistro/<int:registroId>', methods=['GET'])
@token_required
def getRegistro(decoded, registroId):
    userId = decoded['user_id']

    # Obtener el registro junto con la categoría en una sola consulta
    registro = db.session.query(
        Registro.id,
        Registro.cantidad,
        Registro.concepto,
        Registro.tipo,
        Registro.fecha,
        Categoria.nombre.label('categoria')
    ).join(Categoria, Categoria.id == Registro.categoria_id
    ).filter(Registro.user_id == userId, Registro.id == registroId
    ).first()

    if not registro:
        return jsonify({"message": "Registro no encontrado"}), 404

    return {
        "id": registro.id,
        "cantidad": registro.cantidad,
        "concepto": registro.concepto,
        "tipo": registro.tipo,
        "fecha": registro.fecha.strftime('%Y-%m-%d'),
        "categoria": registro.categoria
    }, 200


@registro_bp.route('/updateRegistro', methods=['POST'])
@token_required
def updateRegistro(decoded):
    try:
        userId = decoded['user_id']
        data = request.json

        # Validar datos obligatorios
        required_fields = ['id', 'categoria', 'tipo', 'cantidad', 'concepto']
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        registroId = data['id']
        categoria_nombre = data['categoria']
        nuevo_tipo = data['tipo']
        nueva_cantidad = data['cantidad']
        nuevo_concepto = data['concepto']

        # Obtener el usuario
        user = User.query.filter_by(id=userId).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Obtener el registro existente
        registro_existente = Registro.query.filter_by(user_id=userId, id=registroId).first()
        if not registro_existente:
            return jsonify({"message": "Registro no encontrado"}), 404

        # Obtener la categoría en base al nombre
        categoria = Categoria.query.filter(
            (Categoria.nombre == categoria_nombre) & 
            ((Categoria.es_global == True) | (Categoria.user_id == userId))
        ).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada"}), 404

        # Obtener el presupuesto de la categoría anterior (si existe)
        presupuesto_existente = Presupuesto.query.filter_by(user_id=userId, categoria_id=registro_existente.categoria_id).first()

        # Ajustar saldo si el tipo cambia
        if registro_existente.tipo != nuevo_tipo:
            if registro_existente.tipo == 'Ingreso':
                user.saldo -= registro_existente.cantidad
            else:
                user.saldo += registro_existente.cantidad

            if nuevo_tipo == 'Ingreso':
                user.saldo += nueva_cantidad
            else:
                user.saldo -= nueva_cantidad
        else:
            # Si el tipo NO cambia, solo se ajusta la diferencia de cantidad
            diferencia = nueva_cantidad - registro_existente.cantidad
            if registro_existente.tipo == 'Ingreso':
                user.saldo += diferencia
            else:
                user.saldo -= diferencia

        # Ajustar presupuesto si la categoría no cambió
        if presupuesto_existente and registro_existente.categoria_id == categoria.id:
            presupuesto_existente.presupuesto_restante -= (nueva_cantidad - registro_existente.cantidad)

        # Si no hay cambios, evitar actualización innecesaria
        if (registro_existente.categoria_id == categoria.id and
            registro_existente.tipo == nuevo_tipo and
            registro_existente.cantidad == nueva_cantidad and
            registro_existente.concepto == nuevo_concepto):
            return jsonify({"message": "No hay cambios para actualizar"}), 200

        # Actualizar los datos del registro
        registro_existente.categoria_id = categoria.id
        registro_existente.tipo = nuevo_tipo
        registro_existente.cantidad = nueva_cantidad
        registro_existente.concepto = nuevo_concepto

        # Guardar cambios
        db.session.commit()

        return jsonify({"message": "Registro modificado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar el registro: {str(e)}"}), 500