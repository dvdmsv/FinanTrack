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
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.presupuesto_routes import presupuesto_bp
from routes.registro_routes import registro_bp
from routes.saldo_routes import saldo_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app, origins=Config.CORS_ORIGINS, methods=Config.METHODS, allow_headers=Config.HEADERS)

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(category_bp, url_prefix='/categoria')
app.register_blueprint(presupuesto_bp, url_prefix='/presupuesto')
app.register_blueprint(registro_bp, url_prefix='/registro')
app.register_blueprint(saldo_bp, url_prefix='/saldo')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.info("Logger configurado correctamente")

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight check passed'}), 200


# @app.route('/getUser', methods=['GET'])
# @token_required
# def getUser(decoded):
#     userId = decoded['user_id']
#     user = User.query.filter_by(id=userId).first()
#     if user:
#         return jsonify({
#             'message': 'Token is valid',
#             'user': user.username
#         }), 200
#     return jsonify({'message': 'User not found'}), 404

# @app.route('/getUserData', methods=['GET'])
# @token_required
# def getUserData(decoded):
#     return jsonify({
#             'message': 'Token is valid',
#             'user_data': decoded
#         }), 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True, host='0.0.0.0', port=5000)