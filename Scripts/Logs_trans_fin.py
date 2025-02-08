import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer
import logging

# Configuración del logging
logging.basicConfig(filename = "/Users/milene/Desktop/MAESTRIA CIENCIA DE DATOS/7. INGENIERIA DE DATOS/PROYECTO FINAL/logs_transacciones.log", level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")

# Configuración del producer Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC = "transacciones_financieras"

try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    logging.info("Conectado a Kafka exitosamente.")
except Exception as e:
    logging.error(f"Error al conectar con Kafka: {str(e)}")
    exit(1)

# Lista de opciones para la simulación
acciones = ["AAPL", "TSLA", "AMZN", "GOOGL", "MSFT"]
tipos_transaccion = ["COMPRA", "VENTA"]
errores_posibles = ["ERROR_API", "ERROR_CONEXION", "TIMEOUT"]

def generar_transaccion():
    accion = random.choice(acciones)
    tipo_transaccion = random.choice(tipos_transaccion)
    cantidad = random.randint(1, 100)
    precio_unitario = round(random.uniform(100, 3000), 2)
    total = round(cantidad * precio_unitario, 2)

    # Determinar si la transacción es exitosa o fallida (10% de fallo)
    estado = "FALLIDO" if random.random() < 0.1 else "EXITOSO"

    # Solo incluir error si el estado es FALLIDO
    error = random.choice(errores_posibles) if estado == "FALLIDO" else None

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": accion,
        "tipo_transaccion": tipo_transaccion,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total,
        "estado": estado,
        "error": error
    }

# Enviar transacciones continuamente
while True:
    transaccion = generar_transaccion()
    print(json.dumps(transaccion, indent=2))
    try:
        producer.send(TOPIC, value = transaccion)
        logging.info(f"Transacción enviada: {transaccion}")
    except Exception as e:
        logging.error(f"Error enviando transacción: {str(e)}")
    
    time.sleep(1)  # Envía un log cada segundo
    