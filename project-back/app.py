from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from scheduler import scheduler
from db import db
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.presupuesto_routes import presupuesto_bp
from routes.registro_routes import registro_bp
from routes.saldo_routes import saldo_bp
from routes.user_routes import user_bp
from routes.pdf_routes import pdf_bp
from routes.pago_routes import pago_bp
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
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(pdf_bp, url_prefix='/pdf')
app.register_blueprint(pago_bp, url_prefix='/pago')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.info("Logger configurado correctamente")

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight check passed'}), 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=5000)