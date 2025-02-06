from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from db import db
from Modelos import Registro, PagoRecurrente

def procesar_pagos_recurrentes():
    """ Función que ejecuta los pagos recurrentes automáticamente. """
    hoy = datetime.utcnow()
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
        db.session.add(nuevo_registro)

        # Actualizar la fecha del siguiente pago
        if pago.frecuencia == "diario":
            pago.siguiente_pago += timedelta(days=1)
        elif pago.frecuencia == "semanal":
            pago.siguiente_pago += timedelta(weeks=1)
        elif pago.frecuencia == "mensual":
            pago.siguiente_pago += timedelta(days=30)
        elif pago.frecuencia == "anual":
            pago.siguiente_pago += timedelta(days=365)

        db.session.commit()

    print(f"Pagos recurrentes procesados: {len(pagos)}")

# Configurar el scheduler en segundo plano
scheduler = BackgroundScheduler()
scheduler.add_job(procesar_pagos_recurrentes, 'interval', days=1)  # Se ejecuta cada día a la misma hora
scheduler.start()
