import os
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy import func, text
import logging
import jwt
import datetime
import secrets
from functools import wraps
from Modelos import db, User, Categoria, Registro, Presupuesto  # Importa los modelos y la instancia db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:33060/finanzas'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost:33061/finanzas'

# Configuracion para docker
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#     'DATABASE_URI',
#     'mysql+pymysql://root:root@host.docker.internal:33060/finanzas'
# )
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db con la app
db.init_app(app)

bcrypt = Bcrypt(app)
CORS(app, origins=["http://localhost", "http://localhost:4200"], methods=["GET", "POST", "OPTIONS", "DELETE"], allow_headers=["Content-Type", "Authorization"])

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.info("Logger configurado correctamente")

# Generar una clave secreta segura
SECRET_KEY = secrets.token_urlsafe(64)

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight check passed'}), 200

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Expired token'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 400

        return f(decoded, *args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': 'Login exitoso',
            'userId': user.id,
            'token': token
        }), 200
    return jsonify({'message': 'Credenciales incorrectas', 'status': 'error'}), 401

@app.route('/registro', methods=['POST', 'OPTIONS'])
def registro():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight check passed'}), 200

    data = request.json
    username = data.get('username')
    password = data.get('password')
    saldo = data.get('saldo')

    if not username or not password:
        return jsonify({'messaje': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'messaje': 'Username already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password, saldo=saldo)

    try:
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'messaje': 'User registered successfully',
            'token': token
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 500

@app.route('/setSaldo', methods=['POST'])
@token_required
def setSaldo(decoded):
    data = request.json
    userId = decoded['user_id']
    user = User.query.filter_by(id=userId).first()
    user.saldo = data.get('saldo')
    db.session.commit()
    return jsonify({
        'message': 'Saldo updated',
        'saldo': user.saldo
    }), 200

@app.route('/getSaldo', methods=['GET'])
@token_required
def getSaldo(decoded):
    userId = decoded['user_id']
    user = User.query.filter_by(id=userId).first()
    return jsonify({
        'saldo': user.saldo
    }), 200

@app.route('/getCategorias', methods=['GET'])
@token_required
def getCategorias(decoded):
    userId = decoded['user_id']
    categoriasGlobales = Categoria.query.filter_by(user_id=None).all()
    categoriasUnicas = Categoria.query.filter_by(user_id=userId).all()

    return jsonify({
        'categoriasGlobales': [categoria.to_dict() for categoria in categoriasGlobales],
        'categoriasUnicas': [categoria.to_dict() for categoria in categoriasUnicas]
    }), 200

@app.route('/setCategoria', methods=['POST'])
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

@app.route('/deletePresupuesto/<int:presupuestoId>', methods=['DELETE'])
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


@app.route('/setPresupuesto', methods=['POST'])
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

@app.route('/getPresupuesto', methods=['GET'])
@token_required
def getPresupuesto(decoded):
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
                'presupuesto_restante': presupuesto.presupuesto_inicial
            })
    
    return jsonify({
        'presupuestos': presupuesto_data
    }), 200

@app.route('/generarRegistro', methods=['POST'])
@token_required
def generarRegistro(decoded):
    
    data = request.json
    userId = decoded['user_id']
    app.logger.info(request.json)

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

@app.route('/getRegistrosUser', methods=['GET'])
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
            'cantidad': registro.cantidad,
            'concepto': registro.concepto,
            'tipo': registro.tipo,
            'fecha': registro.fecha.strftime('%d-%m-%Y %H:%M'),
            'categoria': registro.categoria
        })
    
    # Retornar los registros en formato JSON
    return {'registros': registros_data}, 200

@app.route('/getRegistrosPorCategoria', methods=['GET'])
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
            r.user_id = :user_id
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


@app.route('/getUser', methods=['GET'])
@token_required
def getUser(decoded):
    userId = decoded['user_id']
    user = User.query.filter_by(id=userId).first()
    if user:
        return jsonify({
            'message': 'Token is valid',
            'user': user.username
        }), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/getUserData', methods=['GET'])
@token_required
def getUserData(decoded):
    return jsonify({
            'message': 'Token is valid',
            'user_data': decoded
        }), 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True, host='0.0.0.0', port=5000)