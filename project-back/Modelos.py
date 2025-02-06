import datetime
from db import db

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0.0)

    # Relación con categorías
    categorias = db.relationship('Categoria', backref='users_categorias', lazy=True)

    # Relación con presupuestos
    presupuestos = db.relationship('Presupuesto', backref='users_presupuestos', lazy=True)

    # Relación con registros
    registros = db.relationship('Registro', backref='users_registros', lazy=True)

# Modelo de Categoría
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL para categorías globales
    es_global = db.Column(db.Boolean, default=False, nullable=False)  # True si es global, False si es personalizada

    # Relación con presupuestos
    presupuestos = db.relationship('Presupuesto', backref='categorias_presupuestos', lazy=True)

    # Relación con registros
    registros = db.relationship('Registro', backref='categorias_registros', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,                     # ID de la categoría
            'nombre': self.nombre,             # Nombre de la categoría
            'es_global': self.es_global,       # Indicador si es global
            'user_id': self.user_id            # ID del usuario propietario (None si es global)
        }

# Modelo de Presupuesto
class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)  # Porcentaje asignado
    presupuesto_inicial = db.Column(db.Float, nullable=False)  # Presupuesto asignado inicialmente
    presupuesto_restante = db.Column(db.Float, nullable=False)  # Presupuesto que queda

    # Relación con el usuario
    user = db.relationship('User', backref='presupuestos_users', lazy=True)

    # Relación con la categoría
    categoria = db.relationship('Categoria', backref='presupuestos_categorias', lazy=True)

# Modelo de Registro
class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)  # Positivo para ingresos, negativo para gastos
    concepto = db.Column(db.String(255), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # 'Ingreso' o 'Gasto'
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relación con el usuario
    user = db.relationship('User', backref='registros_users', lazy=True)

    # Relación con la categoría
    categoria = db.relationship('Categoria', backref='registros_categorias', lazy=True)

# Modelo de pagos recurrentes
class PagoRecurrente(db.Model):
    __tablename__ = 'pagosrecurrentes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)  # Monto del pago recurrente
    concepto = db.Column(db.String(255), nullable=False)  # Descripción del pago
    tipo = db.Column(db.String(50), nullable=False)  # 'Ingreso' o 'Gasto'
    frecuencia = db.Column(db.String(20), nullable=False)  # 'diario', 'semanal', 'mensual', 'anual'
    siguiente_pago = db.Column(db.DateTime, nullable=False)  # Fecha del próximo pago automático

    user = db.relationship('User', backref='pagos_recurrentes_users', lazy=True)
    categoria = db.relationship('Categoria', backref='pagos_recurrentes_categorias', lazy=True)

