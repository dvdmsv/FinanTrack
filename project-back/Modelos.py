import datetime
from db import db

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0.0)

    # Relaciones
    categorias = db.relationship('Categoria', back_populates='user', lazy=True, cascade="all, delete")
    presupuestos = db.relationship('Presupuesto', back_populates='user', lazy=True, cascade="all, delete")
    registros = db.relationship('Registro', back_populates='user', lazy=True, cascade="all, delete")
    pagos_recurrentes = db.relationship('PagoRecurrente', back_populates='user', lazy=True, cascade="all, delete")

# Modelo de Categoría
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL para categorías globales
    es_global = db.Column(db.Boolean, default=False, nullable=False)  # True si es global, False si es personalizada

    # Relaciones
    user = db.relationship('User', back_populates='categorias')
    presupuestos = db.relationship('Presupuesto', back_populates='categoria', lazy=True, cascade="all, delete")
    registros = db.relationship('Registro', back_populates='categoria', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'es_global': self.es_global,
            'user_id': self.user_id
        }

# Modelo de Presupuesto
class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    presupuesto_inicial = db.Column(db.Float, nullable=False)
    presupuesto_restante = db.Column(db.Float, nullable=False)

    # Relaciones
    user = db.relationship('User', back_populates='presupuestos')
    categoria = db.relationship('Categoria', back_populates='presupuestos')

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

    # Relaciones
    user = db.relationship('User', back_populates='registros')
    categoria = db.relationship('Categoria', back_populates='registros')

# Modelo de Pagos Recurrentes
class PagoRecurrente(db.Model):
    __tablename__ = 'pagos_recurrentes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    frecuencia = db.Column(db.String(20), nullable=False)  # 'diario', 'semanal', 'mensual', 'anual'
    intervalo = db.Column(db.Integer, nullable=False) # Intervalo entre la frecuencia (cada 1 dia/semana/mes/anio, cada 2...)
    siguiente_pago = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    user = db.relationship('User', back_populates='pagos_recurrentes')
    categoria = db.relationship('Categoria', lazy=True)
