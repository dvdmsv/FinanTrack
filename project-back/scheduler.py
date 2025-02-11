from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from db import db
from Modelos import Registro, PagoRecurrente, User

def procesar_pagos_recurrentes():
    """Función que ejecuta los pagos recurrentes automáticamente."""
    from app import app  # Importación dentro de la función para evitar el import circular

    with app.app_context():
        hoy = datetime.now()
        pagos = PagoRecurrente.query.filter(PagoRecurrente.siguiente_pago <= hoy).all()

        for pago in pagos:
            nuevo_registro = Registro(
                user_id=pago.user_id,
                categoria_id=pago.categoria_id,
                cantidad=pago.cantidad,
                concepto=pago.concepto,
                tipo=pago.tipo,
                fecha=hoy
            )

            # Actualizar saldo del usuario
            user = User.query.get(pago.user_id)
            if user:
                if pago.tipo == 'Gasto':
                    user.saldo -= pago.cantidad
                elif pago.tipo == 'Ingreso':
                    user.saldo += pago.cantidad

                db.session.add(nuevo_registro)
                db.session.commit()

                # Actualizar la fecha del siguiente pago
                if pago.frecuencia == "Diario":
                    pago.siguiente_pago += timedelta(days=1)
                elif pago.frecuencia == "Semanal":
                    pago.siguiente_pago += timedelta(weeks=1)
                elif pago.frecuencia == "Mensual":
                    pago.siguiente_pago += timedelta(days=30)
                elif pago.frecuencia == "Anual":
                    pago.siguiente_pago += timedelta(days=365)

                db.session.commit()

        print(f"Pagos recurrentes procesados: {len(pagos)}")

# Se define el scheduler, pero NO se inicia aquí
scheduler = BackgroundScheduler()
scheduler.add_job(procesar_pagos_recurrentes, 'interval', minutes=5)
